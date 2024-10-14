import socket
import threading
import os
import style as s
import screenspace as ss 
import battleship
import networking

import select
from time import sleep

bank_cash = 100000
starting_cash = 1500
players = []
port = 3131
board = ""
active_games = []
global timer
timer = 0

class Game:
    def __init__(self, name: str, players: list, board: str, other_data):
        self.name = name
        self.players = players
        self.board = board
        self.other_data = other_data


class Client:
    def __init__(self, socket: socket.socket, name: str, money: int, properties: list):
        self.socket = socket
        self.name = name
        self.money = money
        self.properties = properties
        self.active_games = []

def initialize_terminal():
    """
    Clears terminal and prints a welcome message to Banker.
    
    Parameters: None
    Returns: None
    """
    os.system("cls")
    print("Welcome to Terminal Monopoly, Banker!")

def start_server() -> socket.socket:
    """
    Begins receiving server socket on local machine IP address and inputted port #. 

    Asks user for port # and begins server on the local machine at its IP address. 
    It then waits for a predetermined number of players to connect. Upon a full game, 
    it returns the transmitter socket. 

    Parameters: None
    Returns: Transmitter socket aka the Banker's sender socket.  
    """
    global players, port
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get local machine name
    host = socket.gethostname()
    ip_address = socket.gethostbyname(host)

    # Choose a port that is free
    # port = int(input("Choose a port, such as 3131: "))
    port = 3131

    # Bind to the port
    # server_socket.bind(('localhost', port))
    server_socket.bind((host, port))
    s.print_w_dots("Server started on %s port %s" % (ip_address, port))
    server_socket.listen()

    s.print_w_dots("Waiting for clients...")
    
    # TEMP VARIABLE: Players should be hardcoded to 4 for printing/playing purposes
    # Alternatively, make game work for N players...?
    num_players = 1
    handshakes = [False] * num_players

    # start_receiver(handshakes)
    game_full = False
    while not game_full:
        # Accepts connections while there are less than <num_players> players
        sleep(1)
        if len(players) != num_players:
            client_socket, addr = server_socket.accept()
            print("Got a connection from %s" % str(addr))
            client_handler = threading.Thread(target=handshake, args=(client_socket,handshakes))
            client_handler.start()
        else: 
            game_full = True
            # # Give program a moment to evaluate handshakes
            # for h in handshakes:
            #     sleep(1)
            #     if h == False:
            #         players -= 1
            # break
    s.print_w_dots("Game is full. Starting game...")
    s.print_w_dots("")
    s.print_w_dots("")
    s.print_w_dots("")
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
        clients = {}
        while True:
            # check for a connection to the server or data ready from clients.
            # readers will be empty on timeout.
            readers,_,_ = select.select(to_read,[],[],0.1)
            for reader in readers:
                if reader is server:
                    player,address = reader.accept()
                    # Client(player, 'Player', starting_cash, [])
                    s.print_w_dots('Player connected from: ' + address[0])
                    clients[player] = address # store address of client in dict
                    to_read.append(player) # add client to list of readable sockets
                else:
                    data = reader.recv(1024)
                    handle_data(data, reader)
                    ### Else ifs chain here for all player input options
                    
                    if not data: # No data indicates disconnect
                        s.print_w_dots(f'Player at {address[0]} disconnected.')
                        to_read.remove(reader) # remove from monitoring
                        del clients[reader] # remove from dict as well
                        if(len(clients) == 0):
                            s.print_w_dots('[RECEIVER] All connections dropped. Receiver stopped.')
                            return
            print(f'Time passed since last command: {timer}. ',flush=True,end='\r')
            timer += 1

def handle_data(data: bytes, client: socket.socket = None) -> str:
    """
    Handles all data received from player sockets. 
    
    Parameters:
    data (str) Data received from player sockets. 
    
    Returns:
    str representing the response to the player's data. 
    """
    global timer

    # Example usage
    if data.decode() == 'request_board':
        timer = 0
        # Player requests board:
        # Send board size, then board in segments
        board_data = board.encode()
        s.print_w_dots(f'Gameboard sent to player {client[0]}')

    elif data.decode() == 'ships':
        if len(active_games) == 0:
            s.print_w_dots('No active games to join.')
            number_of_players = 1
            s.print_w_dots(f'Creating new game with {number_of_players} players.')
            battleship_game = battleship.start_game()
            active_games.append(Game('Battleship', [None] * number_of_players, battleship_game.board, battleship_game))
            s.print_w_dots('Game created.')
            # @TODO adjust for additional games. battleship is not necessarily in 0th spot
            # likewise, player 0 is not always the client communication.. use find or in fxn
            active_games[0].players[0] = client
            active_games[0].other_data.player_names.append(players[0].name)
            s.print_w_dots(f'Player {client} joined game.')
            battleship_board = battleship_game.board + battleship_game.popup("Test")
            print(battleship_board)
            print("Current size of Battleship board (if over 10^10, broken): ", len(battleship_board))
            networking.send_message(client, battleship_board)
            s.print_w_dots(f'Gameboard sent to player {client}')
        else:
            battleship_board = active_games[0].other_data.board + active_games[0].other_data.popup("Test")
            
            print("Current size of Battleship board (if over 10^10, broken): ", len(battleship_board))
            networking.send_message(client, battleship_board)
            
            s.print_w_dots(f'Gameboard sent to player {client}')
        
        if active_games[0].other_data.gamestate == 'placing ships':
            # assuming player 0 in battleship
                if len(active_games[0].other_data.ships[0]) != 5: 
                    networking.send_message(client, f'{players[0].name}\'s turn to place ships!')



def handshake(client_socket: socket.socket, handshakes: list):
    """
    As players connect, they attempt to handshake the server, this function handles that and 
    only starts the game once 4 handshakes have been successfully resolved. 
    
    Parameters:
    client_socket (socket.socket) Server sender socket which players connect to at game
        initialization. 
    handshakes (list) Boolean list of successful handshakes. By default, all values are false.  
    """
    global players
    # Attempt handshake
    client_socket.send("Welcome to the game!".encode('utf-8'))
    message = client_socket.recv(1024).decode('utf-8')
    if message == "Connected!":
        handshakes[len(players)] = True
        players.append(Client(client_socket, 'Player 1', 2000, []))
        players[len(players)-1].name = input(f"\033[36;0HWhat is this player's name? ")     
    else: 
        handshakes[len(players)] = False

def set_gamerules() -> None:
    """
    Configure all gamerule variables according to Banker user input. Repeats until successful. 
    
    Parameters: None
    Returns: None
    """
    global bank_cash, starting_cash
    try:
        bank_cash = int(input("Enter the amount of money the bank starts with: "))
        starting_cash = int(input("Enter the amount of money each player starts with: "))
    except:
        print("Failed to set gamerules. Try again.")
        input()
        set_gamerules()

if __name__ == "__main__":
    initialize_terminal()
    server_socket = start_server()
    start_receiver()
    # print(f"Found {players}, each at: ")
    # for player in player_data:
        # print(s.Fore.BLUE+ str(player_data[player][socket.socket]))
    # print(s.Style.RESET_ALL)
    # set_gamerules()
