import time
import random
import modules_directory.inventory as inventory
from utils.screenspace import g, set_cursor_str, Terminal
from socket import socket
import utils.networking as net

name = "Fish loader"
command = "fish"
description = "Women want me, fish FEAR me."
help_text = "Type FISH to start catching, the fish can smell money."
persistent = False # No need to run additional commands after switching

class fishing_game():
    """
    Fishing Game
    Author: Amy Hoang (https://github.com/TiniToni)
    Version: 1.4 (9/28/2025) Updated to adhere to new design philosophy
    """
    def __init__(self) -> None:
        self.__fishies = g.copy()
        self.__pictures = []
        self.__pictures.append(self.__fishies.pop('fishing 1 idle'))
        self.__pictures.append(self.__fishies.pop('fishing 1 win'))
        self.__catchtime = 0

    #this is not actually used
    def start(self) -> str:
        start = int(time.time())
        delay = random.randint(3,10)
        self.__catchtime = start + delay
        return self.__pictures[0]

    def get_input(self) -> str:
        return input()

    def results(self, player_inventory: inventory) -> str:
        retval = set_cursor_str(0,0) + self.__pictures[1]
        if random.choice([True, False]):
            fish = random.choice(['Carp', 'Bass', 'Salmon'])
            player_inventory.add_item(fish, 1) # added fish to inventory
            
            retval += set_cursor_str(24 - (1 if fish == 'Salmon' else 0), 3) + 'Nice job, you caught a ' + fish + '!'
            fish_graphic = self.__fishies['fishing 1 ' + fish.lower()]
            retval += set_cursor_str(36,7) + fish_graphic[0:3]
            retval += set_cursor_str(36,8) + fish_graphic[3:6]
            retval += set_cursor_str(36,9) + fish_graphic[6:9]

        else:    
            retval += set_cursor_str(33, 3) + 'No luck...'

        return retval
def run(player_id: int, server: socket, active_terminal: Terminal):
    """
    Run the fishing module.
    
    Parameters:
        server (socket): The server socket for communication.
        active_terminal (ss.Terminal): The active terminal object.
    """
    active_terminal.clear()
    active_terminal.persistent = persistent
    active_terminal.update(g.get('fishing 1 idle'))
    playerinput = input("Type anything to catch a fish")
    net.send_message(server, f'{player_id}fish,reel')
    retval = net.receive_message(server)
    active_terminal.update(retval, False)

def handle(client_socket: socket, player_inventory: inventory)->None:
    """
    Handles fishing and inventory interaction

    Parameters:
    client_socket (socket): The client socket to send messages to
    player_inventory (inventory): The player's inventory object
    player_id (int): The Player's ID --> same as above
    """
    message = fishing_game_obj.results(player_inventory)
    net.send_message(client_socket, message)

fishing_game_obj = fishing_game()