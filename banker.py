# Python Builtin Utilities
import socket
import threading
import os
import sys
import random
import select
from time import sleep
import importlib

# Our Utilities
from style import MYCOLORS as COLORS, print_w_dots, choose_colorset
import screenspace as ss 
import gamemanager as gm
import networking as net
import validation as valid

# Modules
import modules_directory.tictactoe as tictactoe
import modules_directory.inventory as inv
from modules_directory.inventory import handle as handle_inventory
from modules_directory.deed_viewer import handle as handle_deed
from modules_directory.balance import handle as handle_balance
from modules_directory.casino import handle as handle_casino
from modules_directory.chat import handle as handle_chat
from modules_directory.shop import handle as handle_shop

# Monopoly Game
import monopoly_directory.monopoly as mply

STARTING_CASH = 1500
clients = []
server_socket = None
port = 3131
num_players = 0
play_monopoly = True
handle_cmds = {}
messages = []

TTT_Output = ss.OutputArea("TicTacToe", ss.TTT_OUTPUT_COORDINATES, 36, 9)
Casino_Output = ss.OutputArea("Casino", ss.CASINO_OUTPUT_COORDINATES, 36, 22)
Monopoly_Game_Output = ss.OutputArea("Monopoly", ss.MONOPOLY_OUTPUT_COORDINATES, 191, 6)
Main_Output = ss.OutputArea("Main", ss.MAIN_OUTPUT_COORDINATES, 79, 12)

class Client:
    def __init__(self, socket: socket.socket, id: int, name: str, money: int, properties: list, inventory_object: inv.Inventory):
        self.socket = socket
        self.id = id
        self.name = name
        self.money = money
        self.properties = properties
        self.inventory = inventory_object
        self.can_roll = True
        self.num_rolls = 0
        self.terminal_statuses = ["ACTIVE", "ACTIVE", "ACTIVE", "ACTIVE"]

def add_to_output_area(output_type: str, text: str, color: str = COLORS.WHITE) -> None:
    """
    Adds text to the specified output area.
    This should replace all print statements in the code.

    Args:
        output_area (str): The output area to add text to.
        text (str): The text to add.

    Returns:
        None
    """
    if output_type == "Monopoly":
        Monopoly_Game_Output.add_output(text, color)
    elif output_type == "TicTacToe":
        TTT_Output.add_output(text, color)
    elif output_type == "Casino":
        Casino_Output.add_output(text, color)
    else:
        Main_Output.add_output(text, color)

def start_server() -> socket.socket:
    """
    Begins receiving server socket on local machine IP address and inputted port #. 

    Asks user for port # and begins server on the local machine at its IP address. 
    It then waits for a predetermined number of players to connect. Upon a full game, 
    it returns the transmitter socket. 

    Parameters: None

    Returns: Transmitter socket aka the Banker's sender socket.  
    """
    global clients, port, server_socket
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if "-local" in sys.argv:
        ip_address = "localhost"
        host = "localhost"
        port = 33333
    else: 
        # Get local machine name
        host = socket.gethostname()
        ip_address = socket.gethostbyname(host)

        # Choose a port that is free
        port = input("Choose a port, such as 3131: ")
    
        while not valid.validate_port(port) or not valid.is_port_unused(int(port)):
            port = input("Invalid port. Choose a port, such as 3131: ")

    port = int(port) # Convert port to int for socket binding
    # Bind to the port
    server_socket.bind((host, port))
    print_w_dots(f"Server started on {ip_address} port {port}")
    server_socket.listen()

    print_w_dots(f"Waiting for {num_players} clients...")
    
    handshakes = [False] * num_players

    game_full = False
    while not game_full:
        # Accepts connections while there are less than <num_players> players
        if len(clients) < num_players:
            client_socket, addr = server_socket.accept()
            print(f"Got a connection from {addr}." if ss.VERBOSE else "Got a connection.")
            client_handler = threading.Thread(target=handshake, args=(client_socket,handshakes))
            client_handler.start()
        else: 
            game_full = True
        sleep(0.5) 
    print_w_dots("Game is full. Starting game")
    # Send a message to each client that the game is starting, allowing them to see their terminals screen
    for i in range(len(clients)): 
        clients[i].id = i
        net.send_message(clients[i].socket, f"Game Start!{num_players} {i}")
        sleep(0.5)

def start_receiver() -> None:
    """
    This function handles all client-to-server requests (not the other way around).
    Function binds an independent receiving socket at the same IP address, one port above. 
    For example, if the opened port was 3131, the receiver will open on 3132.  
    
    Parameters: None

    Returns: None
    """
    global player_data, port
    add_to_output_area("Main", "[RECEIVER] Receiver started!", COLORS.GREEN) 
    # Credit to https://stackoverflow.com/a/43151772/19535084 for seamless server-client handling. 
    with socket.socket() as server:
        host = socket.gethostname()
        ip_address = socket.gethostbyname(host)
        if "-local" in sys.argv:
            ip_address = "localhost"
            port = 33333
        server.bind((ip_address,int(port+1)))
        server.listen()
        add_to_output_area("Main", f"[RECEIVER] Receiver accepting connections at {port+1}", COLORS.GREEN)
        to_read = [server]  # add server to list of readable sockets.
        while True:
            # check for a connection to the server or data ready from clients.
            # readers will be empty on timeout.
            readers,_,_ = select.select(to_read,[],[],0.1)
            for reader in readers:
                if reader is server:
                    player,address = reader.accept()
                    add_to_output_area("Main", f"Player connected from: {address[0]}", COLORS.GREEN)
                    to_read.append(player) # add client to list of readable sockets
                else:
                    try:
                        data = net.receive_message(reader)
                        handle_data(data, reader)
                    except ConnectionResetError:
                        add_to_output_area("Main", f"Player at {address[0]} disconnected.", COLORS.RED)
                        to_read.remove(reader) # remove from monitoring

                        # TODO send a message to each player to query who is still connected, then properly remove
                        # the disconnected player from the game. Currently only removing the first player in clients list. 
                        clients.pop(0)

                    # if not data: # No data indicates disconnect
                    #     add_to_output_area("Main", f"Player at {address[0]} disconnected.", s.COLORS.RED)
                    #     to_read.remove(reader) # remove from monitoring
                if(len(to_read) == 1):
                    if "-stayopen" not in sys.argv:
                        add_to_output_area("Main", "[RECEIVER] All connections dropped. Receiver stopped.", COLORS.GREEN)
                        return
                    else:
                        add_to_output_area("Main", "[RECEIVER] All connections dropped. Receiver will stay open.", COLORS.GREEN)
                        # Reopen the server socket
                        server_socket.close()
                        start_server()

def set_unittest() -> None:
    """
    Unit test function for the Banker module.
    Add here as you think of more tests.

    Parameters: None

    Returns: None
    """
    global num_players, STARTING_CASH, play_monopoly
    ss.set_cursor_str(0, 0)
    print(f"""
    Enter to skip unit testing.
    - Monopoly game will not start.
    - num_players = 2
    - STARTING_CASH = 1500
    - No games added to the game manager.
    
    Unit test -1: Create your own test. 
    - Set the number of players, starting cash to whatever you want.
    - You may also indicate whether to start the Monopoly game or not.

    Unit test 1: 
    - num_players = 1
    - Starts the Monopoly game.
    - STARTING_CASH = 2000    
    - Tests adding games to the game manager (1 Game).

    Unit test 2:
    - num_players = 2
    - Starts the Monopoly game.
    - STARTING_CASH = 1500
    - Tests adding games to the game manager (4 Games).
          
    Unit test 3:
    - num_players = 4
    - Does not start the Monopoly game.
    - STARTING_CASH = 100
    - No games added to the game manager.
    
    Unit test 4 {COLORS.LIGHTBLUE}(Useful for locally testing modules without Monopoly){COLORS.RESET}: 
    - num_players = 1
    - Does not start the Monopoly game.
    - STARTING_CASH = 100
    - No games added to the game manager.
    
    Any other number will skip unit tests.
    - Monopoly game will not start.
    - num_players = 2
    - STARTING_CASH = 1500
    - No games added to the game manager.
          """ if ss.VERBOSE else "")
    if len(sys.argv) > 1:
        if sys.argv[1].isdigit(): # If a test number is provided as a command line argument
            test = int(sys.argv[1])
        else:
            test = ss.get_valid_int("Enter a test number: ", allowed=[' '])
    else: # If no command line argument is provided, ask for a test number
        test = ss.get_valid_int("Enter a test number: ", allowed=[' '])
    if test == "":
        play_monopoly = False
        STARTING_CASH = 1500
        num_players = 2
        print("Skipping unit tests." if ss.VERBOSE else "")
        return
    if test == -1:
        play_monopoly = ss.get_valid_int("Enter 1 to start Monopoly, 0 to skip: ", 0, 1) == 1
        num_players = ss.get_valid_int("Enter the number of players: ")
        STARTING_CASH = ss.get_valid_int("Enter the starting cash: ")
        return
    
    if (test == 1):
        play_monopoly = True
        num_players = 1
        STARTING_CASH = 2000
        gm.add_game(gm.Game('Fake Game', [Client(None, -1, "Null", 0, [])] * 4, 'board', 'other_data'))
    elif (test == 2):
        play_monopoly = True
        num_players = 2
        STARTING_CASH = 1500
        gm.add_game(gm.Game('Battleship', [Client(None, -99, "Null", 0, [])] * 4, 'board', 'other_data'))
        gm.add_game(gm.Game('Battleship', [Client(None, -98, None, 0, [])] * 2, 'board', 'other_data'))
        gm.add_game(gm.Game('Battleship', [Client(None, -97, "Name", 0, [])] * 3, 'board', 'other_data'))
        gm.add_game(gm.Game('TicTacToe', [Client(None, -96, "nada", 0, [])] * 2, 'board', None))
    elif (test == 3):
        play_monopoly = False
        num_players = 4
        STARTING_CASH = 100
    elif (test == 4):
        play_monopoly = False
        num_players = 1
        STARTING_CASH = 100 
    else:
        play_monopoly = False
        print("Invalid test number." if ss.VERBOSE else "")
        print("Skipping unit tests." if ss.VERBOSE else "")
        return

def change_balance(id: int, delta: int) -> int: 
    """
    Adjusts the balance of a specific player by a given amount.

    This function updates the money attribute of the player identified by their ID.
    A positive delta increases the player's balance, while a negative delta decreases it.

    Args:
        id (int): The unique identifier of the player whose balance needs to be adjusted.
        delta (int): The amount to add or subtract from the player's balance.

    Returns:
        None
    """
    clients[id].money += delta
    return clients[id].money

def handle_data(data: str, client: socket.socket) -> None:
    """
    Handles all data received from player sockets. 
    
    Parameters:
        data (str): Data received from player sockets. 
        client (socket.socket): The client socket that sent the data.
    
    Returns:
        None
    """
    current_client = None
    try:
        current_client = clients[int(data[0])] # Assume the data is prefixed by the client number AKA player_id.
        data = data[1:]
    except:
        current_client = get_client_by_socket(client) # This is a backup in case the client data is not prefixed by client.
        add_to_output_area("Main", f"Failed to get client from data. Data was not prefixed by client: {data}", COLORS.RED)

    add_to_output_area("Main", f"Received data from {current_client.name}: \"{data}\"")
    
    if data == 'request_board': 
        net.send_message(client, mply.get_gameboard())
    
    elif data.startswith('mply'):
        monopoly_game(current_client, data)

    # elif data.startswith('ttt'):
    #     handle_ttt(data, current_client)

    elif "chat" not in data and "inventory" in data: # Ensure the chat module is not being called
        handle_inventory(data, client, current_client.inventory)

    elif "chat" not in data and "shop" in data: # Ensure the chat module is not being called
        handle_shop(data, client, current_client.inventory, current_client.money, current_client.id, change_balance)

    elif data.startswith('deed'):
        handle_deed(data, client, mply)

    elif data.startswith("bal"):
        handle_balance(data, client, mply, current_client.money, current_client.properties)

    elif data.startswith('casino'):
        handle_casino(data, client, change_balance, add_to_output_area, current_client.id, current_client.name)

    elif data.startswith('chat'):
        handle_chat(data, client, messages, current_client.id, current_client.name)
        
    elif data.startswith('term_status'):
        command_data = data.split(' ')
        term = int(command_data[1])
        net.send_message(client, str(current_client.terminal_statuses[term]))
    
    elif data.startswith('kill') or data.startswith('disable') or data.startswith('active') or data.startswith('busy'):
        """
        Should be called by a player (1) to disable another player (2).
        Player 1 expects value of success/fail (busy or already dead).
        Player 2 doesn't know unless it is successful.
        """
        handle_term(data, current_client, client)

def handle_term(cmds: str, current_client: Client, client: socket.socket) -> None:
    """
    Command Structure:
        action player term length
        (Ex. DISABLE 0 5 15)
    
    Args:
        action: Type of action on term (ACTIVE/DISABLE/KILL/BUSY)
        player: ID of player to change
        term:   Terminal to Set
        length: Length of DISABLE
    """
    command_data = cmds.split(' ')
    if(command_data[0] == 'disable'):
        try:
            opponent = int(command_data[1])
            if len(clients) <= opponent or clients[opponent] == None or clients[opponent] == current_client:
                net.send_message(client, "\nInvalid opponent. Please select another player.")
                return
            if(int(command_data[2]) <= 0 or int(command_data[2]) > len(clients[opponent].terminal_statuses)):
                net.send_message(client, "\nInvalid terminal. Please enter a valid terminal ID.")
                return
            if((clients[opponent]).terminal_statuses[int(command_data[2]) - 1] != "ACTIVE"):
                net.send_message(client, "\nThis terminal is not active at the moment.")
                return
            if(int(command_data[3]) < 10):
                net.send_message(client, "\nInvalid time. Must be greater than 10 seconds.")
                return
            else:
                net.send_notif(clients[opponent].socket, "disable " + str(int(command_data[2]) - 1), "TERM:")
                clients[opponent].terminal_statuses[int(command_data[2]) - 1] = "DISABLED"
                add_to_output_area("", f"{clients[opponent].name}'s terminal was disabled. Current Statuses: {clients[opponent].terminal_statuses}")
                threading.Timer(float(command_data[3]), net.send_notif, (clients[opponent].socket, f"enable {str(int(command_data[2]) - 1)}", "TERM:")).start()
                net.send_message(client, "\nTerminal disabled.")
        except:
            net.send_message(client, "\nInvalid opponent. Please select another player.")
    elif(command_data[0] == 'active'):
        current_client.terminal_statuses[int(command_data[1]) - 1] = "ACTIVE"
        add_to_output_area("", f"{current_client.name}'s terminal is active. Current Statuses: {current_client.terminal_statuses}")
    elif(command_data[0] == 'kill'):
        try:
            opponent = int(command_data[1])
            if len(clients) <= opponent or clients[opponent] == None or clients[opponent] == current_client:
                net.send_message(client, "\nInvalid opponent. Please select another player.")
                return
            if(int(command_data[2]) <= 0 or int(command_data[2]) > len(clients[opponent].terminal_statuses)):
                net.send_message(client, "\nInvalid terminal. Please enter a valid terminal ID.")
                return
            if(clients[opponent].terminal_statuses[int(command_data[2]) - 1] != "ACTIVE"):
                net.send_message(client, "\nThis terminal is not active at the moment.")
                return
            else:
                net.send_notif(clients[opponent].socket, "kill " + str(int(command_data[2]) - 1), "TERM:")
                clients[opponent].terminal_statuses[int(command_data[2]) - 1] = "DISABLED"
                add_to_output_area("", f"{clients[opponent].name}'s terminal was killed. Current Statuses: {clients[opponent].terminal_statuses}")
                net.send_message(client, "\nTerminal killed.")
        except:
            net.send_message(client, "\nInvalid opponent. Please select another player.")
    elif(command_data[0] == 'busy'):
        current_client.terminal_statuses[int(command_data[1]) - 1] = "BUSY"
        add_to_output_area("", f"{current_client.name}'s terminal is busy. Current Statuses: {current_client.terminal_statuses}")

def handshake(client_socket: socket.socket, handshakes: list) -> None:
    """
    As players connect, they attempt to handshake the server, this function handles that.
    Player's name is also validated here. If an invalid (or empty) name is input, a default name is assigned.
    
    Parameters:
        client_socket (socket.socket) Server sender socket which players connect to at game initialization. 
        handshakes (list) Boolean list of successful handshakes. By default, all values are false.  

    Returns:
        None
    """
    global clients
    # Attempt handshake
    net.send_message(client_socket, "Welcome to the game!")
    message = net.receive_message(client_socket)
    if message.startswith("Connected!"):
        handshakes[len(clients)-1] = True
        name = message.split(',')[1]
        
        clients.append(Client(client_socket, None, name, 2000, [], inv.Inventory())) # Append the client to the list of clients with a temporary id of None

    else: 
        handshakes[len(clients)-1] = False

def get_client_by_socket(socket: socket.socket) -> Client:
    """
    Returns the client object associated with the given socket. 
    
    Parameters:
        socket (socket.socket): The socket of the client. 
    
    Returns:
        obj (Client):
        Client object associated with the given socket. 
    """
    for client in clients:
        # Only checking the IP address for now. This will not work if two clients are on the same IP address.
        # Think: locally testing. This has proven to be an issue while testing tic tac toe on the same machine.
        # While this should work in a real-world scenario, it's not ideal for testing and is currently being 
        # ignored. TODO fix this. Not as simple as client.socket.getpeername()[1] == socket.getpeername()[1]
        if client.socket.getpeername()[0] == socket.getpeername()[0]:
            return client

def set_gamerules() -> None:
    """
    Configure all gamerule variables according to Banker user input. Repeats until successful. 
    
    Parameters: None

    Returns: None
    """
    global STARTING_CASH, num_players
    try:
        STARTING_CASH = ss.get_valid_int("Enter the amount of money each player starts with: ")
        num_players = ss.get_valid_int("Enter the number of players: ")
    except:
        print("Failed to set gamerules. Try again.")
        input()
        set_gamerules()

def monopoly_controller(unit_test) -> None:
    """
    Controls the flow of the Monopoly game.

    This function initializes the Monopoly game, waits for players to connect,
    and then enters a loop to manage turns. It sends the game board to the 
    current player and prompts them to roll the dice.

    This function does nothing if a Monopoly game is not set to play during Banker setup.

    Returns:
        None
    """
    add_to_output_area("Monopoly", "About to start Monopoly game.")
    if not play_monopoly:
        add_to_output_area("Monopoly", "No players in the game. Not attempting to run Monopoly.")
        return
    sleep(5) # Temporary sleep to give all players time to connect to the receiver TODO remove this and implement a better way to check all are connected to rcvr
    mply.unittest(unit_test)
    net.send_notif(clients[mply.turn].socket, mply.get_gameboard() + ss.set_cursor_str(0, 38) + "Welcome to Monopoly! It's your turn. Type roll to roll the dice.", "MPLY:")
    add_to_output_area("Monopoly", "Sent gameboard to player 0.")
    last_turn = 0
    while True:
        sleep(1)
        if mply.turn != last_turn:
            ss.set_cursor(0, 20)
            last_turn = mply.turn
            net.send_notif(clients[mply.turn].socket, mply.get_gameboard() + ss.set_cursor_str(0, 38) + "It's your turn. Type roll to roll the dice.", "MPLY:")
            clients[mply.turn].can_roll = True
            ss.set_cursor(ss.MONOPOLY_OUTPUT_COORDINATES[0]+1, ss.MONOPOLY_OUTPUT_COORDINATES[1]+1)
            add_to_output_area("Monopoly", f"Player turn: {mply.turn}. Sent gameboard to {clients[mply.turn].name}.")

def monopoly_game(client: Client = None, cmd: str = None) -> None:
    """
    Description:
        This is the main game loop for Monopoly.
        It will be called from the main function in its own thread. 
    Notes:
        Monopoly command looks like this: "mply,(action),(specific data),(even more specific data),(etc)" 

        player_roll all happens on the player side, so the player can handle all of that. 
        All data during player_roll will be sent to banker like the following:
        recv_message() -> handle_data() -> monopoly_game()
        Where monopoly_game parses the data and banker does not need to send anything back. 

        Now for player_choice, banker and player will do a bit more back and forth.
        Most of the game logic can be handled on the player side, but banker will
        have to preface the messages with cash, properties, etc. 
    """
    dice = (0, -1)
    if mply.players[mply.turn].name == client.name: # Check if the client who sent data is the current player 
                                                    #TODO restrict name values so identical names are disallowed
        action = cmd.split(',')[1]
        if action == None or action == '':
            ret_val = mply.request_roll()
            net.send_notif(client.socket, ret_val, "MPLY:")
        elif action == 'roll' and client.can_roll:
            dice = mply.roll()
            client.num_rolls += 1
            ret_val = mply.process_roll(client.num_rolls, dice)
            if ret_val.startswith("player_choice"):
                ret_val.replace("player_choice", "")
                client.can_roll = False
            net.send_notif(client.socket, ret_val, "MPLY:")
        elif action == 'trybuy': #TODO Better handling of locations would be nice. 
            mply.buy_logic("banker", "b")
            ret_val = mply.get_gameboard()
            # Need to check if doubles were rolled, otherwise end the rolling phase
            if dice[0] != dice[1]:
                client.can_roll = False
            net.send_notif(client.socket, ret_val, "MPLY:")
        elif action == 'propmgmt': #TODO This is almost complete. Still somewhat buggy.
            try: 
                property_id = cmd.split(',')[2]
            except:
                property_id = ""
            ret_val = mply.housing_logic(mply.players[0], "banker", property_id)
            net.send_notif(client.socket, ret_val, "MPLY:")
        elif action == 'deed': #TODO This is not yet complete. Very buggy. 
            try: 
                property_id = cmd.split(',')[2]
            except:
                property_id = ""
            mply.update_status(mply.players[0], "deed", [], "banker", property_id)
        elif action == 'continue':
            ret_val = mply.get_gameboard()
            net.send_notif(client.socket, ret_val, "MPLY:")
        elif action == 'endturn':
            mply.end_turn()
            ret_val = "ENDOFTURN" + mply.get_gameboard()
            net.send_notif(client.socket, ret_val, "MPLY:")

if __name__ == "__main__":

    os.system('cls' if os.name == 'nt' else 'clear')
    print("Welcome to Terminal Monopoly, Banker!")

    if "-skipcalib" not in sys.argv and "-local" not in sys.argv:
        ss.calibrate_screen('banker')

    if "-silent" in sys.argv:
        ss.VERBOSE = False

    set_unittest() 
    # set_gamerules()
    start_server()
    choose_colorset("DEFAULT_COLORS")
    ss.print_banker_frames()
    monopoly_unit_test = 6 # assume 1 player, 2 owned properties. See monopoly.py unittest for more options
    game = mply.start_game(STARTING_CASH, num_players, [clients[i].name for i in range(num_players)])
    threading.Thread(target=monopoly_controller, args=[monopoly_unit_test], daemon=True).start()
    start_receiver()

