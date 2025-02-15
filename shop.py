import keyboard
import os
from style import set_cursor_str, graphics as g

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
        self.__pictures = []
        
    def display_shop(self, selected_index):
        """
        Display the shop interface with the current selection highlighted.
        Only called once at the start of the shop interface.
        """
        print(g.get('shop'))
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
        pass

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
                    
        os.system('cls' if os.name == 'nt' else 'clear')
                    
        
def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    shop = Shop()
    shop.shop_interface()
    
    
if __name__ == '__main__':
    main()
    

    
