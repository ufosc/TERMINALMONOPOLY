import keyboard
import os
from time import sleep
import screenspace as ss
from socket import socket
import networking as net
from style import set_cursor_str, set_cursor, graphics as g
from modules_directory.inventory import Inventory

class Shop():
    def __init__(self):
        self.x = 38
        self.y = 6
        self.options = []

        # These are the menus that will be displayed in the shop interface.
        self.menus = ["Salmon Pro Shop", "Module Modifiers", "Board Upgrades", "Defensive Items"]

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
        retval = g.get('shop')
        y = 6
        retval += set_cursor_str(33, 3) + "=== Welcome to the Shop ==="
        retval += set_cursor_str(33, 4) + "Use W/S to navigate and Enter to select."
        
        for i, menu in enumerate(self.menus):
            if i == selected_index:
                retval += set_cursor_str(38, y) + f"> {menu}"
            else:
                retval += set_cursor_str(38, y) + f"  {menu}"
            y += 1

        return retval 
        
    def generate_menu(self, title: str, items: dict, cursor_y: int = 6, cursor_x: int = 43) -> str:
        """
        Generates a menu with the given items and highlights the selected index.

        Parameters:
            items (dict): A dictionary where keys are item names and values are their prices.
            selected_index (int): The index of the currently selected item.
            start_y (int): The starting y-coordinate for the menu.

        Returns:
            str: The formatted menu string.
        """
        retval = g.get("shop_2")
        retval += set_cursor_str(cursor_x, cursor_y) + title.capitalize().center(20)
        cursor_y += 2 # Extra line between title and content
        for i, (item, price) in enumerate(items.items()):
            if i == 0:
                retval += set_cursor_str(cursor_x, cursor_y) + f"> {item}: ${price}"
            else:
                retval += set_cursor_str(cursor_x, cursor_y) + f"  {item}: ${price}"
            cursor_y += 1

        return retval
    
    def generic_menu(self, title: str, items: dict, server: socket, active_terminal: ss.Terminal, player_id: int, cursor_x: int = 43, cursor_y: int = 6):
        """
        Displays a generic menu for the shop and handles user input.

        Parameters:
            title (str): The title of the menu.
            items (dict): A dictionary of items and their prices.
            server (socket): The server socket for communication.
            active_terminal (ss.Terminal): The active terminal object.
            player_id (int): The player's ID.
            cursor_x (int): The x-coordinate for the cursor.
            cursor_y (int): The y-coordinate for the cursor.
        """
        display_text = self.generate_menu(title, items, 2, 23) # Generate the menu with the given title and items. Do this *once*.
        active_terminal.update(display_text, padding=False) 
        selected_index = 0
        selecting = True
        sleep(0.25) # Sleep to prevent an accidental purchase from pressing "enter" too fast.
        while keyboard.is_pressed("enter"):
            pass  # Wait for the user to release the enter key before proceeding.

        while selecting:
            if keyboard.is_pressed('w') or keyboard.is_pressed('up'):  # Move up in the menu
                display_text += set_cursor_str(cursor_x, cursor_y + selected_index) + " "
                selected_index = (selected_index - 1) % len(items.keys())  # Wrap around to the last menu item if at the top
                display_text += set_cursor_str(cursor_x, cursor_y + selected_index) + ">" # Set the cursor to the selected menu item.

                active_terminal.update(display_text, padding=False)
                while keyboard.is_pressed('w') or keyboard.is_pressed('up'):
                    pass # Wait for the user to release the up key before proceeding.
            elif keyboard.is_pressed('s') or keyboard.is_pressed('down'):  # Move down in the menu
                display_text += set_cursor_str(cursor_x, cursor_y + selected_index) + " "
                selected_index = (selected_index + 1) % len(items.keys())  # Wrap around to the last menu item if at the top
                display_text += set_cursor_str(cursor_x, cursor_y + selected_index) + ">" # Set the cursor to the selected menu item.
                
                active_terminal.update(display_text, padding=False)
                while keyboard.is_pressed('s') or keyboard.is_pressed('down'):
                    pass # Wait for the user to release the down key before proceeding.

            elif keyboard.is_pressed("enter"):  # Select item
                selected_item = list(items.keys())[selected_index]
                net.send_message(server, f"{player_id}shop,select,{title},{selected_item}")  # Send the selected item to the server
                while keyboard.is_pressed("enter"):
                    pass # Wait for the user to release the enter key before proceeding.

                display_text += set_cursor_str(cursor_x, 10) + " " * (70 - cursor_x) # Clear the line for the cat's response. 
                response = set_cursor_str(cursor_x, 10) + net.receive_message(server) # Receive the cat's response to the purchase.
                display_text += response

                active_terminal.update(display_text, padding=False)  # Update the terminal with the response

            elif keyboard.is_pressed("q"):  # Quit menu
                selecting = False  # Exit the loop
                break  # Exit the loop

    def shop_interface(self, server: socket, active_terminal: ss.Terminal, player_id: int): # menu is the current menu that is being displayed. Default is main menu.
        """
        Display the shop interface and handle the player's input."
        """
        ret_val = self.display_shop()
        active_terminal.update(ret_val, padding=False) # Show the shop art and menu options
        sleep(0.25) # Sleep to prevent the keyboard hook from being triggered by the shop interface.

        selected_index = 0
        selecting = True
        while selecting:
            if keyboard.is_pressed('w') or keyboard.is_pressed('up'):
                ret_val += set_cursor_str(self.x, self.y + selected_index) + " "
                selected_index = (selected_index - 1) % len(self.menus) # Wrap around to the last menu if at the top.
                ret_val += set_cursor_str(self.x, self.y + selected_index) + ">" # Set the cursor to the selected menu item.
                active_terminal.update(ret_val, False) # Inefficient
                while keyboard.is_pressed('w') or keyboard.is_pressed('up'):
                    pass # Wait for the user to release the up key before proceeding.
            if keyboard.is_pressed('s') or keyboard.is_pressed('down'):  # Move down in the menu.
                ret_val += set_cursor_str(self.x, self.y + selected_index) + " "
                selected_index = (selected_index + 1) % len(self.menus)
                ret_val += set_cursor_str(self.x, self.y + selected_index) + ">" 
                active_terminal.update(ret_val, False)
                while keyboard.is_pressed('s') or keyboard.is_pressed('down'):
                    pass # Wait for the user to release the down key before proceeding.
            if keyboard.is_pressed("q"):  # Quit shop.
                net.send_message(server, f"{player_id}shop,exit")  # Send the exit command to the server.
                selecting = False  # Exit the loop.
            if keyboard.is_pressed("enter"):  # Select item.
                
                if self.menus[selected_index] == "Salmon Pro Shop":
                    self.generic_menu("Salmon Pro Shop", self.fishprices, server, active_terminal, player_id, 23, 4)  # Call the fish menu.
                elif self.menus[selected_index] == "Module Modifiers":
                    self.generic_menu("Module Modifiers", self.module_modifiers, server, active_terminal, player_id, 23, 4)
                elif self.menus[selected_index] == "Board Upgrades":
                    self.generic_menu("Board Upgrades", self.board_upgrades, server, active_terminal, player_id, 23, 4)
                elif self.menus[selected_index] == "Defensive Items":
                    self.generic_menu("Defensive Items", self.defensive_items, server, active_terminal, player_id, 23, 4)

                sleep(0.25) # Delay to enter a new screen
                active_terminal.update(ret_val, False) # Update the terminal to show the shop art and menu options again.

name = "Shop Module"
author = "https://github.com/Eon02"
description = "Buy and sell items here!"
version = "1.4 - Reworking to add other internal shops - adamgulde"
command = "shop"
help_text = "Type SHOP to enter the shop. Press W/S to navigate and Enter to select. Press Q to exit the shop."
persistent = False

shop_object = Shop()

def run(player_id: int, server: socket, active_terminal: ss.Terminal):
    ss.indicate_keyboard_hook(active_terminal.index)
    active_terminal.persistent = persistent
    shop_object.shop_interface(server, active_terminal, player_id) # Run the shop interface.

    ss.update_terminal(active_terminal.index, active_terminal.index) # Turn off the keyboard hook indication
    active_terminal.update(g.get("shop_exit"))

def handle(data: str, client_socket: socket, player_inventory: Inventory, player_balance: int) -> None:
    """
    Data is received of form "shop,select,SUBSHOP,ITEM" or "shop,exit" where SUBSHOP is the name 
    of the shop type and ITEM is the name of the item to be bought.

    Always make sure to send a net.send_message to client socket even if a purchase is unsuccessful. 
    This is what the cat says. It can be empty string.
    """
    cmds = data.split(",")
    if cmds[1] == "exit":
        return
    elif cmds[1] == "select":
        subshop = cmds[2]
        item = cmds[3]
        if subshop == "Salmon Pro Shop":
            if player_inventory.getinventory()["fish"].get(item) > 0:
                player_inventory.remove_item(item, 1)
                player_balance += shop_object.fishprices[item]
                net.send_message(client_socket, f"Meow! Sold {item} for ${shop_object.fishprices[item]}")
            else:
                net.send_message(client_socket, f"Prrr... No {item} to sell")
        elif subshop == "Module Modifiers":
            pass
        elif subshop == "Board Upgrades":
            pass
        elif subshop == "Defensive Items":
            pass

    