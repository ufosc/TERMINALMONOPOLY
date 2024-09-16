# Monopoly game is played on Banker's terminal. 
from colorama import Fore, Style, Back
import style as s
import random
import os
import platform
import ctypes

class Player: 
    """
    Player class for Monopoly game\n
    Contains player data.\n
    """
    def __init__(self, cash:int, order:int) -> None:
        self.cash = cash
        self.properties = []
        self.order = order
        self.location = 0
        self.jail = False
        self.jailcards = 0
    """
    Player cash\n
    @cash: int\n
    Player properties\n
    @properties: list\n
    Player location\n
    @location: int\n
    Player jail status\n
    @jail: bool\n
    """
    def buy(self, location:int) -> None:
        """
        Buy property\n
        @location: int\n
        """
        self.properties.append(location)
        self.cash -= board.deeds[board.locations[location][0]][0] if board.locations[location][0] in board.deeds else board.special_deeds[board.locations[location][0]][0]
        if board.locations[location][0] in board.special_deeds:
            if location % 5 == 0: #@TODO Only 3 of the railroads correctly appear as bought 
                                    # in unittest1, please fix railroad property condition
                railroads_owned = 0
                for i in range(5, 36, 10):
                    if board.locations[i][3] == self.order:
                        railroads_owned += 1
                for i in range(5, 36, 10):
                    if board.locations[i][3] == self.order:
                        board.locations[i][2] = railroads_owned
            # visually unappealing code, fix if bored
            elif location == 12:
                if board.locations[28][3] == self.order:
                    board.locations[12][2] = 2
                    board.locations[28][2] = 2
                else: board.locations[12][2] = 1
            elif location == 28:
                if board.locations[12][3] == self.order:
                    board.locations[28][2] = 2
                    board.locations[12][2] = 2
                else: board.locations[28][2] = 1
        board.locations[location][3] = self.order
    def pay(self, amount:int) -> None:
        """
        Pay amount\n
        @amount: int\n
        """
        self.cash -= amount
    def receive(self, amount:int) -> None:
        """
        Receive amount\n
        @amount: int\n
        """
        self.cash += amount
    def jail(self) -> None:
        """
        Go to jail\n
        """
        self.location = 10
        self.jail = True
    def leave_jail(self) -> None:
        """
        Leave jail\n
        """
        self.jail = False

    def __str__(self) -> str:
        return f"Player {self.order}"

class Board:
    """
    Board class for Monopoly game\n
    Contains location data.\n
    """
    def __init__(self, num_players) -> None:
        self.locations = {
            # locations[x][3] indicates who owns, but also is used for special codes below:
                # Special codes: -1 is not owned, -2 is mortaged, -3 is community chest, -4 is chance, -5 is tax
                # -6 is jail, -7 is go to jail, -8 is free parking, -9 is luxury, -10 is go 
        0: ["Go", list(range(num_players)), 0, -10, (32,72), s.COLORS["LIGHTGRAY"]],
        1: ["Mediterranean Avenue", [], 0, -1, (32,65), s.COLORS["BROWN"]],
        2: ["Community Chest", [], 0, -3, (32, 58), s.COLORS["COMMUNITY"]],
        3: ["Baltic Avenue", [], 0, -1, (32, 51), s.COLORS["BROWN"]],
        4: ["Income Tax", [], 0, -5, (32, 44), s.COLORS["LIGHTGRAY"]],
        5: ["Reading Railroad", [], 0, -1, (32, 37), s.COLORS["LIGHTBLACK"]],
        6: ["Oriental Avenue", [], 0, -1, (32, 30), s.COLORS["LIGHTBLUE"]],
        7: ["Chance", [], 0, -4, (32, 23), s.COLORS["CHANCE"]],
        8: ["Vermont Avenue", [], 0, -1, (32, 16), s.COLORS["LIGHTBLUE"]],
        9: ["Connecticut Avenue", [], 0, -1, (32, 9), s.COLORS["LIGHTBLUE"]],
        10: ["Jail", [], 0, -7, (32, 2), s.COLORS["LIGHTGRAY"]],
        11: ["St. Charles Place", [], 0, -1, (29, 2), s.COLORS["ROUGE"]],
        12: ["Electric Company", [], 0, -1, (26, 2), s.COLORS["YELLOW"]],
        13: ["States Avenue", [], 0, -1, (23, 2), s.COLORS["ROUGE"]],
        14: ["Virginia Avenue", [], 0, -1, (20, 2), s.COLORS["ROUGE"]],
        15: ["Pennsylvania Railroad", [], 0, -1, (17, 2), s.COLORS["LIGHTBLACK"]],
        16: ["St. James Place", [], 0, -1, (14, 2), s.COLORS["ORANGE"]],
        17: ["Community Chest", [], 0, -3, (11, 2), s.COLORS["COMMUNITY"]],
        18: ["Tennessee Avenue", [], 0, -1, (8, 2), s.COLORS["ORANGE"]],
        19: ["New York Avenue", [], 0, -1, (5, 2), s.COLORS["ORANGE"]],
        20: ["Free Parking", [], 0, -8, (2, 2), s.COLORS["LIGHTGRAY"]],
        21: ["Kentucky Avenue", [], 0, -1, (2, 9), s.COLORS["RED"]],
        22: ["Chance", [], 0, -4, (2, 16), s.COLORS["CHANCE"]],
        23: ["Indiana Avenue", [], 0, -1, (2, 23), s.COLORS["RED"]],
        24: ["Illinois Avenue", [], 0, -1, (2, 30), s.COLORS["RED"]],
        25: ["B&O Railroad", [], 0, -1, (2, 37), s.COLORS["LIGHTBLACK"]],
        26: ["Atlantic Avenue", [], 0, -1, (2, 44), s.COLORS["YELLOW"]],
        27: ["Ventnor Avenue", [], 0, -1, (2, 51), s.COLORS["YELLOW"]],
        28: ["Water Works", [], 0, -1, (2, 58), s.COLORS["CYAN"]],
        29: ["Marvin Gardens", [], 0, -1, (2, 65), s.COLORS["YELLOW"]],
        30: ["Go To Jail", [], 0, -7, (2, 72), s.COLORS["LIGHTGRAY"]],
        31: ["Pacific Avenue", [], 0, -1, (5, 72), s.COLORS["GREEN"]],
        32: ["North Carolina Avenue", [], 0, -1, (8, 72), s.COLORS["GREEN"]],
        33: ["Community Chest", [], 0, -3, (11, 72), s.COLORS["COMMUNITY"]],
        34: ["Pennsylvania Avenue", [], 0, -1, (14, 72), s.COLORS["GREEN"]],
        35: ["Short Line", [], 0, -1, (17, 72), s.COLORS["LIGHTBLACK"]],
        36: ["Chance", [], 0, -4, (20, 72), s.COLORS["CHANCE"]],
        37: ["Park Place", [], 0, -1, (23, 72), s.COLORS["BLUE"]],
        38: ["Luxury Tax", [], 0, -9, (26, 72), s.COLORS["LIGHTGRAY"]],
        39: ["Boardwalk", [], 0, -1, (29, 72), s.COLORS["BLUE"]]
    }
        """Dictionary of Monopoly locations\n
        @locations: {int: [str, list, int, bool]}\n
        key: number
        value: [name, players, number of houses [0-4], owned, (x,y) coordinates on gameboard, color code]"""
        self.deeds = {"Mediterranean Avenue": (60, 50, 2, 10, 30, 90, 160, 250, 30),
                    "Baltic Avenue":          (60, 50, 4, 20, 60, 180, 320, 450, 30),
                    "Oriental Avenue":        (100, 50, 6, 30, 90, 270, 400, 550, 50),
                    "Vermont Avenue":         (100, 50, 6, 30, 90, 270, 400, 550, 50),
                    "Connecticut Avenue":      (120, 50, 8, 40, 100, 300, 450, 600, 60),
                    "St. Charles Place":      (140, 100, 10, 50, 150, 450, 625, 750, 70),
                    "States Avenue":          (140, 100, 10, 50, 150, 450, 625, 750, 70),
                    "Virginia Avenue":        (160, 100, 12, 60, 180, 500, 700, 900, 80),
                    "St. James Place":        (180, 100, 14, 70, 200, 550, 750, 950, 90),
                    "Tennessee Avenue":       (180, 100, 14, 70, 200, 550, 750, 950, 90),
                    "New York Avenue":        (200, 100, 16, 80, 220, 600, 800, 1000, 100),
                    "Kentucky Avenue":        (220, 150, 18, 90, 250, 700, 875, 1050, 110),
                    "Indiana Avenue":         (220, 150, 18, 90, 250, 700, 875, 1050, 110),
                    "Illinois Avenue":        (240, 150, 20, 100, 300, 750, 925, 1100, 120),
                    "Atlantic Avenue":        (260, 150, 22, 110, 330, 800, 975, 1150, 130),
                    "Ventnor Avenue":         (260, 150, 22, 110, 330, 800, 975, 1150, 130),
                    "Marvin Gardens":         (280, 150, 24, 120, 360, 850, 1025, 1200, 140),
                    "Pacific Avenue":         (300, 200, 26, 130, 390, 900, 1100, 1275, 150),
                    "North Carolina Avenue":  (300, 200, 26, 130, 390, 900, 1100, 1275, 150),
                    "Pennsylvania Avenue":    (320, 200, 28, 150, 450, 1000, 1200, 1400, 160),
                    "Park Place":             (350, 200, 35, 175, 500, 1100, 1300, 1500, 175),
                    "Boardwalk":              (400, 200, 50, 200, 600, 1400, 1700, 2000, 200)
                    }
        """dict[str, tuple]: properties
        Key: title
        Value: tuple with values as follows:\n
            0 - Purchase Price\n
            1 - Price Per House\n
            2 - Rent\n
            3 - Rent w 1 House\n
            4 - Rent w 2 House\n
            5 - Rent w 3 House\n
            6 - Rent w 4 House\n
            7 - Rent w Hotel\n
            8 - Mortgage Value\n
        """
        """
        @RR_VALUES constants for the purchase, rent, mortgage, and color code values of the railroads
        """
        RR_VALUES = [200, 25, 50, 100, 200, 100]
        """
            Key: title
            Value: tuple with values as follows:
                0 - Purchase Price
                1 - Price / multiplier with 1 property 
                2 - Price / multiplier with 2 properties
                3 - Price with 3 railroads (or -1 if utility)
                4 - Price with 4 railroads (or -1 if utility)
                5 - Mortgage Value
        """
        self.special_deeds = {
                "Reading Railroad":       ([value for value in RR_VALUES]),
                "Pennsylvania Railroad":  ([value for value in RR_VALUES]),
                "B&O Railroad":           ([value for value in RR_VALUES]),
                "Short Line":             ([value for value in RR_VALUES]),
                "Electric Company":       (150, 4, 10, -1, -1, 75),
                "Water Works":            (150, 4, 10, -1, -1, 75)
                }

    def update_location(self, player:Player, roll: int, new = None) -> None:
        """
        Update location with player\n
        @location: int\n
        @player: Player object\n
        """
        if(new == None):
            new_location = player.location + roll
            if new_location > 39:
                new_location -= 40
                player.receive(200)
                update_history(f"Player {player.order} passed Go and received $200")
            self.locations[player.location][1].remove(player.order)
            self.locations[new_location][1].append(player.order)
            player.location = new_location

            if(roll == -1):
                self.locations[player.location][1].remove(player.order)
                self.locations[10][1].append(player.order)
                player.location = 10
        else: # Used mostly for chance and community chest cards (roll = old location, new = new location)
            if roll > new and new != 10 and new != player.location-3:
                player.receive(200)
            self.locations[roll][1].remove(player.order)
            self.locations[new][1].append(player.order)
            player.location = new
        
    def current_location(self, player:Player) -> int:
        """
        Return current location\n
        @player: Player object\n
        """
        return player.location

class Cards:
    """
    Cards class for Monopoly game\n
    Contains card data.\n
    """
    def __init__(self) -> None:
        self.chance = s.get_graphics().get('chance cards text').split("\n")
        self.community_chest = s.get_graphics().get('community chest text').split("\n")
        random.shuffle(self.chance)
        random.shuffle(self.community_chest)
    def draw_chance(self, p: Player) -> str:
        """
        Draw chance card\n
        """
        self.chance.append(self.chance.pop(0))

        card_number = int(self.chance[-1].split(".")[0])
        match card_number:
            case 1: 
                board.update_location(p, p.location, 39)
            case 2: 
                board.update_location(p, p.location, 0)
            case 3:
                board.update_location(p, p.location, 24)
            case 4: 
                board.update_location(p, p.location, 11)
            case 5:
                if p.location < 5 or p.location > 35:
                    board.update_location(p, p.location, 5)
                elif p.location < 15:
                    board.update_location(p, p.location, 15)
                elif p.location < 25:
                    board.update_location(p, p.location, 25)
                else:
                    board.update_location(p, p.location, 35)
            case 6: 
                if p.location < 5 or p.location > 35:
                    board.update_location(p, p.location, 5)
                elif p.location < 15:
                    board.update_location(p, p.location, 15)
                elif p.location < 25:
                    board.update_location(p, p.location, 25)
                else:
                    board.update_location(p, p.location, 35)
            case 7: 
                if p.location < 12 or p.location > 28:
                    board.update_location(p, p.location, 12)
                else:
                    board.update_location(p, p.location, 28)
            case 8: 
                p.receive(50)
            case 9: 
                p.jailcards += 1
            case 10: 
                board.update_location(p, p.location, p.location - 3)
            case 11: 
                p.jail = True
                board.update_location(p, p.location, 10)
            case 12: 
                # @TODO housing repairs, implement!
                pass
            case 13:
                p.pay(15)
            case 14:
                board.update_location(p, p.location, 5)
            case 15:
                # @TODO: Implement chairman of the board
                pass
            case 16: 
                p.receive(150)
        return self.chance[-1]
    def draw_community_chest(self, p: Player) -> str:
        """
        Draw community chest card\n
        """
        self.community_chest.append(self.community_chest.pop(0))

        card_number = int(self.community_chest[-1].split(".")[0])
        match card_number:
            case 1:
                board.update_location(p, p.location, 0)
            case 2:
                p.receive(200)
            case 3:
                p.pay(50)
            case 4: 
                p.receive(50)
            case 5:
                p.jailcards += 1
            case 6:
                board.update_location(p, p.location, 10)
                p.jail = True
            case 7:
                p.receive(100)
            case 8:
                p.receive(20)
            case 9:
                # Other players must pay $10, implement!
                pass
            case 10:
                p.receive(100)
            case 11:
                p.pay(100)
            case 12:
                p.pay(50)
            case 13:
                p.receive(25)
            case 14: 
                # Street repair, implement!
                pass
            case 15:
                p.receive(10)
            case 16:
                p.receive(100)
        return self.community_chest[-1]

def refresh_board():
    """
    Refresh the gameboard\n
    """
    print(Style.RESET_ALL + "\033[0;0H", end="")
    print(gameboard)
    for i in range(40): 
        # This loop paints the properties on the board with respective color schemes
        color = board.locations[i][5]
        backcolor = board.locations[i][5].replace("38", "48")
        print(Back.BLACK + color + f"\033[{board.locations[i][4][0]};{board.locations[i][4][1]}H{i}" + backcolor + " " * (4 + (1 if i < 10 else 0)))
        
        if(board.locations[i][3] != -1): # If owned
            print(end=Style.RESET_ALL)
            color = f"\033[38;5;{board.locations[i][3]+1}m"
            print(f"\033[{board.locations[i][4][0]+2};{board.locations[i][4][1]}H" + color + "▀")

        if(board.locations[i][3] == -3): # If community chest
            print(end=Style.RESET_ALL)
            print(f"\033[{board.locations[i][4][0] + 1};{board.locations[i][4][1]}H" + s.COLORS["COMMUNITY"] + "█" * 6)
            print(f"\033[{board.locations[i][4][0] + 2};{board.locations[i][4][1]}H" + s.COLORS["COMMUNITY"] + "▀" * 6)

        if(board.locations[i][3] == -4): # If chance
            print(end=Style.RESET_ALL)
            print(f"\033[{board.locations[i][4][0] + 1};{board.locations[i][4][1]}H" + s.COLORS["CHANCE"] + "█" * 6)
            print(f"\033[{board.locations[i][4][0] + 2};{board.locations[i][4][1]}H" + s.COLORS["CHANCE"] + "▀" * 6)
        
        if(board.locations[i][2] > 0): # If there are houses
            print(end=Style.RESET_ALL)
            print(f"\033[{board.locations[i][4][0]+2};{board.locations[i][4][1]+1}H" + s.COLORS["GREEN"] + "▀" * (board.locations[i][2]))
        
        if(board.locations[i][2] == 5): # If there is a hotel
            print(end=Style.RESET_ALL)
            print(f"\033[{board.locations[i][4][0]+2};{board.locations[i][4][1]+5}H" + s.COLORS["RED"] + "▀")

        if(board.locations[i][3] == -2): # If mortgaged
            print(end=Style.RESET_ALL)
            print(f"\033[{board.locations[i][4][0]+2};{board.locations[i][4][1]}H" + s.COLORS["LIGHTGRAY"].replace("38", "48") + "M")

    print(end=Style.RESET_ALL)

    for i in range(num_players):
        color = f"\033[38;5;{i+1}m" # define player colors
        token = "◙"
        print(color + f"\033[{board.locations[players[i].location][4][0]+1};{board.locations[players[i].location][4][1]+1+i}H{token}")
    
    print(end=Style.RESET_ALL)

def print_commands():
    """
    Print commands\n
    """
    commandsinfo = s.get_graphics().get('commands').split("\n")
    for i in range(len(commandsinfo)):
        for j in range(len(commandsinfo[i])):
            print(f"\033[{34+i};79H" + commandsinfo[i][:j], end="")

history = []
def update_history(message: str):
    """
    Update the history\n
    Text added here needs to be a maximum of 40 characters, or wrap around\n
    Split the text into multiple lines (multiple entries to history variable)\n
    """
    if len(message) > 40:
        while len(message) > 40:
            history.append(message[:40] + " " * (40 - len(message)))
            message = message[40:]
    history.append(message + " " * (40 - len(message)))
    if len(history) > 31:
        while(len(history) > 31):
            history.pop(0)
    refresh_h_and_s()

status = []
def update_status(p: Player, update: str, status: list = status):
    """
    Update the status\n
    """
    # Property status update (list all properties of player)
    status.clear()
    if(update == "properties"):
        status.append(s.COLORS[f"Player{p.order}"] + f"{p} has properties: " + Style.RESET_ALL)
        for i in range(len(p.properties)):
            status.append(f"{p.properties[i]}: {board.locations[p.properties[i]][0]}")
    if(update == "deed"):
        propertyid = input("What property to view? Enter property #")
        try:
            propertyid = int(propertyid)
            if board.locations[propertyid][0] in board.deeds or board.locations[propertyid][0] in board.special_deeds:
                if(board.locations[propertyid][3] != -1):
                    status.append(f"Current owner: " + s.COLORS[f"Player{board.locations[propertyid][3]}"] + f"Player{board.locations[propertyid][3]}" + Style.RESET_ALL)
                    status.append(f"Houses: {board.locations[propertyid][2]}")
            if(board.locations[propertyid][0] in board.deeds):
                deed = board.deeds.get(board.locations[propertyid][0])
                status.append(f"{board.locations[propertyid][5]}=== {board.locations[propertyid][0]} ===")
                status.append(f"Purchase Price: {deed[0]}")
                status.append(f"Price Per House: {deed[1]}")
                status.append(f"Rent: {deed[2]}")
                status.append(f"Rent w 1 house: {deed[3]}")
                status.append(f"Rent w 2 houses: {deed[4]}")
                status.append(f"Rent w 3 houses: {deed[5]}")
                status.append(f"Rent w 4 houses: {deed[6]}")
                status.append(f"Rent w hotel: {deed[7]}")
                status.append(f"Mortgage Value: {deed[8]}")
            elif board.locations[propertyid][0] in board.special_deeds:
                deed = board.special_deeds.get(board.locations[propertyid][0])
                status.append(f"{board.locations[propertyid][5]}=== {board.locations[propertyid][0]} ===")
                status.append(f"Purchase Price: {deed[0]}")
                status.append(f"Rent (or mltplr) with 1 owned: {deed[1]}")
                status.append(f"Rent (or mltplr) with 2 owned: {deed[2]}")
                status.append(f"Rent with 3 locations owned: {deed[3]}")
                status.append(f"Rent with 4 locations owned: {deed[4]}")
                status.append(f"Mortgage Value: {deed[5]}")
            else:
                raise ValueError
        except ValueError:
            print(f"Invalid input. Please enter a # for a property.")
    refresh_h_and_s()

border = s.get_graphics().get('history and status')
border = border.split("\n")
def refresh_h_and_s():
    """
    Refresh the history, status, and leaderboard\n
    """
    # Refresh history
    for i in range(len(border)):
        print(f"\033[{i};79H", end="")
        if(len(history) - i<= 0):
            for j in range(len(border[i])):
                print(border[i][j], end="")
    for i in range(len(history)):
        print(f"\033[{i+4};81H" + history[i] if i < len(history) else "", end=Style.RESET_ALL)
    
    # Refresh status
    for i in range(len(status)):
        print(f"\033[{i+4};122H" + status[i] if i < len(status) else "")
    print(Style.RESET_ALL, end="")

    # Refresh leaderboard
    sorted_players = sorted(players, key=lambda x: x.cash, reverse=True)
    for i in range(len(sorted_players)):
        if(sorted_players[i].order != -1):
            print(s.COLORS[f"Player{sorted_players[i].order}"] + f"\033[{31+i};122H{sorted_players[i].order} - ${sorted_players[i].cash}", end=Style.RESET_ALL)

def buy_logic():
    CL = players[turn].location
    input("\033[37;0HBuy?") # Add buy logic
    if(board.locations[CL][0] in board.deeds):
        price = board.deeds[board.locations[CL][0]][0]
        if(players[turn].cash > price):
            players[turn].buy(CL)
            board.locations[CL][3] = turn
            update_history(f"Player {turn} bought {board.locations[CL][0]} for ${price}")
        else:
            update_history(f"Player {turn} did not buy {board.locations[CL][0]}")
    else:
        price = board.special_deeds[board.locations[CL][0]][0]
        if(players[turn].cash > price):
            players[turn].buy(CL)
            board.locations[CL][3] = turn
            update_history(f"Player {turn} bought {board.locations[CL][0]} for ${price}")
        else:
            update_history(f"Player {turn} did not buy {board.locations[CL][0]}")

def housing_logic(p: Player):
    update_status(p, "properties")
    propertyid = input("What property do you want to build on? Enter property # or 'e' to exit."+
                       "\033[40;0H" + " " * 78+"\033[41;0H" + " " * 78+"\033[40;0H")
    flag = True
    exit = False
    try:   
        if propertyid == 'e':
            exit = True
        else:
            propertyid =  int(propertyid)
    except ValueError: ###AHHHHHHHH clean me please
        print(f"\033[42;0" + s.COLORS["RED"] + f"Invalid input, please enter a number in {p.properties}", end=Style.RESET_ALL)
        flag = False
    if flag and not exit:
        if not propertyid in p.properties:
            print("You do not own this property!")
        else: 
            family = board.locations[propertyid][5]
            if family == s.COLORS["CYAN"] or family == s.COLORS["LIGHTBLACK"] or board.locations[propertyid][0].startswith("Electric"):
                print("This property cannot be improved.")
                flag = False
            if flag: 
                for i in range(propertyid-3 if propertyid > 3 else 0, propertyid+5 if propertyid < 35 else 39): # check only a few properties around for efficiency
                    if board.locations[i][5] == family:
                        if not i in p.properties:
                            print("You do not own a monopoly on these properties!")
                            flag = False
            if flag:
                cost = 0
                if flag:
                    if 0 < propertyid < 10:
                        cost = 50
                    elif 10 < propertyid < 20:
                        cost = 100
                    elif 20 < propertyid < 30:
                        cost = 150
                    elif 30 < propertyid < 40:
                        cost = 200
                    max = 5 - board.locations[propertyid][2]
                    houses = input(f"Cost of housing is ${cost}. How many houses would you like to buy? (Max {max}/min 0)")
                    try:
                        houses = int(houses)
                        if(0 <= houses <= max):
                            p.cash -= cost * houses
                            update_history(f"{p} bought {houses} houses on {board.locations[propertyid][0]}!")
                            board.locations[propertyid][2] += houses
                            refresh_board()
                        else:
                            raise ValueError
                    except ValueError:
                        print(f"Invalid input. Please enter a number 0-{max}")
    if not exit:
        housing_logic(p)

def mortgage_logic():
    input("\033[37;0HWhat property to mortgage?") 

from datetime import datetime
def log_error(error_message: str) -> None:
    """
    Log error message to errorlog.txt\n
    """
    with open("errorlog.txt", "a") as f:
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"{formatted_datetime}\n{error_message}\n")

def make_fullscreen():
    current_os = platform.system()

    if current_os == "Windows":
        # Maximize terminal on Windows
        user32 = ctypes.WinDLL("user32")
        SW_MAXIMIZE = 3
        hWnd = user32.GetForegroundWindow()
        user32.ShowWindow(hWnd, SW_MAXIMIZE)

    elif current_os == "Linux" or current_os == "Darwin":
        # Maximize terminal on Linux/macOS
        os.system("printf '\033[9;1t'")
    else:
        print(f"Fullscreen not supported for OS: {current_os}")

make_fullscreen()
print()
screen_test = input("Please make sure the terminal in full screen mode. Press enter to continue.")

# CASH = input("Starting cash?")
# num_players = int(input("Number players?"))
CASH = 2000
num_players = 4
bankrupts = 0

players = []
for i in range(num_players):
    players.append(Player(CASH, i))

turn = 0

board = Board(num_players)
decks = Cards()

import style as s

gameboard = s.get_graphics().get('gameboard')
os.system('cls' if os.name == 'nt' else 'clear')
print(Fore.WHITE + "\033[0;0H", end="")
print(gameboard)

def unittest():
    players[1].buy(1)
    players[1].buy(3)
    players[2].buy(5)
    players[2].buy(15)
    players[2].buy(25)
    players[2].buy(35)

unittest()

while(True):
    refresh_board()      
    if(players[turn].order != -1): # If player is not bankrupt
        update_history(s.COLORS[f"Player{turn}"] + f"Player {turn}'s turn")
        print_commands()
        input("\033[36;0HRoll dice?")
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        update_history(f"Player {turn} rolled {die1} and {die2}")

        board.update_location(players[turn], die1 + die2)
        update_history(f"Player {turn} landed on {board.locations[players[turn].location][0]}")
        refresh_board()
        if board.locations[players[turn].location][3] < 0:
            match board.locations[players[turn].location][3]:
                case -1: #unowned
                    buy_logic()
                case -2: #mortgaged
                    pass
                case -3: #community chest
                    card = decks.draw_community_chest(players[turn])
                    update_history(f"Player {turn} drew a Community Chest card! {card}")
                case -4: #chance
                    card = decks.draw_chance(players[turn])
                    update_history(f"Player {turn} drew a Chance card! {card}")
                    if(board.locations[players[turn].location][3] == -1):
                        buy_logic()
                    if(board.locations[players[turn].location][3] == -5):
                        players[turn].pay(200)
                        update_history(f"Player {turn} paid income tax ($200)")
                case -5: #income tax
                    players[turn].pay(200)
                    update_history(f"Player {turn} paid income tax ($200)")
                case -6: #jail
                    pass
                case -7: #go to jail
                    players[turn].jail = True
                    board.update_location(players[turn], -1)
                case -8: #free parking
                    pass
                case -9: #luxury tax
                    players[turn].pay(100)
                    update_history(f"Player {turn} paid luxury tax ($100)")
                case -10: #go
                    pass
        elif board.locations[players[turn].location][3] != players[turn].order:
            # Pay another player rent
            cl = players[turn].location
            rent = board.deeds[board.locations[cl][0]][2 + board.locations[cl][2]] if board.locations[cl][0] in board.deeds else board.special_deeds[board.locations[cl][0]][board.locations[cl][2]]
            if rent == 4 and board.locations[cl][0] in board.special_deeds:
                rent = 4 * (die1 + die2)
            elif rent == 10 and board.locations[cl][0] in board.special_deeds:
                rent = 10 * (die1 + die2)
            players[turn].pay(rent)
            players[board.locations[cl][3]].receive(rent)
            update_history(f"{players[turn]} paid ${rent} to Player {board.locations[cl][3]}")
        refresh_board()
        if die1 == die2:
            update_history(f"{players[turn]} rolled doubles! Roll again.")
            # @TODO implement rolling doubles
        if(players[turn].cash > 0):
            choice = input("\033[38;0He to end turn, p to manage properties, d to view a deed?")
            while(choice != 'e'): # @TODO remove soon! players should not be able to do these actions during gameboard screen 
                if choice == "e":
                    pass
                elif choice == "p":
                    housing_logic(players[turn])
                elif choice == "d":
                    update_status(players[turn], "deed")
                else:
                    print("Invalid option!")
                choice = input("\033[38;0H'e' to end turn, p to manage properties, ?")
            update_history(f"{players[turn]} ended their turn.")
        else:
            update_history(f"Player {turn} is in debt. Resolve debts before ending turn.")
            option = input("\033[38;0HResolve debts before ending turn.").lower().strip()
            if(option == "b"): # Declare bankruptcy
                update_history(f"Player {turn} declared bankruptcy.")
                players[turn].order = -1
            elif(option == "m"): # Mortgage properties
                pass
            elif(option == "s"): # Sell houses/hotels
                housing_logic()

            # TODO! For now, just declare bankruptcy. Player should NOT, by default, be able to by pressing "enter"

            else:
                update_history(f"Player {turn} declared bankruptcy.")
                players[turn].order = -1
            # Need to fix all this sometime erghhghh
            bankrupts += 1

    # Wipe the bottom of the screen (input area)
    print("\033[36;0H" + " " * 76)
    print("\033[37;0H" + " " * 76)
    print("\033[38;0H" + " " * 76)
    print("\033[39;0H" + " " * 76)
    print("\033[40;0H" + " " * 76)
    print("\033[41;0H" + " " * 76)
    print("\033[42;0H" + " " * 76)
    print("\033[43;0H" + " " * 76)
    print("\033[44;0H" + " " * 76)

    if(bankrupts == num_players - 1):
        break

    turn = (turn + 1)%num_players

for index, player in enumerate(players):
    if player.order != -1:
        update_history(s.COLORS[f"Player{index}"] + f"Player {index} wins!")
        break
print("\033[40;0H", end="")