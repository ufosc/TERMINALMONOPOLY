import keyboard
import os
import screenspace as ss
from socket import socket
import networking as net
from style import set_cursor_str, graphics as g
import modules_directory.inventory as inventory

class Shop():
    # TODO : Shop needs to reference the players own inventory
    def __init__(self, inventory): #pass in an inventory object that shop can access
        self.inventory = inventory
        self.fishprices = {"Carp": 5, "Bass": 8, "Salmon": 12}
        
    def display_shop(self, selected_index:int =0):
        """
        Display the shop interface with the current selection highlighted.
        Only called once at the start of the shop interface.
        """
        retval = set_cursor_str(0,0) + g.get('shop')
        y = 6
        retval += set_cursor_str(33, 3) + "=== Welcome to the Shop ==="
        retval += set_cursor_str(33, 4) + "Use W/S to navigate and Enter to select."
        for i, price in enumerate(self.fishprices.keys()):
            if i == selected_index:
                retval += set_cursor_str(43, y) + f"> {price}: ${self.fishprices[price]}"
            else:
                retval += set_cursor_str(43, y) + f"  {price}: ${self.fishprices[price]}"
            y += 1
        y += 1
        
        retval += set_cursor_str(45, y) + "Your inventory: "
        # for fish in testfishinventory.caughtfish.keys():
        #     if testfishinventory.caughtfish[fish] > 0:
        #         retval += set_cursor_str(45, y+1) + f"{fish} x{testfishinventory.caughtfish[fish]} "
              
        return retval
        # print(retval)
        
    def sellfish(self, fish):
        if self.inventory.getinventory()[fish] > 0:
            self.inventory.removefish(fish)
            print(f"Sold {fish} for ${self.fishprices[fish]}")
        else:
            print(f"No {fish} to sell")

    # TODO: update shop screen in response to input
    def shop_interface(self):
        selected_index = 0
        shopping = True
        self.display_shop(selected_index)
        while shopping:
            key = keyboard.read_event()
            if key.event_type == "down":
                if key.name == "w":  # Move up
                    selected_index = (selected_index - 1) % len(self.fishprices)
                elif key.name == "up":
                    selected_index = (selected_index - 1) % len(self.fishprices)
                elif key.name == "s":  # Move down
                    selected_index = (selected_index + 1) % len(self.fishprices)
                elif key.name == "down":
                    selected_index = (selected_index + 1) % len(self.fishprices)
                elif key.name == "enter":  # Select item
                    os.system('cls' if os.name == 'nt' else 'clear')
                    selected_fish = self.fishprices[list(self.fishprices.keys())[selected_index]]
                    
                    keyboard.read_event()
                elif key.name == "q":  # Quit shop
                    shopping = False
                y = 6
                for i, price in enumerate(self.fishprices.keys()):
                    if i == selected_index:
                        print(set_cursor_str(43, y) + f"> {price}: ${self.fishprices[price]}")
                    else:
                        print(set_cursor_str(43, y) + f"  {price}: ${self.fishprices[price]}")
                    y += 1
                    
        # os.system('cls' if os.name == 'nt' else 'clear')

name = "Shop Module"
author = "https://github.com/Eon02"
description = "Buy and sell items here!"
version = "1.2"
command = "shop"
help_text = "Type SHOP to enter the shop. Press W/S to navigate and Enter to select. Press Q to exit the shop."
persistent = False

def run(player_id, server, active_terminal: ss.Terminal):
    active_terminal.update(g.get("shop_exit"))

# def run(inventory: inventory, active_terminal: ss.Terminal) -> str:
    # active_terminal.update(Shop(inventory).display_shop()) # temporary, will be replaced with banker Shop communication
