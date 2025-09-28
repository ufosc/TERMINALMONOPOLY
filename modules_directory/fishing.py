import time
import random
from utils.utils import g, set_cursor_str
# import modules_directory.inventory as inv

class fishing_game():
    """
    Fishing Game
    Author: Adam Gulde (github.com/adamgulde)
    Version: 1.3 (2/27/2025) Updated to adhere to new module constraints
    Written on an airplane in an hour, roughly.
    This class interfaces with player.py perfectly. 
    """
    def __init__(self) -> None:
        self.__fishies = g.copy()
        self.__pictures = []
        self.__pictures.append(self.__fishies.pop('fishing 1 idle'))
        self.__pictures.append(self.__fishies.pop('fishing 1 win'))
        self.__catchtime = 0
        self.__inventory = None

    def start(self, inventory) -> str:
        start = int(time.time())
        delay = random.randint(3,10)
        self.__catchtime = start + delay
        self.__inventory = inventory
        return self.__pictures[0]

    def get_input(self) -> str:
        return input()

    def results(self) -> str:
        retval = set_cursor_str(0,0) + self.__pictures[1]
        # if self.__catchtime < int(time.time()) < self.__catchtime + 5:
        if random.choice([True, False]):
            fish = random.choice(['Carp', 'Bass', 'Salmon'])
            self.__inventory.add_item(fish, 1) # added fish to inventory
            
            retval += set_cursor_str(24 - (1 if fish == 'Salmon' else 0), 3) + 'Nice job, you caught a ' + fish + '!'
            fish_graphic = self.__fishies['fishing 1 ' + fish.lower()]
            retval += set_cursor_str(36,7) + fish_graphic[0:3]
            retval += set_cursor_str(36,8) + fish_graphic[3:6]
            retval += set_cursor_str(36,9) + fish_graphic[6:9]

        else:    
            retval += set_cursor_str(33, 3) + 'No luck...'

        return retval

name = "Fishing Game"
author = "https://github.com/adamgulde"
version = "1.3" # Moved to its own file
command = "fish"
help_text = "Type FISH to go fishing, and press ENTER to try to reel something in! Go fishing!"
persistent = False

fishing_game_obj = fishing_game() 
# def run(inventory: inventory, gamestate: str = 'start') -> tuple[str, str]:
#     """
#     Fishing module handler for player.py. Returns tuple of [visual data, gamestate] both as strings.
#     """
#     stdIn = ''
#     if (gamestate == 'start'):
#         return fishing_game_obj.start(inventory), 'playing'
#     elif (gamestate == 'playing'):
#         stdIn = fishing_game_obj.get_input()
#         if stdIn == 'e':
#             return '', 'e'
#         return fishing_game_obj.results(), 'e'  
#     elif (gamestate == 'e'):
#         return '', 'start'  