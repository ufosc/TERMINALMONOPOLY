import time
import random
from style import get_graphics, set_cursor, set_cursor_str

class fishing_game():
    """
    Fishing Game
    Author: Adam Gulde (github.com/adamgulde)
    Version: 1.0
    Written on an airplane in an hour, roughly.
    This class interfaces with player.py perfectly. 
    If you want to playtest the game you can run the file by itself.
    """
    def __init__(self) -> None:
        graphics = get_graphics()
        self.__fishies = graphics.copy()
        self.__pictures = []
        self.__pictures.append(self.__fishies.pop('fishing 1 idle'))
        self.__pictures.append(self.__fishies.pop('fishing 1 win'))
        self.__catchtime = 0
        self.__inventory = []

    def start(self):
        start = int(time.time())
        delay = random.randint(3,10)
        self.__catchtime = start + delay
        return self.__pictures[0]

    def get_input(self) -> str:
        return input()

    def results(self) -> str:
        retval = set_cursor_str(0,0) + self.__pictures[1]
        if self.__catchtime < int(time.time()) < self.__catchtime + 5:
        # if random.choice([True, False]):
            fish = random.choice(['carp', 'bass', 'salmon'])
            self.__inventory.append(fish) # added fish to inventory
            
            retval += set_cursor_str(24 - (1 if fish == 'salmon' else 0), 3) + 'Nice job, you caught a ' + fish + '!'
            fish_graphic = self.__fishies['fishing 1 ' + fish]
            retval += set_cursor_str(36,7) + fish_graphic[0:3]
            retval += set_cursor_str(36,8) + fish_graphic[3:6]
            retval += set_cursor_str(36,9) + fish_graphic[6:9]

        else:    
            retval += set_cursor_str(33, 3) + 'No luck...'

        return retval

    def get_inventory(self)->list:
        return self.__inventory

if __name__ == "__main__":
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    graphics = get_graphics()

    pictures = []

    fishies = graphics.copy()

    pictures.append(fishies.pop('fishing 1 idle'))
    pictures.append(fishies.pop('fishing 1 win'))

    print(pictures[0])

    start = int(time.time())
    delay = random.randint(3,10)
    catchtime = start + delay
   
    input()
    set_cursor(0,0)
    print(pictures[1])
    print()
    print()
    if catchtime < int(time.time()) < catchtime + 5:
        fish = random.choice(['carp', 'bass', 'salmon'])

        retval = ""
        retval += set_cursor_str(24 - (1 if fish == 'salmon' else 0), 3) + 'Nice job, you caught a ' + fish + '!'
        fish_graphic = fishies['fishing 1 ' + fish]
        retval += set_cursor_str(37,9) + fish_graphic[0:3]
        retval += set_cursor_str(37,10) + fish_graphic[3:6]
        retval += set_cursor_str(37,11) + fish_graphic[6:9]

        print(retval)

    else:    
        set_cursor(33, 5)
        print('No luck...')
    set_cursor(0, 40)

