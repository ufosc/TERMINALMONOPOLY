class Inventory():
    def __init__(self):
        """
        Initializes the inventory of the player.
        The inventory is a dictionary of items and their quantities.
        All items are stored here, to be extracted by the shop module.
        """
        self.items = {}
    
    def getinventory(self) -> dict:
        """
        Returns the inventory of the player.
        """
        return self.items
    
    def add_item(self, item: str, quantity: int) -> None:
        """
        Adds an item to the inventory.
        If the item already exists, it adds the quantity to the existing item.
        This could be a fish, or a Terminal upgrade, or an attack Module. 
        """
        if item in self.items:
            self.items[item] += quantity
        else:
            self.items[item] = quantity
    
    def remove_item(self, item: str, quantity: int) -> None:
        """
        Removes an item from the inventory.
        If the item does not exist, it does nothing.
        If the quantity is greater than the quantity of the item, it removes all of the item.
        """
        if item in self.items:
            if self.items[item] > quantity:
                self.items[item] -= quantity
            else:
                del self.items[item]

from socket import socket
from screenspace import Terminal

name = "Inventory Module"
command = "inv"
author = "https://github.com/adamgulde"
description = "View all inventory items."
version = "1.2"
help_text = "Type INV to view your inventory."

def run(server: socket, active_terminal: Terminal, player_id: int):
    item_list = [f"{item}: {quantity}" for item, quantity in Inventory.getinventory().items()]
    if len(item_list) > 0:
        item_list = '\n'.join(item_list)
        if item_list.count("\n") > 18:
            # Truncate the list to 18 lines and add ellipsis
            item_list = '\n'.join(item_list.split('\n')[:18]) + "\n..."
        active_terminal.update(f"Inventory:\n{item_list}", padding=True)
    else: 
        active_terminal.update("Inventory is empty. Try catching some fish!", padding=True)