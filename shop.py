

import screenspace as ss
import keyboard
import os
from style import get_graphics, set_cursor, set_cursor_str, COLORS


class FishInventory():
    def __init__(self):
        self.caughtfish = {"Carp": 1, "Bass": 0, "Salmon": 0}
    
    def getinventory(self):
        return self.caughtfish
    
    def addfish(self, fish):
        self.caughtfish[fish] += 1
        return self.caughtfish
    
    def removefish(self, fish):
        self.caughtfish[fish] -= 1
        return self.caughtfish
    
    # need function for viewing inventory

testfishinventory = FishInventory()

class Shop():
    # TODO : Shop needs to reference the players own inventory
    def __init__(self):
        self.fishprices = {"Carp": 5, "Bass": 8, "Salmon": 12}
        graphics = get_graphics()
        self.__shopimages = graphics.copy()
        self.__pictures = []
        self.__pictures.append(self.__shopimages.pop('shop'))
        
    def display_shop(self, selected_index):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self.__pictures[0])
        retval = ""
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
        for fish in testfishinventory.caughtfish.keys():
            if testfishinventory.caughtfish[fish] > 0:
                retval += set_cursor_str(45, y+1) + f"{fish} x{testfishinventory.caughtfish[fish]} "
              
        print(retval)
        
    def sellfish(self, fish):
    # TODO: implement selling properly
    

    # TODO: update shop screen in response to input
    def shop_interface(self):
        
          
        selected_index = 0
        shopping = True
        while shopping:
            self.display_shop(selected_index)
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
                    
        os.system('cls' if os.name == 'nt' else 'clear')
                    
        
def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    shop = Shop()
    shop.shop_interface()
    
    
    
if __name__ == '__main__':
    main()
    

    
