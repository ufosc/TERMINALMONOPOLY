
import player
from style import get_graphics, set_cursor, set_cursor_str


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


class Shop():
    def __init__(self):
        self.fishprices = {"Carp": 5, "Bass": 8, "Salmon": 12}
        graphics = get_graphics()
        self.__shopimages = graphics.copy()
        self.__pictures = []
        self.__pictures.append(self.__shopimages.pop('shop'))
        
    def shopview(self):
        print(self.__pictures[0])
        retval = ""
        y = 6
        for price in self.fishprices.keys():
            retval += set_cursor_str(45, y) + f"{price}: ${self.fishprices[price]}"
            y +=1
        y += 1
        retval += set_cursor_str(45, y) + "Your inventory: "
        
        for fish in player.playerfish.caughtfish.keys():
            if player.playerfish.caughtfish[fish] > 0:
                retval += set_cursor_str(45, y+1) + f"{fish} x{player.playerfish.caughtfish[fish]} "
              
        print(retval)
        
    def sellfish(self, fish):
        player.balance += self.fishprices[fish]
        FishInventory.removefish(player.playerfish, fish)
        return player.playerfish
    
    def getinput(self):
        choice = input("")
        
        
        
    # need to take input to let player sell the fish
    
        

def main():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    shop = Shop()
    shop.shopview()
    
    
if __name__ == '__main__':
    main()
    

    
