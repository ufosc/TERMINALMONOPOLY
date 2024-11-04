import screenspace as ss
import style as s
import random
import os
# Now that this has been moved to modules_directory, it does not 
# run standalone with the current imports. This is *fine* because
# it does not *need* to standalone, but debugging could get 
# annoying. 

class Ship():
    """
        Patrol
        ╔═╗
        ╚═╝

        Submarine
        ╔══╦╗
        ╚══╩╝

        Destroyer
        ╔═╦╩╗
        ╣ ╠╣╠
        ╚═╩╦╝

        Battleship
        ╔╩╩╩╩╗
        ╣╬╬╬╬╠
        ╚╦╦╦╦╝

        Carrier
        ╔═╦═╦═╗
        ║»║¤║«║
        ╚═╩═╩═╝
    """
    def __init__(self, x: int, y: int, name: str) -> None:
        self.x = x
        self.y = y
        if name == "patrol":
            self.icon = "╔═╗╚═╝"
            self.size = (3,2)
            self.name = "Patrol Boat"
            self.health = 1
        elif name == "submarine":
            self.icon = "╔══╦╗╚══╩╝"
            self.size = (5,2)
            self.name = "Submarine"
            self.health = 3
        elif name == "destroyer":
            self.icon = "╔═╦╩╗╣ ╠╣╠╚═╩╦╝"
            self.size = (5,3)
            self.name = "Destroyer"
            self.health = 3
        elif name == "battleship":
            self.icon = "╔╩╩╩╩╗╣╬╬╬╬╠╚╦╦╦╦╝"
            self.size = (6,3)
            self.name = "Battleship"
            self.health = 4
        elif name == "carrier":
            self.icon = "╔═╦═╦═╗║»║¤║«║╚═╩═╩═╝"
            self.size = (7,3)
            self.name = "Aircraft Carrier"
            self.health = 5
        else: 
            print("Invalid ship name.")

    def in_bounds(self, x, y) -> bool:
        return x + self.size[0] <= ss.cols and y + self.size[1] <= ss.rows and x >= 2 and y >= 1
    
    def __str__(self) -> str:
        return self.name
        
class BattleshipGame():
    """
    Battleship Game
    Author: Adam Gulde (github.com/adamgulde)
    Version: 1.0.0
    https://en.wikipedia.org/wiki/Battleship_(game)
    """
    def __init__(self) -> None:
        self.board = self.generate_water_and_coords()
        self.players = 1
        self.player_names = []
        self.ships = [[] * self.players]
        self.changed_coords = []
        self.gamestate = 'placing ships' # other gamestates are 'p1 turn', 'p2 turn', 'p3 turn', 'p4 turn' 

    def generate_water_and_coords(self) -> str:
        texture = ""
        texture += s.COLORS.backCOMMUNITY + s.COLORS.BLACK
        for x in range(0, ss.cols, 3):
            texture +=  f"{x}  " if x < 10 else f"{x} "
        texture += "\n"
        for y in range(1, ss.rows):
            texture += s.COLORS.backCOMMUNITY + s.COLORS.BLACK
            texture += (str(y) + (" " if y < 10 else "") if y % 2 == 0 else "  ")
            texture += f"{s.COLORS.backLIGHTBLUE}{s.COLORS.BLUE}"
            for _ in range(ss.cols-2):
                texture += random.choices(
                    ["░", "▒", "▓"],
                    weights=[1, 2, 7],  # Adjust weights to create larger pools of dark textures
                    k=1
                )[0]
            texture += "\n"
        self.board = texture + s.COLORS.RESET
        return self.board

    def print_ship(self, sh: Ship, playerNum = 0) -> str:
        text = s.COLORS.playerColors[playerNum]
        for i in range(sh.size[1]):
            text += f"{s.set_cursor_str(sh.x+1,sh.y+i+1)}{sh.icon[i*sh.size[0]:(i+1)*sh.size[0]]}\n"
        return text

    def print_explosion(self, x: int, y: int) -> str:
        text = ""
        text += s.set_cursor_str(x,y) + random.choice([s.COLORS.ORANGE, s.COLORS.RED]) + random.choice(["░", "▒", "▓"])
        return text

    def print_miss(self, x: int, y: int) -> str:
        text = s.COLORS.LIGHTGRAY
        text += s.set_cursor_str(x,y) + random.choice(["░", "▒", "▓"])

        return text

    def popup(self, message: str, color: str = s.COLORS.WHITE) -> str: 
        """
        ...fill in comment
        x and y params should be top left corner of terminal.
        """
        message = message + " " * max(0, (78 - len(message)))
        # Max 78 character popup for messaging the player.

        p = color + s.set_cursor_str(25, 5)
        outline = s.get_graphics()["popup 1"].split("\n")
        for i in range(len(outline)):
            p += s.set_cursor_str(25, 5+i) + outline[i]
            if 0 < i < 4:
                # Custom text wrapping
                p += s.set_cursor_str(27, 5+i) + message[(i-1)*26:(i-1)*26+26]
        return p 

    def get_valid_int(self, prompt):
        while True:
            try:
                s.set_cursor(0, ss.INPUTLINE)
                value = int(input(prompt))
                return value
            except ValueError:
                self.popup("Invalid input. Please     enter a valid integer.", s.COLORS.RED)
                s.set_cursor(0, ss.INPUTLINE)

    def is_overlapping(self, x: int, y: int, size: tuple, player_num: int) -> Ship:
        for sh in self.ships[player_num]:
            if (x < sh.x + sh.size[0] and x + size[0] > sh.x and
                y < sh.y + sh.size[1] and y + size[1] > sh.y):
                return sh
        return None

    def place_ships(self, current_board:str, player_num:int = 0) -> str:
        return_board = current_board
        s.set_cursor(0, ss.INPUTLINE)
        ships_to_place = [Ship(-1, -1, "patrol"), Ship(-1, -1, "submarine"), Ship(-1, -1, "destroyer"), 
                        Ship(-1, -1, "battleship"), Ship(-1, -1, "carrier")]
        self.ships[player_num].clear()
        return_board = self.get_ship_board(player_num)
        for ship in ships_to_place:
            while ship.x == -1 :
                x = self.get_valid_int(f"Enter x-coordinate for your {ship}: ")
                y = self.get_valid_int(f"Enter y-coordinate for your {ship}: ")
                
                if ship.in_bounds(x, y):
                    if self.is_overlapping(x, y, ship.size, player_num) == None:
                        ship.x = x
                        ship.y = y
                        self.ships[player_num].append(ship)
                    else:
                        return self.popup(f"Error! This ship is on    another ship. Recall this ship size is {ship.size}", s.COLORS.RED)
                else:
                    return self.popup(f"Error! Out of bounds. Max x is {ss.cols-ship.size[0]}. Max y is {ss.rows-ship.size[1]}", s.COLORS.RED)

            return_board = self.get_ship_board(player_num)   
            s.set_cursor(0, ss.INPUTLINE)
        
        done = input("Does this look good? n for no, anything else for yes.")
        if done == 'n':
            while done != 'y':
                move = self.get_valid_int(f"Enter a number (0-4) of a ship to remove from the list {[ship.name for ship in self.ships[player_num]]}: ")
                if 0 <= move < len(self.ships[player_num]):
                    self.ships[player_num].pop(move)
                    return_board = self.get_ship_board(player_num)
                    s.set_cursor(0, ss.INPUTLINE)
                    ship_names = ['patrol', 'submarine', 'destroyer', 'battleship', 'carrier']
                    new_ship = Ship(-1, -1, ship_names[move])
                    while new_ship.x == -1:
                        x = self.get_valid_int(f"Enter x-coordinate for your {new_ship}: ")
                        y = self.get_valid_int(f"Enter y-coordinate for your {new_ship}: ")
                        
                        if new_ship.in_bounds(x, y):
                            if self.is_overlapping(x, y, new_ship.size, player_num) == None:
                                new_ship.x = x
                                new_ship.y = y
                                self.ships[player_num].insert(move, new_ship)
                            else:
                                return self.popup(f"Error! This ship is on    another ship. Recall this ship size is {new_ship.size}", s.COLORS.RED)
                        else:
                            return self.popup(f"Error! Out of bounds. Max x is {ss.cols-new_ship.size[0]}. Max y is {ss.rows-new_ship.size[1]}", s.COLORS.RED)
                    return_board = self.get_ship_board(player_num)   
                    done = input("Does this look good? y for yes, anything else for no.")

        return return_board

    def get_ship_board(self, player_num:int) -> str:
        # os.system("cls")
        current_board = self.board
        for ship in self.ships[player_num]:
            current_board += self.print_ship(ship)
        return current_board

    def attack(self):
        while(len(self.ships) > 0): # not correct final logic, temporary
            s.set_cursor(0, ss.INPUTLINE)
            x = self.get_valid_int("Enter x-coordinate for your attack: ")
            if x < 2 or x > 74:
                self.popup("Error! Out of bounds. Please enter a valid          coordinate (2-74) inclusive.", s.COLORS.RED)
                continue
            y = self.get_valid_int("Enter y-coordinate for your attack: ")
            if y < 1 or y > 19:
                self.popup("Error! Out of bounds. Please enter a valid          coordinate (1-19) inclusive.", s.COLORS.RED)   
                continue
            if (x,y) in self.changed_coords:
                self.popup("Error! This coordinate has already been attacked.", s.COLORS.RED)
                continue
            else:   
                self.changed_coords.append((x,y))
                for player_ship_list in self.ships:
                    for ship in player_ship_list:
                        if self.is_overlapping(x, y, (1,1)) == ship:
                            self.popup(f"Hit! You hit the {ship.name}!", s.COLORS.dispBLUE)
                            self.board += self.print_explosion(x+1, y+1)
                            ship.health -= 1
                            if ship.health == 0:
                                player_ship_list.remove(ship)
                                for i in range(ship.size[0]):
                                    for j in range(ship.size[1]):
                                        self.board += self.print_explosion(ship.x+i+1, ship.y+j+1)
                                self.popup(f"You sunk the {ship.name}!", s.COLORS.dispBLUE)
                            break
                        else:
                            self.popup("Miss!.", s.COLORS.RED)
                            self.board += self.print_miss(x+1, y+1)
            s.set_cursor(0, ss.INPUTLINE)
            input("Press enter to continue.")
            print(self.get_board())
        
def start_game() -> BattleshipGame:
    ships = BattleshipGame()
    return ships

if __name__ == "__main__":
    os.system("cls")

    ships = BattleshipGame()
    print(ships.board)
    # ships.place_ships(ships.board, 0)
    # s.set_cursor(0,0)
    # print(ships.board)
    # print(ships.get_ship_board(0))

    # def unittest1():
    #     ships.p1ships = [Ship(3,10,"patrol"), Ship(12,2,"submarine"), Ship(33,5,"destroyer"), Ship(50,7,"battleship"), Ship(15,9,"carrier")]
    # unittest1() 

    # ships.attack()