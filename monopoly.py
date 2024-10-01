# Monopoly game is played on Banker's terminal. 
import style as s
from style import COLORS
import random
import board
import cards

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
        board.locations[location][3] = self.order
        if board.locations[location][0] in board.special_deeds:

            if location == 5 or location == 15 or location == 25 or location == 35: # railroad
                owned_rails = [k for k in range(5, 36, 10) if board.locations[k][3] == self.order]
                for k in owned_rails:
                    board.locations[k][2] = len(owned_rails)
            
            elif location == 12: # electric company, check if water works is owned
                if board.locations[28][3] == self.order:
                    board.locations[12][2] = 2
                    board.locations[28][2] = 2
                else: board.locations[12][2] = 1
            
            elif location == 28: # water works, check if electric company is owned
                if board.locations[12][3] == self.order:
                    board.locations[28][2] = 2
                    board.locations[12][2] = 2
                else: board.locations[28][2] = 1
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


def refresh_board():
    """
    Refresh the gameboard\n
    """
    print(COLORS.RESET + "\033[0;0H", end="")
    print(gameboard)
    for i in range(40): 
        # This loop paints the properties on the board with respective color schemes
        color = board.locations[i][5]
        backcolor = board.locations[i][5].replace("38", "48")
        print(COLORS.backBLACK + color + f"\033[{board.locations[i][4][0]};{board.locations[i][4][1]}H{i}" + backcolor + " " * (4 + (1 if i < 10 else 0)))
        
        if(board.locations[i][3] != -1): # If owned
            print(end=COLORS.RESET)
            color = f"\033[38;5;{board.locations[i][3]+1}m"
            print(f"\033[{board.locations[i][4][0]+2};{board.locations[i][4][1]}H" + color + "▀")

        if(board.locations[i][3] == -3): # If community chest
            print(end=COLORS.RESET)
            print(f"\033[{board.locations[i][4][0] + 1};{board.locations[i][4][1]}H" + COLORS.COMMUNITY + "█" * 6)
            print(f"\033[{board.locations[i][4][0] + 2};{board.locations[i][4][1]}H" + COLORS.COMMUNITY + "▀" * 6)

        if(board.locations[i][3] == -4): # If chance
            print(end=COLORS.RESET)
            print(f"\033[{board.locations[i][4][0] + 1};{board.locations[i][4][1]}H" + COLORS.CHANCE + "█" * 6)
            print(f"\033[{board.locations[i][4][0] + 2};{board.locations[i][4][1]}H" + COLORS.CHANCE + "▀" * 6)
        
        if(board.locations[i][2] > 0): # If there are houses
            print(end=COLORS.RESET)
            print(f"\033[{board.locations[i][4][0]+2};{board.locations[i][4][1]+1}H" + COLORS.GREEN + "▀" * (board.locations[i][2]))
        
        if(board.locations[i][2] == 5): # If there is a hotel
            print(end=COLORS.RESET)
            print(f"\033[{board.locations[i][4][0]+2};{board.locations[i][4][1]+5}H" + COLORS.RED + "▀")

        if(board.locations[i][3] == -2): # If mortgaged
            print(end=COLORS.RESET)
            print(f"\033[{board.locations[i][4][0]+2};{board.locations[i][4][1]}H" + COLORS.backLIGHTGRAY + "M")

    print(end=COLORS.RESET)

    for i in range(num_players):
        color = COLORS.playerColors[i]
        token = "◙"
        print(color + f"\033[{board.locations[players[i].location][4][0]+1};{board.locations[players[i].location][4][1]+1+i}H{token}")
    
    print(end=COLORS.RESET)

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
        color = COLORS.playerColors[p.order]
        status.append(color + f"{p} has properties: " + COLORS.RESET)
        for i in range(len(p.properties)):
            status.append(f"{p.properties[i]}: {board.locations[p.properties[i]][0]}")
    if(update == "deed"):
        propertyid = input("What property to view? Enter property #")
        try:
            propertyid = int(propertyid)
            if board.locations[propertyid][0] in board.deeds or board.locations[propertyid][0] in board.special_deeds:
                if(board.locations[propertyid][3] != -1):
                    color = COLORS.playerColors[board.locations[propertyid][3]]
                    status.append(f"Current owner: " + color + f"Player{board.locations[propertyid][3]}" + COLORS.RESET)
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
        print(f"\033[{i+4};81H" + history[i] if i < len(history) else "", end=COLORS.RESET)
    
    # Refresh status
    for i in range(len(status)):
        print(f"\033[{i+4};122H" + status[i] if i < len(status) else "")
    print(COLORS.RESET, end="")

    # Refresh leaderboard
    sorted_players = sorted(players, key=lambda x: x.cash, reverse=True)
    for i in range(len(sorted_players)):
        if(sorted_players[i].order != -1):
            color = COLORS.playerColors[sorted_players[i].order]
            print(color + f"\033[{31+i};122H{sorted_players[i].order} - ${sorted_players[i].cash}", end=COLORS.RESET)

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
        print(f"\033[42;0" + COLORS.RED + f"Invalid input, please enter a number in {p.properties}", end=COLORS.RESET)
        flag = False
    if flag and not exit:
        if not propertyid in p.properties:
            print("You do not own this property!")
        else: 
            family = board.locations[propertyid][5]
            if family == COLORS.CYAN or family == COLORS.LIGHTBLACK or board.locations[propertyid][0].startswith("Electric"):
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

# CASH = input("Starting cash?")
# num_players = int(input("Number players?"))
CASH = 2000
num_players = 4
bankrupts = 0

players = []
for i in range(num_players):
    players.append(Player(CASH, i))

turn = 0

board = board.Board(num_players)
decks = cards.Cards()

import style as s
import os
gameboard = s.get_graphics().get('gameboard')
os.system('cls' if os.name == 'nt' else 'clear')
print(COLORS.WHITE + "\033[0;0H", end="")
print(gameboard)

def unittest():
    players[1].buy(1)
    players[1].buy(3)
    players[2].buy(5)
    players[2].buy(15)
    players[2].buy(25)
    players[2].buy(35)
    players[3].buy(12)
    players[3].buy(28)

unittest()
#wipes the bottom of the screen where the player does all of their input
def bottom_screen_wipe():
    print("\033[36;0H" + " " * 76)
    print("\033[37;0H" + " " * 76)
    print("\033[38;0H" + " " * 76)
    print("\033[39;0H" + " " * 76)
    print("\033[40;0H" + " " * 76)
    print("\033[41;0H" + " " * 76)
    print("\033[42;0H" + " " * 76)
    print("\033[43;0H" + " " * 76)
    print("\033[44;0H" + " " * 76)

#Rolls the dice and returns them for the player as a tuple
def roll():
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    return(die1,die2)
#The function that handles the players 
#second and third correspond to if its the players second or third consecutive turn, they are bools
def player_roll(num_rolls):
    print_commands()
    bottom_screen_wipe()   
    if(players[turn].order != -1): # If player is not bankrupt
        player_color = COLORS.playerColors[turn]
        update_history(player_color + f"Player {turn}'s turn")
        print_commands()
        input("\033[36;0HRoll dice?")
        dice = roll()
        bottom_screen_wipe()
        update_history(f"Player {turn} rolled {dice[0]} and {dice[1]}")

        if dice[0] == dice[1]:
            if  num_rolls == 1:
                update_history(f"{players[turn]} rolled doubles! Roll again.")
            
            elif num_rolls == 2:
                update_history(f"{players[turn]} rolled doubles!(X2) Roll again.")
                
            elif num_rolls == 3:
                update_history(f"Player {turn} rolled doubles three times\n in a row!")
                update_history(f"Player {turn} is going to jail!")
                players[turn].jail = True
                board.update_location(players[turn], -1)
        refresh_board()
        #if player rolled their third double they will be in jail and their location doesn't update
        if players[turn].jail == False:
            board.update_location(players[turn], dice[0] + dice[1])
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
                rent = 4 * (dice[0] + dice[1])
            elif rent == 10 and board.locations[cl][0] in board.special_deeds:
                rent = 10 * (dice[0] + dice[1])
            players[turn].pay(rent)
            players[board.locations[cl][3]].receive(rent)
            update_history(f"{players[turn]} paid ${rent} to Player {board.locations[cl][3]}")
        refresh_board()
        #checks if player rolled a double, and has them roll again if they did.
        if dice[0] == dice[1] and players[turn].jail == False:
            num_rolls +=1
            player_roll(num_rolls)

while(True):
    # First time the player who's turn it is rolls their dice
    #if they roll a double the function calls itself and updates its their number of consecutive rolls
    player_roll(num_rolls=1)
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
    bottom_screen_wipe()

    if(bankrupts == num_players - 1):
        break

    turn = (turn + 1)%num_players

for index, player in enumerate(players):
    if player.order != -1:
        color = COLORS.playerColors[index]
        update_history(color + f"Player {index} wins!")
        break
print("\033[40;0H", end="")