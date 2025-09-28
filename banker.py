import itertools
from time import sleep
import sys
import os
# Start the loading animation in a separate thread
loading = True
def loading_animation(text="Loading"):
    for frame in itertools.cycle(['|', '/', '-', '\\']):
        if not loading:
            break
        sys.stdout.write(f'\r{text} {frame}')
        sys.stdout.flush()
        sleep(0.1)
    sys.stdout.write('\rLoading complete!     \n')
import threading
animation_thread = threading.Thread(target=loading_animation, args=["Loading imports"])
animation_thread.start()

# Python Builtin Utilities
import socket
import random
import select
import importlib

# Our Utilities
from style import MYCOLORS as COLORS, print_w_dots, choose_colorset
import screenspace as ss 
from screenspace import Trading_Output, Main_Output, Monopoly_Game_Output, Casino_Output
import gamemanager as gm
import networking as net
import validation as valid
from utils import Client
from loan import Loan

# Modules
import modules_directory.tictactoe as tictactoe
import modules_directory.inventory as inv

# Dynamically import handle functions from modules in modules_directory as handle_<module_name>
modules_path = "modules_directory"
for filename in os.listdir(modules_path):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = filename[:-3]  # Remove the .py extension
        module = importlib.import_module(f"{modules_path}.{module_name}")
        if hasattr(module, "handle"):
            globals()[f"handle_{module_name}"] = getattr(module, "handle")


# Monopoly Game
import monopoly_directory.monopoly as mply

# Stop the loading animation after imports are complete
loading = False
animation_thread.join()

STARTING_CASH = 1500
clients = []
server_socket = None
port = 3131
num_players = 0
play_monopoly = True
monopoly_unit_test = 6 # assume 1 player, 2 owned properties. See monopoly.py unittest for more options
messages = []
DEBT_OK = False

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

def start_receivers() -> None:
    """
    This function handles all client-to-server requests (not the other way around).
    Function binds an independent receiving socket at the same IP address, one port above. 
    For example, if the opened port was 3131, the receiver will open on 3132.  
    
    Parameters: None

    Returns: None
    """
    global port
    threading.Thread(target=receiver_loop, args=(port,), name="ReceiverThread").start() # Start the receiver loop in a separate thread
    threading.Thread(target=receiver_loop, args=(port, True), daemon=True, name="OOFReceiverThread").start() # Start the OOF receiver loop in a separate thread
    add_to_output_area("Main", "Receivers started!", COLORS.GREEN)  
    
def receiver_loop(port:int, is_oof_thread: bool = False) -> None:
    with socket.socket() as server:
        host = socket.gethostname()
        ip_address = socket.gethostbyname(host)
        if "-local" in sys.argv:
            ip_address = "localhost"
            port = 33333
        if is_oof_thread:
            server.bind((ip_address, int(port + 2)))
            add_to_output_area("Main", f"OOF Receiver accepting connections at {port+2}", COLORS.GREEN)
        else:
            server.bind((ip_address, int(port + 1)))
            add_to_output_area("Main", f"Receiver accepting connections at {port+1}", COLORS.GREEN)
        server.listen()
        # Credit to https://stackoverflow.com/a/43151772/19535084 for seamless server-client handling.
        to_read = [server]  # add server to list of readable sockets.
        while True:
            # check for a connection to the server or data ready from clients.
            # readers will be empty on timeout.
            readers,_,_ = select.select(to_read,[],[],0.1)
            for reader in readers:
                if reader is server:
                    player,address = reader.accept()
                    if not is_oof_thread:
                        add_to_output_area("Main", f"Player connected from: {address[0]}", COLORS.GREEN)
                    to_read.append(player) # add client to list of readable sockets
                else:
                    try:
                        data = net.receive_message(reader)
                        handle_data(data, reader)
                    except ConnectionResetError:
                        if not is_oof_thread:
                            add_to_output_area("Main", f"Player at {address[0]} disconnected.", COLORS.RED)
                        to_read.remove(reader) # remove from monitoring

                        # TODO send a message to each player to query who is still connected, then properly remove
                        # the disconnected player from the game. Currently only removing the first player in clients list. 
                        # clients.pop(0)

                    # if not data: # No data indicates disconnect
                    #     add_to_output_area("Main", f"Player at {address[0]} disconnected.", s.COLORS.RED)
                    #     to_read.remove(reader) # remove from monitoring
                if(len(to_read) == 1):
                    if not is_oof_thread:
                        if "-stayopen" not in sys.argv:
                            add_to_output_area("Main", "All connections dropped. Receiver stopped.", COLORS.GREEN)
                            return
                        else:
                            add_to_output_area("Main", "All connections dropped. Receiver will stay open.", COLORS.GREEN)
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
    global num_players, STARTING_CASH, play_monopoly, monopoly_unit_test
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

    Unit test 5: {COLORS.LIGHTBLUE}(Trading unit test, properties and cash available.){COLORS.RESET}:
    - num_players = 2
    - Does not start Monopoly game.
    - STARTING_CASH = 3000
    - Brown and Light Blue properties bought by player 0, Pink and Orange properties bought by player 1.
    
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
    elif (test == 2):
        play_monopoly = True
        num_players = 2
        STARTING_CASH = 1500
    elif (test == 3):
        play_monopoly = False
        num_players = 4
        STARTING_CASH = 100
    elif (test == 4):
        play_monopoly = False
        num_players = 1
        STARTING_CASH = 100 
    elif (test == 5):
        play_monopoly = False
        num_players = 2
        STARTING_CASH = 3000
        # Add properties to the players for testing purposes
        monopoly_unit_test = 5
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
    clients[id].PlayerObject.cash += delta
    return clients[id].PlayerObject.cash

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
        pid = int(data[0])
        current_client = clients[pid] # Assume the data is prefixed by the client number AKA player_id.
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

    # These handle functions are all defined in their respective modules as handle
    elif "chat" not in data and "inventory" in data: # Ensure the chat module is not being called
        handle_inventory(data, client, current_client.inventory)

    elif "chat" not in data and "shop" in data: # Ensure the chat module is not being called
        handle_shop(data, client, current_client.inventory, current_client.PlayerObject.cash, current_client.id, change_balance)

    elif data.startswith('deed'):
        handle_deed(data, client, mply)

    elif data.startswith("bal"):
        handle_balance(data, client, mply, current_client.PlayerObject.cash, current_client.PlayerObject.properties)

    elif data.startswith('casino'):
        handle_casino(data, client, change_balance, add_to_output_area, current_client.id, current_client.name, DEBT_OK)

    elif data.startswith('attack'):
        #run the attack similar to casino on client side and send game to player attacked, then send resulting command back
        handle_attack(data, current_client, client)

    elif data.startswith('loan'):
        handle_loan(data, client, change_balance, add_to_output_area, current_client.id, current_client.name)

    elif data.startswith('chat'):
        handle_chat(data, client, messages, current_client.id, current_client.name)

    elif data.startswith('trade'):
        handle_trading(data, pid, client, clients, add_to_output_area)
        
    elif data.startswith('plist'):
        handle_plist(client, clients)
        
    elif data.startswith('term_status'):
        command_data = data.split(' ')
        term = int(command_data[1])
        net.send_message(client, str(current_client.terminal_statuses[term]))

    elif data.startswith('fish'):
        handle_fishing(client,  current_client.inventory)

    elif data.startswith('kill') or data.startswith('disable') or data.startswith('active') or data.startswith('busy'):
        """
        Should be called by a player (1) to disable another player (2).
        Player 1 expects value of success/fail (busy or already dead).
        Player 2 doesn't know unless it is successful.
        """
        handle_term(data, current_client, client)
def handle_attack(cmds: str, current_client: Client, client: socket.socket) -> None:
    net.send_message(client, "\nInvalid you")
    """
    Command Structure:
        action player term length
        (Ex. Attack 0 5 15 1)

    Args:
        action: Type of action (attack)
        player: ID of player attacked
        pType:penalty game (e.g. guessing game)
        pNum: penalty amount
        player: ID of player attacking
    """
    command_data = cmds.split(' ')
    if(command_data[0] == 'attack'):
        #send game to opponent
        #add_to_output_area("", f"attack status")
        opponent = int(command_data[1])
        attacker = int(command_data[4])
        try:
            if len(clients) <= opponent or clients[opponent] == None or clients[opponent] == clients[attacker]:
                net.send_message(client, "\nInvalid opponent. Please select another player.")
                return
        except:
            net.send_message(client, "\nInvalid opponent. Please select another player.")
        if str(command_data[2].strip()) == 'lose':
            money = change_balance(opponent, 0 - (int(command_data[3])))
            net.send_message(clients[opponent].socket, str(money))
            money = change_balance(attacker, int(command_data[3]))
            net.send_message(clients[attacker].socket, str(money))
            add_to_output_area("",
                               f"{clients[opponent].name}'s balance was reduced by {command_data[3]} as a result of an attack %. Current Statuses: {clients[opponent].money}")
            add_to_output_area("",
                               f"{clients[attacker].name}'s balance was increased by {command_data[3]} as a result of an attack %. Current Statuses: {clients[attacker].money}")
        else:
            try:
                #check if game works
                i = __import__('attack_modules.' + command_data[2], fromlist=[''])
                if((int(command_data[3])) < 1):
                    net.send_message(client, "\nInvalid penalty amount")
                    return

                else:
                    #set attack penalty on opponent balance (need to transfer)
                    add_to_output_area("", f"{clients[opponent].name} has been attacked")
                    net.send_notif(clients[opponent].socket, command_data[4] + " " + command_data[2] + " " + command_data[3], "ATTACK: ")
                    return

                    #clients[opponent].balance += amount

                    #net.send_message(client, "\nPenalty applied.")

            except ImportError:
                net.send_message(client, "\nInvalid attack. Please select another attack.")
                return





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
        
        clients.append(Client(client_socket, None, name, inv.Inventory())) # Append the client to the list of clients with a temporary id of None

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
    It will still purchase properties and change player cash, though, if specified in the unit test.

    Returns:
        None
    """
    add_to_output_area("Monopoly", "About to start Monopoly game.")
    mply.unittest(unit_test)

    if not play_monopoly:
        add_to_output_area("Monopoly", "No players in the game. Not attempting to run Monopoly.")
        ss.set_cursor(25, 5)
        print("Error: Monopoly game not started.")
        return
    sleep(5) # Temporary sleep to give all players time to connect to the receiver TODO remove this and implement a better way to check all are connected to rcvr
    net.send_notif(clients[mply.turn].socket, mply.get_gameboard() + ss.set_cursor_str(0, 38) + "Welcome to Monopoly! It's your turn. Type roll to roll the dice.", "MPLY:")
    add_to_output_area("Monopoly", "Sent gameboard to player 0.")
    last_turn = 0
    while True:
        sleep(1)
        if mply.turn != last_turn:
            # if disconnect, move to next player
            try:
                ss.set_cursor(0, 20)
                last_turn = mply.turn
                net.send_notif(clients[mply.turn].socket, mply.get_gameboard() + ss.set_cursor_str(0, 38) + "It's your turn. Type roll to roll the dice.", "MPLY:")
                clients[mply.turn].can_roll = True
                # ss.set_cursor(ss.MONOPOLY_OUTPUT_COORDINATES[0]+1, ss.MONOPOLY_OUTPUT_COORDINATES[1]+1)
                add_to_output_area("Monopoly", f"Player turn: {mply.turn}. Sent gameboard to {clients[mply.turn].name}.")
            except:
                add_to_output_area("Monopoly", f"Player turn: {mply.turn}. Disconnected")
                mply.end_turn()
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
        elif action == 'endturn' and not client.can_roll:
            mply.end_turn()
            ret_val = "ENDOFTURN" + mply.get_gameboard()
            net.send_notif(client.socket, ret_val, "MPLY:")

def handle_loan(data: str, client_socket: socket.socket, change_balance: callable, add_to_output_area: callable, player_id: int, player_name: str) -> None:

    """
    Handles loan requests from players.
    
    Args:
        data (str): The loan command string containing loan details.
                    Expected format: "loan [loan_type] [amount]"
        client_socket (socket): The socket connection to the client.
        change_balance (function): Function to change the client's balance.
        add_to_output_area (function): Function to add messages to the output area.
        player_id (int): The ID of the client requesting the loan.
        player_name (str): The name of the client requesting the loan.
    
    Returns:
        None
    """
    try:
        # Parse the loan command: "loan [loan_type] [amount]"
        command_data = data.split(' ')
        
        if len(command_data) != 3:
            net.send_message(client_socket, "Invalid loan request format.")
            return
            
        loan_type = command_data[1]  # "high" or "low"
        amount = int(command_data[2])
        
        # Validate loan parameters
        if loan_type == "high":
            if amount <= 0 or amount > 2000:
                net.send_message(client_socket, "High interest loans must be between $1 and $2000.")
                return
            player_loan = Loan(amount, True)
            
        elif loan_type == "low":
            if amount <= 0 or amount > 500:
                net.send_message(client_socket, "Low interest loans must be between $1 and $500.")
                return
            play_loan = Loan(amount, False)
            
        else:
            net.send_message(client_socket, "Invalid loan type. Choose 'high' or 'low'.")
            return
        
        # Calculate the total amount to be repaid (for informational purposes)
        total_repayment = int(amount * (1 + interest_rate))
        
        # Add the loan amount to the player's balance
        new_balance = change_balance(player_id, amount)
        
        # Log the transaction
        add_to_output_area("Loans", f"{player_name} took out a {loan_type} interest loan of ${amount}. New balance: ${new_balance}")
        
        # Send confirmation message back to the client
        response = f"Loan approved! You received ${amount}.\nYou will need to repay ${total_repayment} (${amount} + {int(interest_rate*100)}% interest).\nYour new balance is ${new_balance}."
        net.send_message(client_socket, response)
        
    except (ValueError, IndexError) as e:
        add_to_output_area("Loans", f"Error processing loan for {player_name}: {str(e)}", COLORS.RED)
        net.send_message(client_socket, "Error processing loan request. Please try again.")

if __name__ == "__main__":

    os.system('cls' if os.name == 'nt' else 'clear')
    print("Welcome to Terminal Monopoly, Banker!")

    if "-skipcalib" not in sys.argv and "-local" not in sys.argv:
        ss.calibrate_screen('banker')

    if "-silent" in sys.argv:
        ss.VERBOSE = False

    if "-debtok" in sys.argv:
        DEBT_OK = True

    set_unittest() 
    # set_gamerules()
    start_server()
    choose_colorset("DEFAULT_COLORS")
    game = mply.start_game(STARTING_CASH, num_players, [clients[i].name for i in range(num_players)], clients)
    ss.print_banker_frames()
    threading.Thread(target=monopoly_controller, args=[monopoly_unit_test], daemon=True).start()
    start_receivers()