import socket
import threading
import os
import style as s
from screenspace import Banker as ss

import socket
import select
from time import sleep

bank_cash = 100000
starting_cash = 1500
players = 0
port = 3131
board = ""

player_data = {1: {
                    socket.socket: "",
                    "name": "",
                    "money": starting_cash,
                    "properties": []

                }, 2: {
                    socket.socket: "",
                    "name": "",
                    "money": starting_cash,
                    "properties": []    

                }, 3: {
                    socket.socket: "",
                    "name": "",
                    "money": starting_cash,
                    "properties": []

                }, 4: {
                    socket.socket: "",
                    "name": "",
                    "money": starting_cash,
                    "properties": []

                }}
"""
Players are stored in a dictionary with integer keys 1, 2, 3, and 4. 
Each value is another dictionary, with the following values  
\n(socket.socket) socket to communicate with. Default = ""
\n(name) Name of player. Default = ""
\n(money) Current amount of money. Default = starting_cash
\n(properties) List of properties owned. Default = []
"""

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
    global players
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get local machine name
    host = socket.gethostname()
    ip_address = socket.gethostbyname(host)

    # Choose a port that is free
    port = int(input("Choose a port, such as 3131: "))

    # Ask for the names of the players
    for player in players:
        player.name = input(f"\033[36;0HWhat is {player.name}'s name? ")     

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
        if players != num_players:
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
    global player_data
    s.print_w_dots('[RECEIVER] Receiver started!') 
    # Credit to https://stackoverflow.com/a/43151772/19535084 for seamless server-client handling. 
    with socket.socket() as server:
        host = socket.gethostname()
        ip_address = socket.gethostbyname(host)
        server.bind((ip_address,int(port+1)))
        server.listen()
        s.print_w_dots('[RECEIVER] Receiver accepting connections at {}'.format(port+1))
        to_read = [server]  # add server to list of readable sockets.
        players = {}
        timer = 0
        while True:
            # check for a connection to the server or data ready from clients.
            # readers will be empty on timeout.
            readers,_,_ = select.select(to_read,[],[],0.1)
            for reader in readers:
                if reader is server:
                    player,address = reader.accept()
                    s.print_w_dots('Player connected from: ' + address[0])
                    players[player] = address # store address of client in dict
                    to_read.append(player) # add client to list of readable sockets
                else:
                    data = reader.recv(1024)
                    if data.decode() == 'request_board':
                        timer = 0
                        # Player requests board:
                        # Send board size, then board
                        size = len(board.encode())
                        reader.send(size.to_bytes(4,byteorder='big'))
                        reader.send(board.encode())
                        s.print_w_dots(f'Gameboard sent to player {address[0]}')
                    
                    ### Else ifs chain here for all player input options
                    
                    if not data: # No data indicates disconnect
                        s.print_w_dots(f'Player at {address[0]} disconnected.')
                        to_read.remove(reader) # remove from monitoring
                        del players[reader] # remove from dict as well
                        if(len(players) == 0):
                            s.print_w_dots('[RECEIVER] All connections dropped. Receiver stopped.')
                            return
            print(f'Time passed since last command: {timer}. ',flush=True,end='\r')
            timer += 1

def location_stats(x: int = 0, y:int = 0):
    """
    Function to return data about a specific location at (x,y). 
    """
    # basically need to check adjacent coordinates if and only if they are within a location's 
    # 3x3 "square." Reject all boundary lines and all internal coordinates. 
    # Write a smart function using math to see if the specified coordinate is an edge of a 3x3, 
    # maybe use distance formula 


def update_board(x:int = 0, y:int = 0, player:int = -1, house:bool = False, hotel:bool = False):
    """
    Function to update board at coordinates x,y with several possible parameter combinations.
    
    Parameters: 
    x (int) Exact x position on gameboard to update. [0-79]. Default = 0
    y (int) Exact y position on gameboard to update. [0-34]. Default = 0
    player (int) Player to update gameboard by color. [1-4]. Default = -1
    """
    global board
    if(len(board) == 0):
        board = s.get_graphics().get('gameboard')
    # Proof of concept function- simply set the position to player value
    board[y*80+x] = player
    
    

def handshake(client_socket: socket.socket, handshakes: list):
    """
    As players connect, they attempt to handshake the server, this function handles that and 
    only starts the game once 4 handshakes have been successfully resolved. 
    
    Parameters:
    client_socket (socket.socket) Server sender socket which players connect to at game
        initialization. 
    handshakes (list) Boolean list of successful handshakes. By default, all values are false.  
    """
    global players, player_data
    # Attempt handshake
    client_socket.send("Welcome to the game!".encode('utf-8'))
    message = client_socket.recv(1024).decode('utf-8')
    if message == "Connected!":
        handshakes[players] = True
        players += 1
        player_data[players][socket.socket] = client_socket
    else: 
        handshakes[players] = False

def update_clients(client_socket: socket.socket):
    pass

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
