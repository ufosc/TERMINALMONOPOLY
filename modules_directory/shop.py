import keyboard
import os
import screenspace as ss
from socket import socket
import networking as net
from style import set_cursor_str, graphics as g
from modules_directory.inventory import Inventory

class Shop():
    # TODO : Shop needs to reference the players own inventory
    def __init__(self): #pass in an inventory object that shop can access
        # These are the menus that will be displayed in the shop interface.
        self.menus = ["Salmon Pro Shops", "Module Modifiers", "Board Upgrades", "Defensive Items"]

        # These are the items that can be bought in the shop. The key is the item name and the value is the price.
        self.fishprices = {"Carp": 5, "Bass": 8, "Salmon": 12}
        self.module_modifiers = {"[FISH] Reinforced Fishing Rod": 50, "[STOCKS] Sway the Quants": 100, "[STOCKS] Invest in Regulation Agencies": 100,
                                 "[CASINO] Bottle of Felix Felicis": 200}
        self.board_upgrades = {"Build a Story": 200, "Move Token": 200, "Bribe the Warden": 50}
        self.defensive_items = {"Terminal Shield": 500}

        # If you add more menus, add them to the respective list and the items to the respective dictionary.
        
    def display_shop(self, selected_index:int =0):
        """
        Display the shop interface with the current selection highlighted.
        Only called once at the start of the shop interface.
        """
        retval = set_cursor_str(0,0) + g.get('shop')
        y = 6
        retval += set_cursor_str(33, 3) + "=== Welcome to the Shop ==="
        retval += set_cursor_str(33, 4) + "Use W/S to navigate and Enter to select."
        
        for i, menu in enumerate(self.menus):
            if i == selected_index:
                retval += set_cursor_str(33, y) + f"> {menu}"

        return retval 
        
    def fish_menu(self, selected_index:int = 0):
        retval = ""
        y = 6
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

    def module_modifiers_menu(self, selected_index:int = 0):
        retval = ""
        y = 6
        for i, price in enumerate(self.module_modifiers.keys()):
            if i == selected_index:
                retval += set_cursor_str(43, y) + f"> {price}: ${self.module_modifiers[price]}"
            else:
                retval += set_cursor_str(43, y) + f"  {price}: ${self.module_modifiers[price]}"
            y += 1
        y += 1 # Add a blank line between menus and inventory.

        retval += set_cursor_str(45, y) + "Your inventory: "
    
    def sellfish(self, fish):
        if self.inventory.getinventory()[fish] > 0:
            self.inventory.removefish(fish)
            print(f"Sold {fish} for ${self.fishprices[fish]}")
        else:
            print(f"No {fish} to sell")

    def shop_interface(self, server: socket, menu="Main"): # menu is the current menu that is being displayed. Default is main menu.
        selected_index = 0
        selecting = True
        while selecting:
            key = keyboard.read_event()
            if key.event_type == "down":
                if key.name == "w":
                    selected_index = (selected_index - 1) % len(self.menus)
                elif key.name == "up": # Move up in the menu.
                    selected_index = (selected_index - 1) % len(self.menus) # Move up in the menu.
                elif key.name == "s": # Move down in the menu.
                    selected_index = (selected_index + 1) % len(self.menus) # Move down in the menu.
                elif key.name == "down": # Move down in the menu.
                    selected_index = (selected_index + 1) % len(self.menus) # Move down in the menu.
                elif key.name == "enter": # Select item.
                    net.send_message(server, "menu_select," + self.menus[selected_index]) # Send the selected menu to the server.
                    selecting = False # Exit the loop.
                elif key.name == "q": # Quit shop.
                    net.send_message(server, "menu_select,exit") # Send the exit command to the server.
                    selecting = False # Exit the loop.

        
    def fish_interface(self):
        selected_index = 0
        shopping = True
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
version = "1.3 - Updating to sell more items and work in the new Terminal system"
command = "shop"
help_text = "Type SHOP to enter the shop. Press W/S to navigate and Enter to select. Press Q to exit the shop."
persistent = False

shop_object = Shop()

def run(player_id: int, server: socket, active_terminal: ss.Terminal):
    ss.indicate_keyboard_hook(active_terminal.index)
    active_terminal.persistent = persistent
    active_terminal.update(g.get("shop_exit"))
    shop_object.shop_interface(server) # Run the shop interface.
    ss.update_terminal(active_terminal.index, active_terminal.index) # Turn off the keyboard hook indication
    

# def run(inventory: inventory, active_terminal: ss.Terminal) -> str:
    # active_terminal.update(Shop(inventory).display_shop()) # temporary, will be replaced with banker Shop communication

def handle(data: str, client_socket: socket, player_inventory: Inventory) -> None:
    if data == "get_shop_interface":
        net.send_message(client_socket, shop_object.display_shop())
    elif data == "buy_fish":
        pass
    