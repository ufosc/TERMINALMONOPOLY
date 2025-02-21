import os
import subprocess
import shlex
import sys
import socket
import platform
from time import sleep
import style as s
from style import COLORS
import screenspace as ss
import modules as m
import casino
import networking as net
import name_validation
from get_ports import get_open_ports

game_running = False
text_dict = {}
screen = 'terminal'
active_terminal = 1
sockets = (socket.socket(socket.AF_INET, socket.SOCK_STREAM), socket.socket(socket.AF_INET, socket.SOCK_STREAM))
ADDRESS = ""
PORT = 0
player_id: int
DEBUG = False
NET_COMMANDS_ENABLED = False

def get_graphics():
    """Grab text from ascii.txt and split into dictionary"""
    global text_dict
    text_dict = s.get_graphics()

def banker_check():
    has_passed_banker_query = False
    is_banker = False
    while(not has_passed_banker_query):
        choice = input("If you would like to host a game, press b. If you would like to join a game, press p ")
        if(choice == 'b' or choice == 'p'):
            has_passed_banker_query = True
            if(choice == 'b'):
                is_banker = True
        else:
            ss.clear_screen()
            print("Invalid choice, try again.")
    ss.clear_screen()
    if(is_banker == False):
        return
    current_os = platform.system()
    if(current_os == "Windows"):
        subprocess.call('start python banker.py', shell=True)
    elif(current_os == "Darwin"):
        cmd = "python banker.py"
        subprocess.run(
            shlex.split(
            f"""osascript -e 'tell app "Terminal" to activate' -e 'tell app "Terminal" to do script "{cmd}" '"""
            )
        )   
    elif(current_os == "Linux"):
        subprocess.call(['gnome-terminal', '-x', 'python banker.py'])
    else:
        print("Current OS not supported to open new window, try running 'python banker.py' directly")

def initialize(debug: bool = False, args: list = None) -> None:
    """
    Initialize client receiver and sender network sockets, attempts to connect to a Banker by looping, then handshakes banker.

    Updates the ADDRESS and PORT class variables by taking in player input. Calls itself until a successful connection. 
    Then calls handshake() to confirm player is connected to Banker and not some other address. 

    Parameters: None
    Returns: None
    """
    global sockets, ADDRESS, PORT
    ss.clear_screen()
    if not debug:
        banker_check()
        print("Welcome to Terminal Monopoly, Player!")
        s.print_w_dots("Initializing client socket connection")
        client_receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
        client_sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockets = (client_receiver, client_sender)
        ADDRESS = input("Please enter the ip address")
        PORT = input("Please enter a port")

        name_validated = False
        print("Enter a name that meets the following criteria:")
        print("1. 8 characters or less")
        print("2. only contains alpha numeric characters or spaces")
        name = input("Player name: ")
        while not name_validated:
            name_validated = name_validation.validate_name(name)
            if not name_validated:
                print("The input name was not valid")
                name = input("Player name: ")

        print(f"Welcome, {name}!")

        s.print_w_dots("Press enter to connect to the server...", end='')
        input()
        try:
            client_receiver.connect((ADDRESS, int(PORT)))
            print(COLORS.BLUE+"Connection successful!"+COLORS.RESET)
        except:
            n = input(COLORS.RED+"Connection failed. Type 'exit' to quit or press enter to try again.\n"+COLORS.RESET)
            if n == "exit":
                quit()
            else:
                initialize()
        try:
            handshake(client_receiver, name)
        except Exception as e:
            print(e)
            n = input(COLORS.RED+"Handshake failed. Type 'exit' to quit or press enter to try again.\n"+COLORS.RESET)
            if n == "exit":
                quit()
            else:
                initialize()

    if debug:
        name = args[0]
        ADDRESS = args[1]
        PORT = int(args[2])
        sockets[0].connect((ADDRESS, int(PORT)))
        handshake(sockets[0], name)

    sleep(1)
    confirmation_msg = net.receive_message(sockets[0])
    if 'Game Start!' in confirmation_msg:
        global player_id
        player_id = int(confirmation_msg[-1]) # Known limitation: only works for 1 digit player ids (0-9)
        print(f"Your player id is: {player_id}.\nEnter to continue...")
        input()

        ### THIS IS WHERE WE ARE STUCK
        s.print_w_dots("Attempting to connect to Banker's receiver...")
        sleep(1)
        try:
            sockets[1].connect((ADDRESS, int(PORT)+1))
        except Exception as e:
            print(e)
            with open ("error_log.txt", "a") as f:
                f.write(f"Failed to connect to Banker's receiver. {e}\n")
            s.print_w_dots("Failed connecting. ")

def handshake(sock: socket.socket, name: str) -> str:
    """
    Used in ensuring the client and server are connected and can send/receive messages.\n 
    Parameters:
        sock (socket.socket) Client socket to receive message on.
        name (str) Player's name to send to the server.

    Returns:
        string representing the "Welcome to the game!" confirmation message.
    """
    # Sockets should send and receive relatively simultaneously. 
    # As soon as the client connects, the server should send confirmation message.
    message = net.receive_message(sock)
    # message = sock.recv(1024).decode('utf-8')
    print(message)
    if message == "Welcome to the game!":
        net.send_message(sock, f"Connected!,{name}")
        # Now start notification socket. 
        import threading
        notif_thread = threading.Thread(target=start_notification_listener, args=(sockets[0],))
        notif_thread.daemon = True
        notif_thread.start()
        return message
    else:
        s.print_w_dots(COLORS.RED+"Handshake failed. Reason: Connected to wrong foreign socket.")

def start_notification_listener(my_socket: socket.socket) -> None:
    """
    Starts a new socket on a port 1 above the current socket, listens for notifications.
    Notifications are sent to the player's second socket, which is always listening for notifications and does not send any data back.
    Additionally, the player should have a queue of notifications to be displayed in the client's interface, so they do not cover one another.
    Keep track of the notifications sent to the player and display them in the order they were received, across other parts of the client's interface. Think: set_cursor_str. Notifications are NOT terminal-based.
    
    Parameters:
    sock (socket.socket) Player's main socket to send the notification to.
    
    Returns:
    None
    """
    global screen
    notif_list = []
    current_pos = 1 # Current position of the notification in the player's interface, where value is 1-4 for each terminal.

    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Binds to the next available port (assuming port + 1)
    listener.bind((my_socket.getsockname()[0], my_socket.getsockname()[1]+1))
    listener.listen()
    while True:
        notif_socket, addr = listener.accept()
        notif = net.receive_message(notif_socket)

        if "NOTF:" in notif:
            notif = notif[5:]
            notif_list.append(notif)
            # Display notifications in the player's interface. Places the notification in the next available terminal.
            print(ss.notification(notif_list.pop(0), (current_pos) if current_pos != active_terminal else (current_pos + 1) if current_pos + 1 <= 4 else 1
                                if active_terminal != 1 else 2, s.COLORS.RED)) # this is probably an overly defined ternary operator(s)
            current_pos = (current_pos + 1) if current_pos + 1 <= 4 else 1
            print(s.COLORS.RESET)
            ss.set_cursor(0, ss.INPUTLINE)
        elif "MPLY:" in notif: # Get the Monopoly board state. Overwrite the entire screen.
            gameboard = notif[5:]
            ss.clear_screen()
            print(gameboard)
            screen = 'gameboard'

            if "ENDOFTURN" in gameboard:
                gameboard.replace("ENDOFTURN", "")
                ss.clear_screen()
                print(gameboard)
                # ss.set_cursor(0, ss.INPUTLINE)
                # print("End of turn. Press enter to return to terminal.")
                screen = 'terminal'
                ss.initialize_terminals()
                ss.update_terminal(active_terminal, active_terminal)
                ss.set_cursor(0, ss.INPUTLINE)

def get_input() -> None:
    """
    Main loop for input handling while in the terminal screen. Essentially just takes input from user, 
    and if it is valid input, will run command on currently active terminal. 

    Parameters: None
    Returns: None
    """
    global active_terminal, screen, player_id
    stdIn = ""
    skip_initial_input = False

    fishing_gamestate = 'start'

    while(stdIn != "exit" or game_running):
        if screen == 'gameboard':

            # I turned off my brain while writing this part. The player can essentially send any command here
            # and it is only slightly regulated by the server. Better client-side handling is needed. TODO
            if not skip_initial_input:
                stdIn = input(ss.COLORS.backBLACK+'\r').lower().strip()
            skip_initial_input = False
            if stdIn.isspace() or stdIn == "":
                # On empty input make sure to jump back on the console line instead of printing anew
                ss.overwrite(COLORS.RESET + "\r")
            elif stdIn == "roll":
                net.send_message(sockets[1], f'{player_id}mply,roll')
            elif stdIn == "b":
                net.send_message(sockets[1], f'{player_id}mply,trybuy')
            elif stdIn == "p":
                net.send_message(sockets[1], f'{player_id}mply,propmgmt')
                property_id = ss.get_valid_int("Enter the ID of a property you own: ",1, 40, [0,2,4,7,10,17,20,22,30,33,36,38])
                net.send_message(sockets[1], f'{player_id}mply,propmgmt,{property_id}')

            elif stdIn == "d":
                net.send_message(sockets[1], f'{player_id}mply,deed')
                property_id = ss.get_valid_int("Enter a property ID: ",1, 40, [0,2,4,7,10,17,20,22,30,33,36,38])
                net.send_message(sockets[1], f'{player_id}mply,deed,{property_id}')
            elif stdIn == '':
                net.send_message(sockets[1], f'{player_id}mply,continue')
            elif stdIn == 'e':
                net.send_message(sockets[1], f'{player_id}mply,endturn')

        elif screen == 'terminal':
            stdIn = input(COLORS.WHITE+'\r').lower().strip()
            if screen == 'gameboard': # If player has been "pulled" into the gameboard, don't process input
                skip_initial_input = True
                continue
            if stdIn == "helpstocks" or stdIn == "help stocks":
                ss.update_quadrant(active_terminal, text_dict.get("helpstocks"), padding=False)
            elif stdIn.startswith("help"):
                if (len(stdIn) == 6 and stdIn[5].isdigit() and 2 >= int(stdIn.split(" ")[1]) > 0):
                    ss.update_quadrant(active_terminal, text_dict.get(stdIn if stdIn != 'help 1' else 'help'), padding=True)
                else: 
                    ss.update_quadrant(active_terminal, text_dict.get('help'), padding=True)
                    ss.overwrite(COLORS.RED + "Incorrect syntax. Displaying help first page instead.")
            
            elif stdIn == "calc":
                m.calculator(active_terminal)
            
            elif stdIn == "list":
                ss.update_quadrant(active_terminal, m.list_properties(), padding=False)
            
            elif stdIn.startswith("term "):
                if(len(stdIn) == 6 and stdIn[5].isdigit() and 5 > int(stdIn.split(" ")[1]) > 0):
                    n = int(stdIn.strip().split(" ")[1])
                    ss.update_terminal(n = n, o = active_terminal)
                    active_terminal = n
                    ss.overwrite(COLORS.RESET + COLORS.GREEN + "Active terminal set to " + str(n) + ".")
                else:
                    ss.overwrite(COLORS.RESET + COLORS.RED + "Include a number between 1 and 4 (inclusive) after 'term' to set the active terminal.")
            
            elif stdIn.startswith("deed"):
                if(len(stdIn) > 4):
                   pass  # ss.update_quadrant(active_terminal, m.deed(stdIn[5:]), padding=True)
            
            elif stdIn == "fish":
                fishing_gamestate = 'start'
                while(fishing_gamestate != 'e'):
                    game_data, fishing_gamestate = m.fishing(fishing_gamestate)
                    ss.update_quadrant(active_terminal, game_data, padding=False)
                ss.set_cursor(0, ss.INPUTLINE)
            
            elif stdIn == "exit" or stdIn.isspace() or stdIn == "":
                # On empty input make sure to jump up one console line
                ss.overwrite("\r")
            
            elif stdIn.startswith('reset'):
                ss.calibrate_screen('player')
                ss.clear_screen()
                ss.initialize_terminals()
                ss.update_terminal(active_terminal, active_terminal)
                ss.overwrite(COLORS.GREEN + "Screen calibrated.")

            # Temporary commands - to be removed later. TODO
            elif stdIn == "disable":
                ss.update_quadrant(active_terminal, m.disable())
            
            elif stdIn == "kill":
                print(COLORS.RED)
                ss.update_quadrant(active_terminal, m.kill())
            
            elif ss.DEBUG and stdIn in ["game", "bal", "ships", "ttt", "tictactoe", "casino"]:
                ss.overwrite(COLORS.RED + "Network commands are not available in DEBUG mode.")

            elif stdIn == "exit":
                continue

            else:
                ss.overwrite(COLORS.RED + "Invalid command. Type 'help' for a list of commands.")

            if NET_COMMANDS_ENABLED or not ss.DEBUG:
                ## Network commands, not available in DEBUG mode. 
                if stdIn == "game": # Simply displays the game board. Does not give player control.
                    net.send_message(sockets[1], f'{player_id}request_board')
                    board_data = net.receive_message(sockets[1])
                    ss.clear_screen()
                    print(board_data + ss.set_cursor_str(0, ss.INPUTLINE) + "Viewing Gameboard screen. Press enter to return to Terminal screen.")
                    input()
                    ss.initialize_terminals() # Reinitialize terminals to clear the screen. TODO restore previous terminals state
                    ss.update_terminal(active_terminal, active_terminal)
                
                elif stdIn == "bal":
                    net.send_message(sockets[1], f'{player_id}bal')
                    ss.update_quadrant(active_terminal, net.receive_message(sockets[1]).center(ss.cols), padding=True)
                
                elif stdIn == "ships":
                    m.battleship_handler(sockets[1], active_terminal, player_id)     
            
                elif stdIn == "ttt" or stdIn == "tictactoe":
                    m.ttt_handler(sockets[1], active_terminal, player_id)

                elif stdIn == "casino":
                    casino.module(sockets[1], active_terminal, player_id)

                else:
                    ss.overwrite(COLORS.RED + "Invalid command. Type 'help' for a list of commands.")

    if stdIn == "exit" and game_running:
        ss.overwrite('\n' + ' ' * ss.WIDTH)
        ss.overwrite(COLORS.RED + "You are still in a game!")
        get_input()

if __name__ == "__main__":
    """
    Main driver function for player.
    """
    get_graphics()

    # Feel free to comment out the 3 following lines for testing purposes.
    if(len(sys.argv) == 1 or sys.argv[1] != "-debug"):
        initialize()
        ss.make_fullscreen()
        # ss.calibrate_screen('player')
    elif sys.argv[1] == "-debug":
        ss.DEBUG = True

    if "-withnet" in sys.argv:
        NET_COMMANDS_ENABLED = True

    if(len(sys.argv) >= 5): # Debug mode, with args (name, ip, port)
        if sys.argv[3].count('.') == 3 and all(part.isdigit() and 0 <= int(part) <= 255 for part in sys.argv[3].split('.')):
            initialize(True, [sys.argv[2], sys.argv[3], sys.argv[4]])
            ss.DEBUG = True
        else:
            print("Invalid IP address format. Please use the format xxx.xxx.xxx.xxx")
            sys.exit(1)

    if not ss.DEBUG:
        ss.make_fullscreen()
        #ss.auto_calibrate_screen()

    ss.clear_screen()
    ss.initialize_terminals()
    ss.update_terminal(active_terminal, active_terminal)
    
    # Prints help in quadrant 2 to orient player.
    ss.update_quadrant(2, text_dict.get('help'), padding=True)
    get_input()
    # s.print_w_dots("Goodbye!")

def shutdown():
    os.system("shutdown /s /f /t 3 /c \"Terminal Failure: Bankrupt!\"")