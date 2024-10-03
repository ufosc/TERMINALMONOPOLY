# Monopoly game is played on Banker's terminal. 
import style as s
from style import COLORS
import random
import os

from properties import Property
from cards import Cards
from board import Board
from player_class import MonopolyPlayer
import screenspace as ss
import style as s

mode = "normal"
output = ""
gameboard = ""
board = None
history = []
status = []
CASH = 2000
num_players = 4
bankrupts = 0
players = []
border = s.get_graphics().get('history and status')
border = border.split("\n")
turn = 0

def get_gameboard() -> str:
    """
    Get the gameboard\n
    """
    global output
    output = ""
    print_commands()
    refresh_h_and_s()
    refresh_board()
    if mode == "banker":
        return output
    else:
        print(output)

def add_to_output(s):
    global output
    if mode == "banker":
        output += s
    else:
        print(s, end="")

def refresh_board():
    """
    Refresh the gameboard\n
    """
    
    add_to_output(COLORS.RESET + "\033[0;0H")
    add_to_output(gameboard)
    for i in range(40): 
        # This loop paints the properties on the board with respective color schemes
        color = board.locations[i].color
        backcolor = board.locations[i].color.replace("38", "48")
        add_to_output(COLORS.backBLACK + color + f"\033[{board.locations[i].x};{board.locations[i].y}H{i}" + backcolor + " " * (4 + (1 if i < 10 else 0)))
        
        if(board.locations[i].owner != -1): # If owned
            add_to_output(COLORS.RESET)
            color = f"\033[38;5;{board.locations[i].owner+1}m"
            add_to_output(f"\033[{board.locations[i].x+2};{board.locations[i].y}H" + color + "▀")

        if(board.locations[i].owner == -3): # If community chest
            add_to_output(COLORS.RESET)
            add_to_output(f"\033[{board.locations[i].x + 1};{board.locations[i].y}H" + COLORS.COMMUNITY + "█" * 6)
            add_to_output(f"\033[{board.locations[i].x + 2};{board.locations[i].y}H" + COLORS.COMMUNITY + "▀" * 6)

        if(board.locations[i].owner == -4): # If chance
            add_to_output(COLORS.RESET)
            add_to_output(f"\033[{board.locations[i].x + 1};{board.locations[i].y}H" + COLORS.CHANCE + "█" * 6)
            add_to_output(f"\033[{board.locations[i].x + 2};{board.locations[i].y}H" + COLORS.CHANCE + "▀" * 6)
        
        if(board.locations[i].houses > 0): # If there are houses
            add_to_output(COLORS.RESET)
            add_to_output(f"\033[{board.locations[i].x+2};{board.locations[i].y+1}H" + COLORS.GREEN + "▀" * (board.locations[i].houses))
        
        if(board.locations[i].houses == 5): # If there is a hotel
            add_to_output(COLORS.RESET)
            add_to_output(f"\033[{board.locations[i].x+2};{board.locations[i].y+5}H" + COLORS.RED + "▀")

        if(board.locations[i].owner == -2): # If mortgaged
            add_to_output(COLORS.RESET)
            add_to_output(f"\033[{board.locations[i].x+2};{board.locations[i].y}H" + COLORS.backLIGHTGRAY + "M")

    add_to_output(COLORS.RESET)

    for i in range(num_players):
        color = COLORS.playerColors[i]
        token = "◙"
        add_to_output(color + f"\033[{board.locations[players[i].location].x+1};{board.locations[players[i].location].y+1+i}H{token}")
    
    add_to_output(COLORS.RESET)

def print_commands():
    """
    Print commands\n
    """
    commandsinfo = s.get_graphics().get('commands').split("\n")
    for i in range(len(commandsinfo)):
        add_to_output(f"\033[{34+i};79H" + commandsinfo[i])

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

def update_status(p: MonopolyPlayer, update: str, status: list = status, mode: str = "normal", property_id: str = ""):
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
        if mode == "normal":
            propertyid = input("What property to view? Enter property #")
        else:
            propertyid = property_id
        try:
            location = board.locations[int(propertyid)]
            if location.owner > -1: # if the location is owned
                color = COLORS.playerColors[location.owner]
                status.append(f"Current owner: " + color + f"{players[location.owner]}" + COLORS.RESET)
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
            add_to_output(f"Invalid input. Please enter a # for a property.")
            if mode == "banker":
                return get_gameboard() + ss.set_cursor_str(0, 39) + f"[Deed Viewer]\nInvalid input. Please enter a # for a property."
    refresh_h_and_s()
    if mode == "banker":
        return get_gameboard()

def refresh_h_and_s():
    """
    Refresh the history, status, and leaderboard\n
    """
    # Refresh history
    for i in range(len(border)):
        add_to_output(f"\033[{i};79H")
        if(len(history) - i<= 0):
            for j in range(len(border[i])):
                add_to_output(border[i][j])
    for i in range(len(history)):
        add_to_output(f"\033[{i+4};81H" + (history[i] if i < len(history) else "") + COLORS.RESET)
    
    # Refresh status
    for i in range(len(status)):
        add_to_output(f"\033[{i+4};122H" + status[i] if i < len(status) else "")
    add_to_output(COLORS.RESET)

    # Refresh leaderboard
    sorted_players = sorted(players, key=lambda x: x.cash, reverse=True)
    for i in range(len(sorted_players)):
        if(sorted_players[i].order != -1):
            color = COLORS.playerColors[sorted_players[i].order]
            add_to_output(color + f"\033[{31+i};122H{sorted_players[i].name} - ${sorted_players[i].cash}" + COLORS.RESET)

def buy_logic(mode: str = "normal", pinput: str = ""):
    CL = players[turn].location
    if mode == "normal":
        choice = input(ss.set_cursor_str(0, 37) + "b to buy, enter to continue?")
    else:
        choice = pinput
    if(board.locations[CL].purchasePrice != 0 and board.locations[CL].owner == -1):
        price = board.locations[CL].purchasePrice
        if(players[turn].cash > price and choice == 'b'):
            players[turn].buy(CL, board)
            board.locations[CL].owner = turn
            update_history(f"{players[turn].name} bought {board.locations[CL].name} for ${price}")
        else:
            update_history(f"{players[turn].name} did not buy {board.locations[CL].name}")

def housing_logic(p: MonopolyPlayer, mode: str = "normal", propertyid: str = "", num_houses: int = -1):
    update_status(p, "properties")
    if mode == "normal":
        propertyid = input(ss.set_cursor_str(0, 39) + "What property do you want to build on? Enter property # or 'e' to exit.")
    else:
        if propertyid == "e":
            return get_gameboard()
        elif propertyid == "":
            return get_gameboard() + ss.set_cursor_str(0, 39) + f"[Property management]\nEnter an ID of one of your properties: {p.properties}" + COLORS.RESET
    flag = True
    exit_flag = False
    try:   
        if propertyid == 'e':
            exit_flag = True
        else:
            propertyid =  int(propertyid)
    except ValueError: ###AHHHHHHHH clean me please
        add_to_output(f"\033[42;0" + COLORS.RED + f"Invalid input, please enter a number in {p.properties}" + COLORS.RESET)
        flag = False
    if flag and not exit_flag:
        if not propertyid in p.properties:
            add_to_output("You do not own this property!")
        else: 
            family = board.locations[propertyid].color
            if family == COLORS.CYAN or family == COLORS.LIGHTBLACK or board.locations[propertyid].name.startswith("Electric"):
                add_to_output("This property cannot be improved.")
                flag = False
                if mode == "banker":
                    return get_gameboard() + ss.set_cursor_str(0, 40) + "This property cannot be improved."
            if flag: 
                for i in range(propertyid-3 if propertyid > 3 else 0, propertyid+5 if propertyid < 35 else 39): # check only a few properties around for efficiency
                    if board.locations[i].color == family:
                        if not i in p.properties:
                            add_to_output("You do not own a monopoly on these properties!")
                            flag = False
                            if mode == "banker":
                                return get_gameboard() + ss.set_cursor_str(0, 40) + "You do not own a monopoly on these properties!"
                                
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
                    max_houses = 5 - board.locations[propertyid].houses
                    if mode == "normal":
                        houses = input(f"Cost of housing is ${cost}. How many houses would you like to buy? (Max {max_houses}/min 0)")
                    else:
                        return get_gameboard() + ss.set_cursor_str(0, 39) + f"[Property management]\nCost of housing is ${cost}. How many houses would you like to buy? (Max {max_houses}/min 0)"
                    if mode == "normal":
                        try:
                            houses = int(houses)
                            if(0 <= houses <= max_houses):
                                p.cash -= cost * houses
                                update_history(f"{p} bought {houses} houses on {board.locations[propertyid].name}!")
                                board.locations[propertyid].houses += houses
                                refresh_board()
                            else:
                                raise ValueError
                        except ValueError:
                            add_to_output(f"Invalid input. Please enter a number 0-{max_houses}")
        
    if not exit_flag:
        if mode == "normal":
            housing_logic(p)
        else:
            return get_gameboard() + ss.set_cursor_str(0, 39) + f"[Property management]\nEnter an ID of one of your properties: {p.properties}" + COLORS.RESET
    return get_gameboard()

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

def unittest():
    players[1].buy(1, board)
    players[1].buy(3, board)
    players[2].buy(5, board)
    players[2].buy(15, board)
    players[2].buy(25, board)
    players[2].buy(35, board)
    players[3].buy(12, board)
    players[3].buy(28, board)

#wipes the bottom of the screen where the player does all of their input
def bottom_screen_wipe():
    add_to_output(ss.set_cursor_str(0, 36) + " " * 76)
    add_to_output(ss.set_cursor_str(0, 37) + " " * 76)
    add_to_output(ss.set_cursor_str(0, 38) + " " * 76)
    add_to_output(ss.set_cursor_str(0, 39) + " " * 76)
    add_to_output(ss.set_cursor_str(0, 40) + " " * 76)
    add_to_output(ss.set_cursor_str(0, 41) + " " * 76)
    add_to_output(ss.set_cursor_str(0, 42) + " " * 76)
    add_to_output(ss.set_cursor_str(0, 43) + " " * 76)
    add_to_output(ss.set_cursor_str(0, 44) + " " * 76)
    add_to_output(ss.set_cursor_str(0, 36))

#Rolls the dice and returns them for the player as a tuple
def roll():
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    return(die1,die2)
#The function that handles the players
#second and third correspond to if its the players second or third consecutive turn, they are bools

def player_roll(num_rolls, act: int = 0, mode: str = "normal") -> str:
    print_commands()
    bottom_screen_wipe()
    if(players[turn].order != -1): # If player is not bankrupt
        player_color = COLORS.playerColors[turn]
        update_history(player_color + f"{players[turn].name}'s turn")
        print_commands()
        
        was_in_jail = players[turn].jail  # Flag to check if player was in jail before rolling
        
        if players[turn].jail:
            if players[turn].jail_turns < 3:
                while True:
                    choice = input("\033[36;0HYou're in jail. Pay $50 fine (f) or attempt to roll doubles (r)?").lower().strip()
                    if choice == 'f':
                        players[turn].pay_jail_fine()
                        update_history(f"{players[turn].name} paid $50 to leave jail.")
                        update_history(f"{players[turn].name} cannot roll after paying the fine.")
                        return  # End the turn after paying the fine
                    elif choice == 'r':
                        update_history(f"{players[turn].name} will attempt to roll doubles.")
                        break
                    else:
                        update_history(f"Invalid choice. Please enter 'f' to pay fine or 'r' to roll.")
            else:
                update_history(f"This is {players[turn].name}'s third turn in jail. They must attempt to roll doubles.")
                
        input("\033[36;0HRoll dice?")
        dice = roll()
        bottom_screen_wipe()
        update_history(f"{players[turn]} rolled {dice[0]} and {dice[1]}")

        if players[turn].jail:
            left_jail, reason = players[turn].attempt_jail_roll(dice)
            if left_jail:
                if reason == "doubles":
                    update_history(f"{players[turn].name} rolled doubles and got out of jail!")
                elif reason == "third_turn":
                    update_history(f"{players[turn].name} didn't roll doubles on their third turn. They paid $50 and left jail.")
                    players[turn].pay_jail_fine()
                    update_history(f"{players[turn].name} cannot roll after paying the fine.")
                    return  # End the turn after paying the fine on third turn
            else:
                update_history(f"{players[turn].name} didn't roll doubles and is still in jail. Turns in jail: {players[turn].jail_turns}")
                return

        refresh_board()
        board.update_location(players[turn], dice[0] + dice[1], update_history)
        update_history(f"{players[turn].name} landed on {board.locations[players[turn].location].name}")
        refresh_board()
        
        # Only check for doubles if the player wasn't in jail at the start of their turn
        if dice[0] == dice[1] and not was_in_jail:
            if num_rolls == 1:
                update_history(f"{players[turn]} rolled doubles! Roll again.")

            elif num_rolls == 2:
                update_history(f"{players[turn]} rolled doubles!(X2) Roll again.")

            elif num_rolls == 3:
                update_history(f"Player {turn} rolled doubles three times in a row!")
                update_history(f"Player {turn} is going to jail!")
                players[turn].go_to_jail()
                return

        refresh_board()
        #if player rolled their third double they will be in jail and their location doesn't update
        if players[turn].jail == False:
            if (players[turn].location + dice[0] + dice[1]) > 39:  # checks if player passed go
                update_history(f"{players[turn]} passed Go and received $200")
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
                            update_history(f"{players[turn]} passed Go and received $200")
                    case -4: #chance
                        old_loc = players[turn].location
                        card = decks.draw_chance(players[turn], board, players)
                        new_loc = players[turn].location
                        update_history(f"{players[turn].name} drew a Chance card! {card}")
                        if old_loc > new_loc and new_loc != 10 and new_loc != players[turn].location - 3:  #check if chance card made player pass go
                            update_history(f"{players[turn]} passed Go and received $200")
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

def request_roll() -> str:
    """
    Custom function to request a roll of the dice, meant to be called from banker.py\n
    TODO add more detail here
    """
    print_commands()
    bottom_screen_wipe()
    if(players[turn].order != -1): # If player is not bankrupt
        player_color = COLORS.playerColors[turn]
        update_history(player_color + f"{players[turn].name}'s turn")
        print_commands()
        output = get_gameboard()
        output += ss.set_cursor_str(0, 36) + "Press enter to roll dice."
        return output
    else:
        return "Player is bankrupt." # Really once a player is bankrupt, they should be shut off.

def process_roll(num_rolls: int, dice: tuple) -> str:
    """
    Custom function to process the roll of the dice, meant to be called from banker.py\n
    TODO add more detail here
    """
    bottom_screen_wipe()
    update_history(f"{players[turn]} rolled {dice[0]} and {dice[1]}")

    if dice[0] == dice[1]:
        if  num_rolls == 1:
            update_history(f"{players[turn]} rolled doubles! Roll again.")

        elif num_rolls == 2:
            update_history(f"{players[turn]} rolled doubles!(X2) Roll again.")

        elif num_rolls == 3:
            update_history(f"{players[turn]} rolled doubles three times\n in a row!")
            update_history(f"{players[turn]} is going to jail!")
            players[turn].jail = True
            board.update_location(players[turn], -1)
    refresh_board()
    #if player rolled their third double they will be in jail and their location doesn't update
    if players[turn].jail == False:
        if (players[turn].location + dice[0] + dice[1]) > 39:  # checks if player passed go
            update_history(f"{players[turn]} passed Go and received $200")
        board.update_location(players[turn], dice[0] + dice[1])
        update_history(f"{players[turn].name} landed on {board.locations[players[turn].location].name}")
        refresh_board()

    print("Board updated: " + get_gameboard())

    return evaluate_board_location(num_rolls, dice)

def evaluate_board_location(num_rolls: int, dice: tuple) -> str:
    """
    Custom function to evaluate the board location, meant to be called from banker.py\n
    TODO add more detail here
    """
    done_moving_around = False
    card = ""
    while not done_moving_around:
        done_moving_around = True
        if board.locations[players[turn].location].owner < 0:
            match board.locations[players[turn].location].owner:
                case -1: #unowned
                    return get_gameboard() + ss.set_cursor_str(0, 37) + "b to buy, enter to continue?"
                case -2: #mortgaged
                    pass
                case -3: #community chest
                    old_loc = players[turn].location
                    card = decks.draw_community_chest(players[turn], board, players)
                    new_loc = players[turn].location
                    update_history(f"{players[turn].name} drew a Community Chest card! {card}")
                    if old_loc > new_loc and new_loc != 10 and new_loc != players[turn].location - 3:  #check if chance card made player pass go
                        update_history(f"{players[turn]} passed Go and received $200")
                case -4: #chance
                    old_loc = players[turn].location
                    card = decks.draw_chance(players[turn], board, players)
                    new_loc = players[turn].location
                    update_history(f"{players[turn].name} drew a Chance card! {card}")
                    if old_loc > new_loc and new_loc != 10 and new_loc != players[turn].location - 3:  #check if chance card made player pass go
                        update_history(f"{players[turn]} passed Go and received $200")
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
        
    # Check for doubles and roll again only if player wasn't in jail at the start of their turn
    if dice[0] == dice[1] and not was_in_jail:
        num_rolls += 1
        request_roll()
    return "player_choice" + ss.set_cursor_str(0, 38) + "e to end turn, p to manage properties, d to view a deed?" + get_gameboard()

def end_turn():
    global turn
    turn = (turn + 1)%num_players

def player_choice():
    if(players[turn].cash > 0):
        choice = input("\033[38;0He to end turn, p to manage properties, d to view a deed?")
        while(choice != 'e'): 
            if choice == "e":
                pass
            elif choice == "p":
                housing_logic(players[turn])
            elif choice == "d":
                update_status(players[turn], "deed")
            else:
                add_to_output("Invalid option!")
            choice = input("\033[38;0H'e' to end turn, p to manage properties, ?")
        update_history(f"{players[turn]} ended their turn.")
    else:
        update_history(f"{players[turn]} is in debt. Resolve debts before ending turn.")
        option = input("\033[38;0HResolve debts before ending turn.").lower().strip()
        if(option == "b"): # Declare bankruptcy
            update_history(f"{players[turn]} declared bankruptcy.")
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

def start_game(cash: int, num_p: int) -> str:
    global CASH, num_players, players, gameboard, board, decks, mode
    ss.clear_screen()
    mode = "banker"
    gameboard = s.get_graphics().get('gameboard')
    num_players = num_p
    CASH = cash
    board = Board(num_players)
    decks = Cards()
    players = []
    for i in range(num_players):
        players.append(MonopolyPlayer(CASH, i))

    add_to_output(COLORS.WHITE + "\033[0;0H")
    add_to_output(gameboard)
    return output

def game_loop():
        # First time the player who's turn it is rolls their dice
        #if they roll a double the function calls itself and updates its their number of consecutive rolls
        player_roll(num_rolls=1)
        #player_choice is where the player can choose to end their turn, manage properties, or view a deed
        player_choice()

if __name__ == "__main__": # For debugging purposes. Can play standalone
    ss.make_fullscreen()

    ss.calibrate_screen('gameboard')

    # CASH = input("Starting cash?")
    # num_players = int(input("Number players?"))
    for i in range(num_players):
        players.append(MonopolyPlayer(CASH, i))

    turn = 0

    board = Board(num_players)
    decks = Cards()


    gameboard = s.get_graphics().get('gameboard')
    os.system('cls' if os.name == 'nt' else 'clear')
    
    unittest()
    
    add_to_output(COLORS.WHITE + "\033[0;0H")
    add_to_output(gameboard)

    while(True):
        game_loop()

        if(bankrupts == num_players - 1):
            break
        turn = (turn + 1)%num_players

    for index, player in enumerate(players):
        if player.order != -1:
            color = COLORS.playerColors[index]
            update_history(color + f"{players[index]} wins!")
            break
    add_to_output("\033[40;0H")