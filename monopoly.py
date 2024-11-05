# Monopoly game is played on Banker's terminal. 
import style as s
from style import COLORS
import random
import os

from properties import Property
from cards import Cards
from board import Board
from player_class import Player
import screenspace as ss

def refresh_board():
    """
    Refresh the gameboard\n
    """
    print(COLORS.RESET + "\033[0;0H", end="")
    print(gameboard)
    for i in range(40): 
        # This loop paints the properties on the board with respective color schemes
        color = board.locations[i].color
        backcolor = board.locations[i].color.replace("38", "48")
        print(COLORS.backBLACK + color + f"\033[{board.locations[i].x};{board.locations[i].y}H{i}" + backcolor + " " * (4 + (1 if i < 10 else 0)))
        
        if(board.locations[i].owner != -1): # If owned
            print(end=COLORS.RESET)
            color = f"\033[38;5;{board.locations[i].owner+1}m"
            print(f"\033[{board.locations[i].x+2};{board.locations[i].y}H" + color + "▀")

        if(board.locations[i].owner == -3): # If community chest
            print(end=COLORS.RESET)
            print(f"\033[{board.locations[i].x + 1};{board.locations[i].y}H" + COLORS.COMMUNITY + "█" * 6)
            print(f"\033[{board.locations[i].x + 2};{board.locations[i].y}H" + COLORS.COMMUNITY + "▀" * 6)

        if(board.locations[i].owner == -4): # If chance
            print(end=COLORS.RESET)
            print(f"\033[{board.locations[i].x + 1};{board.locations[i].y}H" + COLORS.CHANCE + "█" * 6)
            print(f"\033[{board.locations[i].x + 2};{board.locations[i].y}H" + COLORS.CHANCE + "▀" * 6)
        
        if(board.locations[i].houses > 0): # If there are houses
            print(end=COLORS.RESET)
            print(f"\033[{board.locations[i].x+2};{board.locations[i].y+1}H" + COLORS.GREEN + "▀" * (board.locations[i].houses))
        
        if(board.locations[i].houses == 5): # If there is a hotel
            print(end=COLORS.RESET)
            print(f"\033[{board.locations[i].x+2};{board.locations[i].y+5}H" + COLORS.RED + "▀")

        if(board.locations[i].owner == -2): # If mortgaged
            print(end=COLORS.RESET)
            print(f"\033[{board.locations[i].x+2};{board.locations[i].y}H" + COLORS.backLIGHTGRAY + "M")

    print(end=COLORS.RESET)

    for i in range(num_players):
        color = COLORS.playerColors[i]
        token = "◙"
        print(color + f"\033[{board.locations[players[i].location].x+1};{board.locations[players[i].location].y+1+i}H{token}")
    
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
    if "[38;5" in message:
        if(((40 - (len(message) - 9)) * 2) == 0):
            history.append(message[:9] + "─" * ((40 - (len(message) - 9)) // 2) + message[9:] + "─" * ((40 - (len(message) - 9)) // 2))
        else:
            history.append(message[:9] + "─" * ((40 - (len(message) - 9)) // 2) + message[9:] + "─" * ((39 - (len(message) - 9)) // 2))
    else:
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
        status.append(color + f"{p.name} has properties: " + COLORS.RESET)
        for i in range(len(p.properties)):
            status.append(f"{p.properties[i]}: {board.locations[p.properties[i]].name}")
    if(update == "deed"):
        propertyid = input("What property to view? Enter property #")
        try:
            location = board.locations[int(propertyid)]
            if location.owner > -1: # if the location is owned
                color = COLORS.playerColors[location.owner]
                status.append(f"Current owner: " + color + f"Player{location.owner}" + COLORS.RESET)
                status.append(f"Houses: {location.houses}")
            if(location.rent != 0): # if location could be owned and is not a utility or railroad
                status.append(f"{location.color}=== {location.name} ===")
                status.append(f"Purchase Price: {location.purchasePrice}")
                status.append(f"Price Per House: {location.housePrice}")
                status.append(f"Rent: {location.rent}")
                status.append(f"Rent w 1 house: {location.rent1H}")
                status.append(f"Rent w 2 houses: {location.rent2H}")
                status.append(f"Rent w 3 houses: {location.rent3H}")
                status.append(f"Rent w 4 houses: {location.rent4H}")
                status.append(f"Rent w hotel: {location.rentHotel}")
                status.append(f"Mortgage Value: {location.mortgage}")
            elif (location.owner >= -2 and location.rent == 0): # if is a railroad or utility
                status.append(f"{location.color}=== {location.name} ===")
                status.append(f"Purchase Price: {location.purchasePrice}")
                status.append(f"Rent (or mltplr) with 1 owned: {location.rent1H}")
                status.append(f"Rent (or mltplr) with 2 owned: {location.rent2H}")
                status.append(f"Rent with 3 locations owned: {location.rent3H}")
                status.append(f"Rent with 4 locations owned: {location.rent4H}")
                status.append(f"Mortgage Value: {location.mortgage}")
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
     # Add buy logic
    if(board.locations[CL].purchasePrice != 0 and input(f"\033[37;0HBuy {board.locations[CL].name} for ${board.locations[CL].purchasePrice}? (y/n) ") == 'y'):
        price = board.locations[CL].purchasePrice
        if(players[turn].cash > price):
            players[turn].buy(CL, board)
            board.locations[CL].owner = turn
            update_history(f"{players[turn].name} bought {board.locations[CL].name} for ${price}")
        else:
            update_history(f"{players[turn].name} did not buy {board.locations[CL].name}")

def housing_logic(p: Player):
    update_status(p, "properties")
    propertyid = input("\033[38;0HWhat property do you want to build on? Enter property # or 'e' to exit."+"\033[39;0H" + " " * 78 + "\033[40;0H" + " " * 78+"\033[41;0H" + " " * 78+"\033[39;0H")
    flag = True
    exit = False
    try:   
        if propertyid == 'e':
            print("\033[37;0H " + ' ' * 78+ "\033[38;0H " + ' ' * 78 + "\033[39;0H " + ' ' * 78)
            exit = True
        else:
            propertyid =  int(propertyid)
    except ValueError: ###AHHHHHHHH clean me please
        print(f"\033[42;0" + COLORS.RED + f"Invalid input, please enter a number in {p.properties}", end=COLORS.RESET)
        flag = False
    if flag and not exit:
        if not propertyid in p.properties:
            print("\033[40;0HYou do not own this property!")
        else: 
            family = board.locations[propertyid].color
            if family == COLORS.CYAN or family == COLORS.LIGHTBLACK or board.locations[propertyid].name.startswith("Electric"):
                print("\033[40;0HThis property cannot be improved.")
                flag = False
            if flag: 
                for i in range(propertyid-3 if propertyid > 3 else 0, propertyid+5 if propertyid < 35 else 39): # check only a few properties around for efficiency
                    if board.locations[i].color == family:
                        if not i in p.properties:
                            print("\033[40;0HYou do not own a monopoly on these properties!")
                            flag = False
            if flag:
                max = 5 - board.locations[propertyid].houses
                houses = input(f"Cost of housing is ${board.locations[propertyid].housePrice}. How many houses would you like to buy? (Max {max}/min 0)")
                try:
                    houses = int(houses)
                    if(0 <= houses <= max):
                        p.cash -= board.locations[propertyid].housePrice * houses
                        update_history(f"{p} bought {houses} house{'s' if houses > 1 else ''} on {board.locations[propertyid].name}!")
                        board.locations[propertyid].houses += houses
                        refresh_board()
                    else:
                        raise ValueError
                except ValueError:
                    print(f"Invalid input. Please enter a number 0-{max}")
    if not exit:
        housing_logic(p)

def mortgage_logic(p:Player):
    update_status(p, "properties")
    propertyid = input("\033[38;0HWhat property to mortgage? Enter property # or 'e' to exit."+"\033[39;0H" + " " * 78 + "\033[40;0H" + " " * 78+"\033[41;0H" + " " * 78+"\033[39;0H")
    flag = True
    exit = False
    try:   
        if propertyid == 'e':
            print("\033[37;0H " + ' ' * 78+ "\033[38;0H " + ' ' * 78 + "\033[39;0H " + ' ' * 78+ "\033[40;0H " + ' ' * 78+ "\033[41;0H " + ' ' * 78+ "\033[42;0H " + ' ' * 78)
            exit = True
        else:
            propertyid =  int(propertyid)
    except ValueError: ###AHHHHHHHH clean me please
        print(f"\033[42;0" + COLORS.RED + f"Invalid input, please enter a number in {p.properties}", end=COLORS.RESET)
        flag = False
    if flag and not exit:
        if not propertyid in p.properties:
            print("\033[42;0HYou do not own this property!")
        elif board.locations[propertyid].mortgage == 0:
            print("\033[42;0HYou cannot mortgage this property!")
        elif board.locations[propertyid].houses != 0:
            print("\033[42;0HYou must sell your houses on this property first!")
        elif board.locations[propertyid].mortgaged:
            print("\033[39;0HThis property is already mortgaged!")
            answer = input(f"\033[40;0HWould you like to repay your mortgage for ${board.locations[propertyid].mortgage * 1.1}? (y/n)")
            if answer == 'y' or answer == 'Y':
                price = board.locations[propertyid].mortgage * 1.1
                if (players[turn].cash > price):
                    players[turn].buy(propertyid,board)
                    board.locations[propertyid].mortgaged = False
                    update_history(f"{players[turn].name} repaid their mortgage on {board.locations[propertyid].name}")
        else:
            p.cash += board.locations[propertyid].mortgage
            board.locations[propertyid].mortgaged = True 
            update_history(f"{p} mortgaged {board.locations[propertyid].name}!")
    if not exit:
        refresh_board()
        mortgage_logic(p)
    
def sell_logic(p:Player):
    update_status(p, "properties")
    propertyid = input("\033[38;0HWhat property do you want to sell houses on? Enter property # or 'e' to exit."+"\033[39;0H" + " " * 78 + "\033[40;0H" + " " * 78+"\033[41;0H" + " " * 78+"\033[39;0H")
    flag = True
    exit = False
    try:   
        if propertyid == 'e':
            print("\033[37;0H " + ' ' * 78+ "\033[38;0H " + ' ' * 78 + "\033[39;0H " + ' ' * 78)
            exit = True
        else:
            propertyid =  int(propertyid)
    except ValueError: ###AHHHHHHHH clean me please
        print(f"\033[42;0" + COLORS.RED + f"Invalid input, please enter a number in {p.properties}", end=COLORS.RESET)
        flag = False
    if flag and not exit:
        if not propertyid in p.properties:
            print("\033[40;0HYou do not own this property!")
        else: 
            family = board.locations[propertyid].color
            if family == COLORS.CYAN or family == COLORS.LIGHTBLACK or board.locations[propertyid].name.startswith("Electric"):
                print("\033[40;0HThis property cannot have houses.")
                flag = False
            if flag and board.locations[propertyid].houses == 0: 
                print("\033[40;0HYou do not own any house on this property!")
                flag = False
            if flag:
                houses = input(f"Sell price is ${board.locations[propertyid].housePrice // 2}. How many houses would you like to sell? (Max {board.locations[propertyid].houses}/min 0)")
                try:
                    houses = int(houses)
                    if (0 <= houses <= board.locations[propertyid].houses):
                        p.cash += houses * board.locations[propertyid].housePrice // 2
                        board.locations[propertyid].houses -= houses
                        update_history(f"{p} sold {houses} house{'s' if houses > 1 else ''} on {board.locations[propertyid].name}!")
                        refresh_board()
                    else:
                        raise ValueError
                except ValueError:
                    print(f"Invalid input. Please enter a number 0-{board.locations[propertyid].houses}")
    if not exit:
        sell_logic(p)


from datetime import datetime
def log_error(error_message: str) -> None:
    """
    Log error message to errorlog.txt\n
    """
    with open("errorlog.txt", "a") as f:
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"{formatted_datetime}\n{error_message}\n")

ss.make_fullscreen()

ss.calibrate_screen('gameboard')

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
print(COLORS.WHITE + "\033[0;0H", end="")
print(gameboard)

def unittest():
    players[1].buy(1, board)
    players[1].buy(3, board)
    players[2].buy(5, board)
    players[2].buy(15, board)
    players[2].buy(25, board)
    players[2].buy(35, board)
    players[3].buy(12, board)
    players[3].buy(28, board)

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
        update_history(player_color + f"{players[turn].name}'s turn")
        print_commands()
        input("\033[36;0HRoll dice?")
        dice = roll()
        bottom_screen_wipe()
        update_history(f"{players[turn].name} rolled {dice[0]} and {dice[1]}")

        if dice[0] == dice[1]:
            if  num_rolls == 1:
                update_history(f"{players[turn].name} rolled doubles! Roll again.")

            elif num_rolls == 2:
                update_history(f"{players[turn].name} rolled doubles!(X2) Roll again.")

            elif num_rolls == 3:
                update_history(f"{players[turn].name} rolled doubles three times\n in a row!")
                update_history(f"{players[turn].name} is going to jail!")
                players[turn].jail = True
                board.update_location(players[turn], -1)
        refresh_board()
        #if player rolled their third double they will be in jail and their location doesn't update
        if players[turn].jail == False:
            if (players[turn].location + dice[0] + dice[1]) > 39:  # checks if player passed go
                update_history(f"Player {players[turn].order} passed Go and received $200")
            board.update_location(players[turn], dice[0] + dice[1])
            update_history(f"{players[turn].name} landed on {board.locations[players[turn].location].name}")
            refresh_board()
        done_moving_around = False
        card = ""
        while not done_moving_around:
            done_moving_around = True
            if board.locations[players[turn].location].owner < 0:
                match board.locations[players[turn].location].owner:
                    case -1: #unowned
                        buy_logic()
                    case -2: #mortgaged
                        pass
                    case -3: #community chest
                        old_loc = players[turn].location
                        card = decks.draw_community_chest(players[turn], board, players)
                        new_loc = players[turn].location
                        update_history(f"{players[turn].name} drew a Community Chest card! {card}")
                        if old_loc > new_loc and new_loc != 10 and new_loc != players[turn].location - 3:  #check if chance card made player pass go
                            update_history(f"Player {players[turn].order} passed Go and received $200")
                    case -4: #chance
                        old_loc = players[turn].location
                        card = decks.draw_chance(players[turn], board, players)
                        new_loc = players[turn].location
                        update_history(f"{players[turn].name} drew a Chance card! {card}")
                        if old_loc > new_loc and new_loc != 10 and new_loc != players[turn].location - 3:  #check if chance card made player pass go
                            update_history(f"Player {players[turn].order} passed Go and received $200")
                        if (board.locations[players[turn].location].owner != -4):
                            done_moving_around = False  # only case where loop is needed
                    case -5: #income tax
                        players[turn].pay(200)
                        update_history(f"{players[turn].name} paid income tax ($200)")
                    case -6:  # jail
                        pass
                    case -7:  # go to jail
                        players[turn].jail = True
                        board.update_location(players[turn], -1)
                    case -8:  # free parking
                        pass
                    case -9:  # luxury tax
                        players[turn].pay(100)
                        update_history(f"{players[turn].name} paid luxury tax ($100)")
                    case -10:  # go
                        pass
            elif board.locations[players[turn].location].owner != players[turn].order:
                # Pay another player rent
                cl = players[turn].location
                rent = board.locations[cl].getRent()
                if board.locations[cl].name == "Electric Company" or board.locations[cl].name == "Water Works":
                    rent *= dice[0] + dice[1]

                if card != "":  # if player collected a specific chance card and moved afterwards on same turn
                    if int(card.split(".")[0]) in [5, 6]:
                        rent *= 2
                    elif int(card.split(".")[0]) in [7]:
                        rent = 10 * (dice[0] + dice[1])
                players[turn].pay(rent)
                players[board.locations[cl].owner].receive(rent)
                update_history(f"{players[turn].name} paid ${rent} to {players[board.locations[cl].owner].name}")
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
        update_history(f"{players[turn].name} ended their turn.")
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
            update_history(f"{players[turn].name} declared bankruptcy.")
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