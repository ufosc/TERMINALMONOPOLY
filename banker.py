import socket
import threading
import os
import sys
import random

from style import MYCOLORS as COLORS, print_w_dots
import screenspace as ss 

import gamemanager as gm
import networking as net
import validation as valid

import modules_directory.tictactoe as tictactoe

import monopoly as mply

import select
from time import sleep

STARTING_CASH = 1500
clients = []
port = 3131
num_players = 0
play_monopoly = True

TTT_Output = ss.OutputArea("TicTacToe", ss.TTT_OUTPUT_COORDINATES, 36, 9)
Casino_Output = ss.OutputArea("Casino", ss.CASINO_OUTPUT_COORDINATES, 36, 22)
Monopoly_Game_Output = ss.OutputArea("Monopoly", ss.MONOPOLY_OUTPUT_COORDINATES, 191, 6)
Main_Output = ss.OutputArea("Main", ss.MAIN_OUTPUT_COORDINATES, 79, 12)

class Client:
    def __init__(self, socket: socket.socket, id: int, name: str, money: int, properties: list):
        self.socket = socket
        self.id = id
        self.name = name
        self.money = money
        self.properties = properties
        self.can_roll = True
        self.num_rolls = 0

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
    global clients, port
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
    print_w_dots("Game is full. Starting game...")
    print_w_dots("")
    print_w_dots("")
    print_w_dots("")
    # Send a message to each client that the game is starting, allowing them to see their terminals screen
    for i in range(len(clients)): 
        clients[i].id = i
        net.send_message(clients[i].socket, f"Game Start!{num_players} {i}")
        sleep(0.5)
    return server_socket

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
                    if not data: # No data indicates disconnect
                        add_to_output_area("Main", f"Player at {address[0]} disconnected.", COLORS.RED)
                        to_read.remove(reader) # remove from monitoring
                if(len(to_read) == 1):
                    add_to_output_area("Main", "[RECEIVER] All connections dropped. Receiver stopped.", COLORS.GREEN)
                    return

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

def change_balance(id: int, delta: int): 
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

    add_to_output_area("Main", f"Received data from {current_client.name}: {data}")
    
    if data == 'request_board': 
        net.send_message(client, mply.get_gameboard())
    
    elif data.startswith('request_info'):
        pass

    if data.startswith("deed"):
        cmds = data.split(' ') 
        location = int(cmds[1])
        property_data = mply.get_deed(location)
        deed_str = property_data.get_deed_str(True)

        net.send_message(client, deed_str)

    elif data.startswith('mply'):
        monopoly_game(current_client, data)

    # elif data == 'ships':

        # handle_battleship(data, current_client)

    elif data.startswith('ttt'):
        handle_ttt(data, current_client)

    elif data.startswith('bal'):
        """
        Return the client's balance.
        """
        net.send_message(client, str(current_client.money))

    elif data.startswith('casino'):
        handle_casino(data, current_client)
        net.send_message(client, str(current_client.money))

def handle_casino(cmds: str, current_client: Client) -> None:
    """
    Handles casino-related commands for a client by updating their balance.

    Args:
        cmds (str): The command string containing the casino operation details.
                    Expected format: "casino [casino_id] [change_balance]"
                    - [delta] (str): The player's win or loss string.
                    - [change_balance] (int): The amount to change the client's balance by.
        current_client (Client): The client whose balance is to be updated.

    Returns:
        None

    Example:
        handle_casino("casino win 100", client)
        This will add 100 to the client's balance.
    """
    command_data = cmds.split(' ')
    delta = 1 if command_data[1] == 'win' else -1
    amount = int(command_data[2])
    change_balance(current_client.id, delta * amount)
    add_to_output_area("Casino", f"Updated {current_client.name}'s balance by {delta * amount}. New balance: {current_client.money}")

def handle_ttt(cmds: str, current_client: Client) -> None:
    """
    Handles all TicTacToe requests from the player.
    
    Parameters:
        cmds (str): The command string from the player.
        current_client (Client): The client object associated with the player.
    
    Returns:
        None
    """
    ttt_game = None
    add_to_output_area("TicTacToe", "TicTacToe data requested!")
    if cmds.split(',')[1] == 'getgamestate':
        # Joining a game logic
        # Game does not exist
        if gm.player_in_game('TicTacToe', current_client.name) == True:
            if len(gm.get_game_by_name('TicTacToe')) >= 1:
                add_to_output_area("TicTacToe", "Player is already playing at least one game, need to select a specific game to rejoin.")
                net.send_message(current_client.socket, "\nPlease select a game to join.\n" + gm.display_games(name='TicTacToe', player_name=current_client.name))
        # Player is not in any games
        else: 
            add_to_output_area("TicTacToe", f"Player is not in any games. Can create a game.")
            # Ask player first, then create a game if they want to play.
            sleep(1)
            net.send_message(current_client.socket, "\nYou are not part of any games.\nWould you like to create a new TicTacToe game?\nEnter -1 to create, or 0 to ignore.")
            net.send_notif(current_client.socket, "You are not part of any games. Would you like to create a new TicTacToe game? Enter -1 to create, or 0 to ignore.")
        return

    if cmds.split(',')[1] == 'joingame':
    # Player knows game exists, and is trying to (re)join a game
        game_id = int(cmds.split(',')[2])

        if game_id == -1: # Create a new game.
            # Don't let a player create a new game if they're already in one.. This might be adjusted later TODO debug
            if gm.player_in_game('TicTacToe', current_client.name) == True:
                if len(gm.get_game_by_name('TicTacToe')) >= 1:
                    add_to_output_area("TicTacToe", "Player input -1 when already playing another game, need to select a specific game to rejoin.")
                    net.send_message(current_client.socket, "\nYou're playing a game already! Rejoin from the game list.\n" + gm.display_games(name='TicTacToe', player_name=current_client.name))
                    return
            else: 
                opponent = int(cmds.split(',')[3])
                # Check if valid opponent inputted
                if len(clients) <= opponent or clients[opponent] == None or clients[opponent] == current_client:
                    net.send_message(current_client.socket, "\nInvalid opponent. Please select another player.")
                    return

                add_to_output_area("TicTacToe", "Creating new TicTacToe game.")
                ttt_game = tictactoe.TicTacToe()
                gm.add_game(gm.Game('TicTacToe', [None] * 2, ttt_game.board, ttt_game))
                game_id = len(gm.games)-1
                gm.get_game_by_id(len(gm.games)-1).players[0] = current_client # Should be able to safely assume that the last game in the list is the one we just created.
                gm.get_game_by_id(len(gm.games)-1).players[1] = clients[opponent] # Second player
                net.send_notif(clients[opponent].socket, f'{current_client.name} is attacking you in TicTacToe!')
                add_to_output_area("TicTacToe", "Game created.")
                add_to_output_area("TicTacToe", f'{current_client.name} joined game with id {len(gm.games)-1}.')
        
        queried_game = gm.get_game_by_id(game_id)
        if queried_game: # Game requested by ID exists
            if queried_game.name == 'TicTacToe' and len(queried_game.players) < queried_game.MAXPLAYERS:
                # Game is a TicTacToe game and has space for another player
                # Note that this means a player can accidentally join a game they're not supposed to
                # if they know the game ID. This is a security flaw. TODO fix this
                gm.add_player_to_game(game_id, current_client.name)
                add_to_output_area("TicTacToe", f'Player {current_client.name} joined game.')
                
                ttt_game = gm.get_game_by_id(game_id)

            elif queried_game.name == 'TicTacToe' and current_client.name in [player.name for player in queried_game.players]:
                # Player is already in the game. Let them rejoin and continue playing with the same game object.
                add_to_output_area("TicTacToe", f'Player rejoined game with ID {game_id}.')
                ttt_game = queried_game

            elif queried_game.name != 'TicTacToe':
                # Player tried to join a game that isn't TicTacToe
                add_to_output_area("TicTacToe", f"[{current_client.name}] Incorrect game name.")
                net.send_message(current_client.socket, "\nIncorrect game name. Please select another game.")
            elif len(queried_game.players) >= queried_game.MAXPLAYERS:
                # Game is full
                add_to_output_area("TicTacToe", f"[{current_client.name}] Game full.")
                net.send_message(current_client.socket, "\nGame is full. Please select another game.")
            else: # Edge case handling. Not strictly necessary or helpful, so remove in the future if it's not needed.
                add_to_output_area("TicTacToe", f"[{current_client.name}] Something else went wrong. Game not found.")
        else: 
            add_to_output_area("TicTacToe", f"[{current_client.name}] Game not found.")
    else: 
        pass
    
    # We should have a game object by now. If we don't, something went wrong.
    if cmds.split(',')[1] == 'move':
        if ttt_game == None: # We know the player is validly in a game, so we can get the game object
            ttt_game = gm.get_game_by_id(int(cmds.split(',')[2]))

        if type(ttt_game) == gm.Game:
            ttt_game_object = ttt_game.other_data # Get the actual *specific* game object from the Game object (in this case, the TicTacToe object)
        # Now check for moves
        if cmds.split(',')[1] == 'move':
            if (ttt_game_object.current_player == 'O' and current_client.name == ttt_game.players[0].name) \
            or (ttt_game_object.current_player == 'X' and current_client.name == ttt_game.players[1].name):
                net.send_message(current_client.socket, "It's not your turn!")
                return "It's not your turn!"
            ttt_game_object.place(int(cmds.split(',')[3].split('.')[0]), int(cmds.split(',')[3].split('.')[1]))
            if ttt_game_object.check_winner():
                net.send_message(current_client.socket, "You win!")
                gm.remove_game(ttt_game.id)
                return "You win!"
            elif ttt_game_object.is_full():
                net.send_message(current_client.socket, "It's a tie!")
                gm.remove_game(ttt_game.id)
                return "It's a tie!"
            else:
                ttt_game_object.current_player = 'O' if ttt_game_object.current_player == 'X' else 'X'
                if current_client.name == ttt_game.players[0].name:
                    net.send_notif(ttt_game.players[1].socket, f'TTT: {current_client.name} has made a move!')
                elif current_client.name == ttt_game.players[1].name:
                    net.send_notif(ttt_game.players[0].socket, f'TTT: {current_client.name} has made a move!')
        
        # Send the board to the player
    if ttt_game != None:
        net.send_message(current_client.socket, tictactoe.construct_board(ttt_game.board))

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
        
        clients.append(Client(client_socket, None, name, 2000, [])) # Append the client to the list of clients with a temporary id of None

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

def monopoly_controller() -> None:
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
    mply.unittest()
    net.send_monopoly(clients[mply.turn].socket, mply.get_gameboard() + ss.set_cursor_str(0, 38) + "Welcome to Monopoly! It's your turn. Type roll to roll the dice.")
    add_to_output_area("Monopoly", "Sent gameboard to player 0.")
    last_turn = 0
    while True:
        sleep(1)
        if mply.turn != last_turn:
            ss.set_cursor(0, 20)
            last_turn = mply.turn
            net.send_monopoly(clients[mply.turn].socket, mply.get_gameboard() + ss.set_cursor_str(0, 38) + "It's your turn. Type roll to roll the dice.")
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
            net.send_monopoly(client.socket, ret_val)
        elif action == 'roll' and client.can_roll:
            dice = mply.roll()
            client.num_rolls += 1
            ret_val = mply.process_roll(client.num_rolls, dice)
            if ret_val.startswith("player_choice"):
                ret_val.replace("player_choice", "")
                client.can_roll = False
            net.send_monopoly(client.socket, ret_val)
        elif action == 'trybuy': #TODO Better handling of locations would be nice. 
            mply.buy_logic("banker", "b")
            ret_val = mply.get_gameboard()
            # Need to check if doubles were rolled, otherwise end the rolling phase
            if dice[0] != dice[1]:
                client.can_roll = False
            net.send_monopoly(client.socket, ret_val)
        elif action == 'propmgmt': #TODO This is almost complete. Still somewhat buggy.
            try: 
                property_id = cmd.split(',')[2]
            except:
                property_id = ""
            ret_val = mply.housing_logic(mply.players[0], "banker", property_id)
            net.send_monopoly(client.socket, ret_val)
        elif action == 'deed': #TODO This is not yet complete. Very buggy. 
            try: 
                property_id = cmd.split(',')[2]
            except:
                property_id = ""
            mply.update_status(mply.players[0], "deed", [], "banker", property_id)
        elif action == 'continue':
            ret_val = mply.get_gameboard()
            net.send_monopoly(client.socket, ret_val)
        elif action == 'endturn':
            mply.end_turn()
            ret_val = "ENDOFTURN" + mply.get_gameboard()
            net.send_monopoly(client.socket, ret_val)

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
    ss.print_banker_frames()
    game = mply.start_game(STARTING_CASH, num_players, [clients[i].name for i in range(num_players)])
    threading.Thread(target=monopoly_controller, daemon=True).start()
    start_receiver()
