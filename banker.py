import socket
import threading
import os
import random
import sys
import io

import style as s
import screenspace as ss 

import gamemanager as gm
import networking as net

import modules_directory.tictactoe as tictactoe
import modules_directory.battleship as battleship

import monopoly as mply

import select
from time import sleep

bank_cash = 100000
starting_cash = 1500
clients = []
port = 3131
num_players = 0

timer = 0

class Client:
    def __init__(self, socket: socket.socket, name: str, money: int, properties: list):
        self.socket = socket
        self.name = name
        self.money = money
        self.properties = properties
        self.can_roll = True
        self.num_rolls = 0

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

    # Get local machine name
    host = socket.gethostname()
    ip_address = socket.gethostbyname(host)

    # Choose a port that is free
    # port = int(input("Choose a port, such as 3131: "))
    port = 3131

    # Bind to the port
    server_socket.bind((host, port))
    s.print_w_dots(f"Server started on {ip_address} port {port}")
    server_socket.listen()

    s.print_w_dots("Waiting for clients...")
    
    handshakes = [False] * num_players

    game_full = False
    while not game_full:
        # Accepts connections while there are less than <num_players> players
        if len(clients) < num_players:
            client_socket, addr = server_socket.accept()
            print(f"Got a connection from {addr}")
            client_handler = threading.Thread(target=handshake, args=(client_socket,handshakes))
            client_handler.start()
        else: 
            game_full = True
        sleep(0.5) 
    s.print_w_dots("Game is full. Starting game...")
    s.print_w_dots("")
    s.print_w_dots("")
    s.print_w_dots("")
    # Send a message to each client that the game is starting, allowing them to see their terminals screen
    for i in range(len(clients)): 
        net.send_message(clients[i].socket, f"Game Start!{num_players} {i+1}")
        sleep(0.5)
    return server_socket

def start_receiver():
    """
    This function handles all client-to-server requests (not the other way around).
    Function binds an independent receiving socket at the same IP address, one port above. 
    For example, if the opened port was 3131, the receiver will open on 3132.  
    
    Parameters: None
    Returns: None
    """
    global player_data, timer, port
    s.print_w_dots('[RECEIVER] Receiver started!') 
    # Credit to https://stackoverflow.com/a/43151772/19535084 for seamless server-client handling. 
    with socket.socket() as server:
        host = socket.gethostname()
        ip_address = socket.gethostbyname(host)
        server.bind((ip_address,int(port+1)))
        server.listen()
        s.print_w_dots('[RECEIVER] Receiver accepting connections at {}'.format(port+1))
        to_read = [server]  # add server to list of readable sockets.
        while True:
            # check for a connection to the server or data ready from clients.
            # readers will be empty on timeout.
            readers,_,_ = select.select(to_read,[],[],0.1)
            for reader in readers:
                if reader is server:
                    player,address = reader.accept()
                    # Client(player, 'Player', starting_cash, [])
                    s.print_w_dots('Player connected from: ' + address[0])
                    to_read.append(player) # add client to list of readable sockets
                else:
                    try:
                        data = net.receive_message(reader)
                        handle_data(data, reader)
                    except ConnectionResetError:
                        s.print_w_dots(f'Player at {address[0]} disconnected.')
                        to_read.remove(reader) # remove from monitoring
                    if not data: # No data indicates disconnect
                        s.print_w_dots(f'Player at {address[0]} disconnected.')
                        to_read.remove(reader) # remove from monitoring
                if(len(to_read) == 1):
                    s.print_w_dots('[RECEIVER] All connections dropped. Receiver stopped.')
                    return
            print(f'{s.set_cursor_str(0, os.get_terminal_size().lines-3)}{s.COLORS.backBLUE}Time passed since last command: {timer}. ',flush=True,end=f'\r{s.COLORS.RESET}')
            timer += 1

def unittest(test: int):
    """
    Unit test function for the Banker module.
    Add here as you think of more tests.
    """
    global num_players
    match test:
        case 1:
            print("Running unittest1")
            num_players = 2
            gm.add_game(gm.Game('Battleship', [Client(None, "Null", 0, [])] * 4, 'board', 'other_data'))
            gm.add_game(gm.Game('Battleship', [Client(None, None, 0, [])] * 2, 'board', 'other_data'))
            gm.add_game(gm.Game('Battleship', [Client(None, "Name", 0, [])] * 3, 'board', 'other_data'))
            gm.add_game(gm.Game('TicTacToe', [Client(None, "nada", 0, [])] * 2, 'board', None))
        case 2:
            gm.add_game(gm.Game('Fake Game', [Client(None, "Null", 0, [])] * 4, 'board', 'other_data'))
            num_players = 1
        case _:
            print("Invalid test number.")
            print("Running unittest2")
            unittest(2)
    
def handle_data(data: bytes, client: socket.socket) -> str:
    """
    Handles all data received from player sockets. 
    
    Parameters:
    data (str) Data received from player sockets. 
    
    Returns:
    str representing the response to the player's data. 
    """
    global timer
    current_client = get_client_by_socket(client)
    decoded_data = data

    print(f"Received data from {current_client.name}: {data}")
    
    # current_client.data_queue.put(decoded_data)

    if decoded_data == 'request_board': 
        net.send_message(client, mply.get_gameboard())
        s.print_w_dots(f'Gameboard sent to player {client}')

    elif decoded_data.startswith('mply'):
        monopoly_game(current_client, decoded_data)

    elif decoded_data == 'ships':
        if gm.game_exists('Battleship') == False:
            s.print_w_dots('No active games to join.')
            number_of_players = 1
            s.print_w_dots(f'Creating new Battleship with {number_of_players} players.')
            battleship_game_object = battleship.start_game()
            battleship_game = gm.Game('Battleship', [-1] * number_of_players, battleship_game_object.board, battleship_game_object)
            gm.add_game(battleship_game)
            s.print_w_dots('Game created.')
            battleship_game_object.player_names.append(current_client.name)
            s.print_w_dots(f'{current_client.name} joined game.')
            net.send_message(client, battleship_game_object.generate_water_and_coords())
            
        elif gm.player_in_game('Battleship', current_client.name) == True:
            if len(gm.get_game_by_name('Battleship')) >= 1:
                print(f'{current_client.name} is already playing at least one game, need to select a specific game to rejoin.')
                net.send_message(client, gm.display_games(name='Battleship', player_name=current_client.name))

        else: # should only appear if player is in multiple games
            net.send_message(client, gm.display_games())

        # battleship_board =  + battleship_game.popup("Players: " + str(gm.get_game_by_id(0).other_data.player_names))
        # print(battleship_board)
        # print("Current size of Battleship board (if over 10^10, broken): ", len(battleship_board))
        # net.send_message(client, battleship_board)
        # s.print_w_dots(f'Gameboard sent to player {client}')
    elif decoded_data.startswith('bal '):
        """
        Gets and changes client's balance.
        The second parameter is added to the value of the client's balance.
        Use 0 to simply get the balance.
        """
        command_data = decoded_data.split(' ')
        current_client.money += int(command_data[1])
        net.send_message(client, str(current_client.money))

    elif decoded_data.startswith('ttt'):
        ttt_game = None
        ttt_location_info = s.set_cursor_str(random.randint(0, 100), random.randint(0, 40)) + random.choice([s.COLORS.dispBLUE, s.COLORS.dispGREEN, s.COLORS.dispRED]) # just throw the information somewhere on the screen
        print(ttt_location_info + "TicTacToe data requested!")
        if decoded_data.split(',')[1] == 'getgamestate':
            # Joining a game logic
            # Game does not exist
            if gm.player_in_game('TicTacToe', current_client.name) == True:
                if len(gm.get_game_by_name('TicTacToe')) >= 1:
                    print(f"{ttt_location_info}Player is already playing at least one game, need to select a specific game to rejoin.")
                    net.send_message(client, "\nPlease select a game to join.\n" + gm.display_games(name='TicTacToe', player_name=current_client.name))
            # Player is not in any games
            else: 
                print(f"{ttt_location_info}TTT: Player is not in any games. Can create a game.")
                # Should not automatically create a game if the player is not in any games.. 
                # Ask player first, then create a game if they want to play.
                net.send_message(client, "\nYou are not part of any games.\nWould you like to create a new TicTacToe game?\nEnter -1 to create, or 0 to ignore.")
            return

        if decoded_data.split(',')[1] == 'joingame':
        # Player knows game exists, and is trying to (re)join a game
            game_id = int(decoded_data.split(',')[2])

            if game_id == -1: # Create a new game.
                # Don't let a player create a new game if they're already in one.. This might be adjusted later TODO debug
                if gm.player_in_game('TicTacToe', current_client.name) == True:
                    if len(gm.get_game_by_name('TicTacToe')) >= 1:
                        print(f"{ttt_location_info}Player input -1 when already playing another game, need to select a specific game to rejoin.")
                        net.send_message(client, "\nYou're playing a game already! Rejoin from the game list.\n" + gm.display_games(name='TicTacToe', player_name=current_client.name))
                        return
                else: 
                    opponent = int(decoded_data.split(',')[3])
                    # Check if valid opponent inputted
                    if len(clients) <= opponent or clients[opponent] == None or clients[opponent] == current_client:
                        net.send_message(client, "\nInvalid opponent. Please select another player.")
                        return

                    s.print_w_dots('Creating new TicTacToe game.')
                    ttt_game = tictactoe.TicTacToe()
                    gm.add_game(gm.Game('TicTacToe', [None] * 2, ttt_game.board, ttt_game))
                    game_id = len(gm.games)-1
                    gm.get_game_by_id(len(gm.games)-1).players[0] = current_client # Should be able to safely assume that the last game in the list is the one we just created.
                    gm.get_game_by_id(len(gm.games)-1).players[1] = clients[opponent] # Second player
                    net.send_notif(clients[opponent].socket, f'{current_client.name} is attacking you in TicTacToe!')
                    s.print_w_dots('Game created.')
                    s.print_w_dots(f'{current_client.name} joined game with id {len(gm.games)-1}.')
            
            queried_game = gm.get_game_by_id(game_id)
            if queried_game: # Game requested by ID exists
                if queried_game.name == 'TicTacToe' and len(queried_game.players) < queried_game.MAXPLAYERS:
                    # Game is a TicTacToe game and has space for another player
                    # Note that this means a player can accidentally join a game they're not supposed to
                    # if they know the game ID. This is a security flaw. TODO fix this
                    gm.add_player_to_game(game_id, current_client.name)
                    s.print_w_dots(f'Player {current_client.name} joined game.')
                    
                    ttt_game = gm.get_game_by_id(game_id)

                elif queried_game.name == 'TicTacToe' and current_client.name in [player.name for player in queried_game.players]:
                    # Player is already in the game. Let them rejoin and continue playing with the same game object.
                    s.print_w_dots(f'\n\n\nTTT: Player rejoined game with ID {game_id}.')
                    ttt_game = queried_game

                elif queried_game.name != 'TicTacToe':
                    # Player tried to join a game that isn't TicTacToe
                    s.print_w_dots('\n\n\nTTT: Incorrect game name.')
                    net.send_message(client, "\nIncorrect game name. Please select another game.")
                elif len(queried_game.players) >= queried_game.MAXPLAYERS:
                    # Game is full
                    s.print_w_dots('\n\n\nTTT: Game full.')
                    net.send_message(client, "\nGame is full. Please select another game.")
                else: # Edge case handling. Not strictly necessary or helpful, so remove in the future if it's not needed.
                    s.print_w_dots('\n\n\nTTT: Something else went wrong. Game not found.')
            else: 
                s.print_w_dots('\n\n\nTTT: Game not found.')
        else: 
            pass
        
        # We should have a game object by now. If we don't, something went wrong.
        if decoded_data.split(',')[1] == 'move':
            if ttt_game == None: # We know the player is validly in a game, so we can get the game object
                ttt_game = gm.get_game_by_id(int(decoded_data.split(',')[2]))

            if type(ttt_game) == gm.Game:
                ttt_game_object = ttt_game.other_data # Get the actual *specific* game object from the Game object (in this case, the TicTacToe object)
            # Now check for moves
            if decoded_data.split(',')[1] == 'move':
                if (ttt_game_object.current_player == 'O' and current_client.name == ttt_game.players[0].name) \
                or (ttt_game_object.current_player == 'X' and current_client.name == ttt_game.players[1].name):
                    net.send_message(client, "It's not your turn!")
                    return "It's not your turn!"
                ttt_game_object.place(int(decoded_data.split(',')[3].split('.')[0]), int(decoded_data.split(',')[3].split('.')[1]))
                if ttt_game_object.check_winner():
                    net.send_message(client, "You win!")
                    gm.remove_game(ttt_game.id)
                    return "You win!"
                elif ttt_game_object.is_full():
                    net.send_message(client, "It's a tie!")
                    gm.remove_game(ttt_game.id)
                    return "It's a tie!"
                else:
                    ttt_game_object.current_player = 'O' if ttt_game_object.current_player == 'X' else 'X'
                    if current_client.name == ttt_game.players[0].name:
                        net.send_notif(ttt_game.players[1].socket, f'TTT: {current_client.name} has made a move!')
                    elif current_client.name == ttt_game.players[1].name:
                        net.send_notif(ttt_game.players[0].socket, f'TTT: {current_client.name} has made a move!')
            
            # Send the board to the player
            # net.send_message(client, tictactoe.construct_board(ttt_game.board))
        if ttt_game != None:
            net.send_message(client, tictactoe.construct_board(ttt_game.board))

    timer = 0

def handshake(client_socket: socket.socket, handshakes: list):
    """
    As players connect, they attempt to handshake the server, this function handles that and 
    only starts the game once 4 handshakes have been successfully resolved. 
    
    Parameters:
    client_socket (socket.socket) Server sender socket which players connect to at game
        initialization. 
    handshakes (list) Boolean list of successful handshakes. By default, all values are false.  
    """
    global clients
    # Attempt handshake
    net.send_message(client_socket, "Welcome to the game!")
    message = net.receive_message(client_socket)
    if message == "Connected!":
        handshakes[len(clients)-1] = True
        clients.append(Client(client_socket, f'Player {len(clients)+1}', 2000, []))
        clients[len(clients)-1].name = input(f"{s.COLORS.backGREEN}{s.set_cursor_str(70,25)}What is this player's name?{s.COLORS.RESET}\n")  

        # If the player doesn't enter a name, assign a default name.
        # Also blacklist other illegal names here that would break the game.
        if clients[len(clients)-1].name == "" or clients[len(clients)-1].name == "PAD ME PLEASE!":
            clients[len(clients)-1].name = f"Player {len(clients)}"   
    else: 
        handshakes[len(clients)-1] = False

def get_client_by_socket(socket: socket.socket) -> Client:
    """
    Returns the client object associated with the given socket. 
    
    Parameters:
    socket (socket.socket) The socket of the client. 
    
    Returns:
    Client object associated with the given socket. 
    """
    for client in clients:
        # Only checking the IP address for now. This will not work if two clients are on the same IP address.
        # Think: locally testing. This has proven to be an issue while testing tic tac toe on the same machine.
        # While this should work in a real-world scenario, it's not ideal for testing and is currently being 
        # ignored. TODO fix this. Not as simple as client.socket.getpeername()[1] == socket.getpeername()[1]
        print(f"Comparing {client.socket.getpeername()} to {socket.getpeername()}")
        if client.socket.getpeername()[0] == socket.getpeername()[0]:
            return client

def set_gamerules() -> None:
    """
    Configure all gamerule variables according to Banker user input. Repeats until successful. 
    
    Parameters: None
    Returns: None
    """
    global bank_cash, starting_cash, num_players
    try:
        bank_cash = ss.get_valid_int("Enter the amount of money the bank starts with: ")
        starting_cash = ss.get_valid_int("Enter the amount of money each player starts with: ")
        num_players = ss.get_valid_int("Enter the number of players: ")
    except:
        print("Failed to set gamerules. Try again.")
        input()
        set_gamerules()

def monopoly_controller() -> None:
    print("About to start Monopoly game.")
    sleep(5) # Temporary sleep to give all players time to connect to the receiver TODO remove this and implement a better way to check all are connected to rcvr
    net.send_monopoly(clients[mply.turn].socket, mply.get_gameboard() + ss.set_cursor_str(0, 38) + "Welcome to Monopoly! It's your turn. Type roll to roll the dice.")
    print("Sent gameboard to player 1.")
    last_turn = 0
    while True:
        sleep(1)
        if mply.turn != last_turn:
            print(ss.set_cursor_str(0, 20) + f"Player {mply.turn} is up.")
            last_turn = mply.turn
            net.send_monopoly(clients[mply.turn].socket, mply.get_gameboard() + ss.set_cursor_str(0, 38) + "It's your turn. Type roll to roll the dice.")
            clients[mply.turn].can_roll = True
            print(f"Sent gameboard to player {mply.turn}.")


def monopoly_game(client: Client = None, cmd: str = None) -> None:
    """
    Description:
        This is the main game loop for Monopoly.
        It will be called from the main function in its own thread. 
    Notes:
        Monopoly command looks like this: "mply,<action>,<specific data>,<even more specific data>,<etc>" 

        player_roll all happens on the player side, so the player can handle all of that. 
        All data during player_roll will be sent to banker like the following:
        recv_message() -> handle_data() -> monopoly_game()
        Where monopoly_game parses the data and banker does not need to send anything back. 

        Now for player_choice, banker and player will do a bit more back and forth.
        Most of the game logic can be handled on the player side, but banker will
        have to preface the messages with cash, properties, etc. 

        TODO fill out this docstring with more information.
    """
    dice = (0, -1)
    if mply.players[mply.turn].name == client.name: # Check if the client who sent data is the current player
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

    os.system("cls")
    print("Welcome to Terminal Monopoly, Banker!")

    test = ss.get_valid_int("Enter a test number: ")
    unittest(test)
    # set_gamerules()
    start_server()
    game = mply.start_game(starting_cash, num_players)
    print(game)
    threading.Thread(target=monopoly_controller, daemon=True).start()
    start_receiver()
    # print(f"Found {players}, each at: ")
    # for player in player_data:
        # print(s.Fore.BLUE+ str(player_data[player][socket.socket]))
    # print(s.Style.RESET_ALL)
