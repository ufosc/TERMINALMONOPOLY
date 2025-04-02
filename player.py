import os
import subprocess
import shlex
import sys
import socket
import platform
import threading
from time import sleep
from style import MYCOLORS as COLORS, graphics as g, print_w_dots
import screenspace as ss
import networking as net
import validation
import modules_directory.inventory as inv
import keyboard

game_running = False
screen = "terminal"
sockets = (socket.socket(socket.AF_INET, socket.SOCK_STREAM), socket.socket(socket.AF_INET, socket.SOCK_STREAM))
ADDRESS = ""
PORT = 0
player_id: int
name: str = ''
DEBUG = False
NET_COMMANDS_ENABLED = False
TERMINALS = [ss.Terminal(1, (2, 2)), ss.Terminal(2, (ss.cols+3, 2)), ss.Terminal(3, (2, ss.rows+3)), ss.Terminal(4, (ss.cols+3, ss.rows+3))]
active_terminal = TERMINALS[0]
inventory = inv.Inventory() # global inventory object for all modules to access

def banker_check(local: bool = False) -> None:
    """
    Asks player if they want to run banker (host a game). If not, prompts user to start it.
    Parameters: local (bool) - if True, create a server on localhost, with all further inputs satisfied. Default is False. 
    Returns: None
    """
    has_passed_banker_query = False
    is_banker = False
    if not local:
        while( not has_passed_banker_query):
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
        subprocess.call("start python banker.py -local" if local else "start python banker.py", shell=True)
    elif(current_os == "Darwin"):
        cmd = "python banker.py -local" if local else "python banker.py"
        subprocess.run(
            shlex.split(
            f"""osascript -e 'tell app "Terminal" to activate' -e 'tell app "Terminal" to do script "{cmd}" '"""
            )
        )   
    elif(current_os == "Linux"):
        # We use a list of existing Linux terminals to run banker.
        list_of_terms = [("gnome-terminal", "-e"), ("kgx", "-x"), ("ptyxis", "--"),
                        ("konsole", "-e"), ("xfce4-terminal", "-e"), ("mate-terminal", "-e"),
                        ("tilix", "-e"), ("xterm", "-e")]
        
        launched = False
        for term in list_of_terms:
            try:
                subprocess.Popen([term[0], term[1], "bash -c '" + sys.executable + (" banker.py -local'" if local else " banker.py'")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=os.path.dirname(os.path.realpath(__file__)))
                launched = True
                break
            except FileNotFoundError:
                pass

        if(not launched):
            print("Your terminal was not detected!\nYou can either type in your terminal's start command (ex: 'gnome-terminal -x') or press enter and directly run 'python banker.py'.")
            term = input("Terminal Command (default: none): ")
            if(term != "" and ' ' in term):
                try:
                    term = term.split(" ")
                    subprocess.Popen([term[0], term[1], "bash -c '" + sys.executable + (" banker.py -local'" if local else " banker.py'")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=os.path.dirname(os.path.realpath(__file__)))
                except:
                    print("Invalid command! Try running 'python banker.py' directly")
            else:
                print("Make sure you start 'python banker.py' directly")
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
    global sockets, ADDRESS, PORT, name
    ss.clear_screen()
    if not debug:
        banker_check()
        print("Welcome to Terminal Monopoly, Player!")
        print_w_dots("Initializing client socket connection")     
        client_receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
        client_sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockets = (client_receiver, client_sender)
        
        name_validated = False
        print("Enter a name that meets the following criteria:")
        print("1. 8 characters or less")
        print("2. only contains alpha numeric characters or spaces")
        name = input("Player name: ")
        while not name_validated:
            name_validated = validation.validate_name(name)
            if not name_validated:
                print("The input name was not valid")
                name = input("Player name: ")
        
        if "localhost" not in sys.argv:
            ADDRESS = input("Enter Host IP: ").strip()
            while not validation.validate_address(ADDRESS):
                print("Invalid IP address. Please enter a valid IP address.")
                ADDRESS = input("Enter Host IP: ").strip()

            PORT = input("Enter Host Port: ")
            # Validate IP address and port
            while not validation.validate_port(PORT):
                print("Invalid port. Please enter a valid port.")
                PORT = input("Enter Host Port: ")


        print(f"Welcome, {name}!")

        print_w_dots("Press enter to connect to the server...", end='')
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

    confirmation_msg = net.receive_message(sockets[0])
    if 'Game Start!' in confirmation_msg:
        global player_id
        player_id = int(confirmation_msg[-1]) # Known limitation: only works for 1 digit player ids (0-9)
        print(f"Your player id is: {player_id}.\nEnter to continue...")
        input()

        ### THIS IS WHERE WE ARE STUCK
        print_w_dots("Attempting to connect to Banker's receiver...")
        sleep(1)
        try:
            sockets[1].connect((ADDRESS, int(PORT)+1))
        except Exception as e:
            print(e)
            with open ("error_log.txt", "a") as f:
                f.write(f"Failed to connect to Banker's receiver. {e}\n")
            print_w_dots("Failed connecting. ")

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
        notif_thread = threading.Thread(target=start_notification_listener, args=(sockets[0],))
        notif_thread.daemon = True
        notif_thread.start()
        return message
    else:
        print_w_dots(COLORS.RED+"Handshake failed. Reason: Connected to wrong foreign socket.")

def print_queue():
    """
    Responsible for updating all Terminal screens with persistent modules, i.e. modules that may be updated while not as the active terminal.
    Ran in its independent thread.
    """
    while True: # TODO: updating certain terminals with networking commands CAN crash the game because the player
                # receives a message for some module that is not the terminal being updated in this loop, or vice versa.
                # 
                # Steps to recreate:
                # Run a module that has a oof callable that is not the active terminal, and then, in another terminal,
                # run a module that has a different oof callable. Have the other 2 terminals also have oof callables.
                # Then, run a command that updates the active terminal. The game may crash because the data is not in sync.
                #  
                # The data becomes out of sync, or not a 1-to-1 mapping. A better solution is to have a queue of messages 
                # to parse through as they're received, and then update the terminal with the correct data based on a 
                # tag or identifier. 
        if screen == 'terminal': # Only update if we are in the terminal screen.
            for t in TERMINALS:
                if t.status == "DISABLED" or t.status == "BUSY": # Skip disabled or (just in case) busy terminals.
                    continue
                sleep(0.5) # Delay to prevent overwhelming the system with print calls. Change to lower value when done debugging.
                # Also important to delay to ensure calls to banker are not overwhelming.
                if not t.oof_callable == None and t.index != active_terminal.index: # Only update if the terminal is not active and has an out-of-focus callable.
                    if not net.player_mtrw: # Ensure the main thread is not waiting on receiving new data
                        data = t.oof_callable() # Call the out-of-focus function to get the new data.
                        t.check_new_data(data) # Check if new data is available.
                        if t.has_new_data and t.oof_callable is not None: # Only update terminal if there is new data, to avoid unnecessary prints.
                            for i in range(150):
                                keyboard.block_key(i) # Naively block all calls to the keyboard when updating Terminals OOF
                            for i in range(150):
                                keyboard.unblock_key(i)
                            t.update(data, padding=False) # Update the terminal with new data.
                            t.has_new_data = False # Reset the flag.
                else: 
                    continue # No need to update if no callable or terminal is active.

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
    global screen, player_id
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
            print(ss.notification(notif_list.pop(0), (current_pos) if current_pos != active_terminal.index else (current_pos + 1) if current_pos + 1 <= 4 else 1
                                if active_terminal.index != 1 else 2, COLORS.RED)) # this is probably an overly defined ternary operator(s)
            current_pos = (current_pos + 1) if current_pos + 1 <= 4 else 1
            print(COLORS.RESET)
            ss.set_cursor(0, ss.INPUTLINE)
        elif "TERM:" in notif:
            term = notif[5:]
            term = term.split(" ")
            if(term[0] == "kill"):
                TERMINALS[int(term[1])].kill()
            elif(term[0] == "disable"):
                TERMINALS[int(term[1])].disable()
            elif(term[0] == "enable"):
                TERMINALS[int(term[1])].enable(True, sockets[1], player_id)
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
                # ss.initialize_terminals()
                ss.update_terminal(active_terminal.index, active_terminal.index)
                ss.set_cursor(0, ss.INPUTLINE)

import importlib
def get_module_commands() -> dict: 
    """
    Retrieves a list of available module commands and their corresponding functions.
    This function scans the "modules_directory" for Python files, dynamically
    imports each module, and checks if the module has a 'command' and 'run' attribute.
    If the attributes exist, the command and its corresponding function are added
    to the dictionary.
    
    Returns:
        dict: A dictionary mapping module commands to their corresponding functions.
    """
    pairs = {}
    for file in os.listdir("modules_directory"):
        if file.endswith(".py"):
            file = file[:-3]
            module = importlib.import_module("modules_directory." + file)
            if hasattr(module, 'command') and hasattr(module, 'run'): # Check if the module has 'command' and 'run' attributes
                pairs[module.command] = module.run # Add the command and its corresponding function to the dictionary
    return pairs

def get_input() -> None:
    """
    Main loop for input handling while in the terminal screen. Essentially just takes input from user, 
    and if it is valid input, will run command on currently active terminal. 

    Parameters: None
    Returns: None
    """
    global active_terminal, screen, player_id
    cmds = get_module_commands()
    threading.Thread(target=print_queue, daemon=True).start()

    stdIn = ""
    skip_initial_input = False
    last_terminal = -1

    while(stdIn != "exit" or game_running):
        if screen == 'gameboard':

            # I turned off my brain while writing this part. The player can essentially send any command here
            # and it is only slightly regulated by the server. Better client-side handling is needed. TODO
            if not skip_initial_input:
                stdIn = input(COLORS.backBLACK+'\r').lower().strip()
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
            if screen == 'gameboard': # If player has been "pulled" into the gameboard, don't process input
                skip_initial_input = True
                continue
            if active_terminal.persistent and last_terminal != active_terminal.index:
                stdIn = active_terminal.command
            else:
                stdIn = input(COLORS.backBLACK+'\r').lower().strip()

            last_terminal = active_terminal.index
            
            # This 'term' command needs to be first, in case of a persistent module.
            if stdIn.startswith("term "): 
                if(len(stdIn) == 6 and stdIn[5].isdigit() and 5 > int(stdIn.split(" ")[1]) > 0):
                    n = int(stdIn.strip().split(" ")[1])
                    ss.update_terminal(n = n, o = active_terminal.index)
                    active_terminal = TERMINALS[n-1] # Update active terminal, n-1 because list is 0-indexed
                    ss.overwrite(COLORS.RESET + COLORS.GREEN + "Active terminal set to " + str(n) + ".")
                else:
                    ss.overwrite(COLORS.RESET + COLORS.RED + "Include a number between 1 and 4 (inclusive) after 'term' to set the active terminal.")
            elif stdIn == "exit":
                break
            # Anything beyond this one should be not crucial, as it will NOT work if disabled.
            elif active_terminal.status == "DISABLED":
                ss.overwrite(COLORS.RED + "Terminal is disabled! Switch to another terminal with 'term'.")
                continue

            # TODO, see https://github.com/ufosc/TERMINALMONOPOLY/issues/105
            elif stdIn == "helpstocks" or stdIn == "help stocks":
                active_terminal.clear()
                active_terminal.update(g.get("helpstocks"))
            elif stdIn.startswith("help"):
                if (len(stdIn) == 6 and stdIn[5].isdigit() and 2 >= int(stdIn.split(" ")[1]) > 0):
                    active_terminal.update(g.get(stdIn if stdIn != 'help 1' else 'help'), padding=True)
                else: 
                    active_terminal.update(g.get('help'), padding=True)
                    ss.overwrite(COLORS.RED + "Incorrect syntax. Displaying help first page instead.")
                active_terminal.oof_callable = None
            elif stdIn == "clear": # Clear the given Terminal to allow other commands to be ran
                active_terminal.clear()
                active_terminal.update("")
                active_terminal.display()
                active_terminal.oof_callable = None
                active_terminal.persistent = False
                active_terminal.command = ""
            elif stdIn in cmds.keys(): # Check if the command is in the available commands
                usable = True
                for t in TERMINALS:
                    if t.index == active_terminal.index: # Skip the active terminal
                        continue
                    if t.command == stdIn: # If the command is already in use by another terminal, do not allow it to be used again.
                        ss.overwrite(COLORS.RED + "Command already in use by another terminal.")
                        usable = False
                        break
                if usable:
                    active_terminal.command = stdIn # Set the command for the active terminal
                    active_terminal.oof_callable = cmds[stdIn] if hasattr(cmds[stdIn], 'oof') else None # Set the out of focus callable function if it exists
                    cmds[stdIn](player_id=player_id, server=sockets[1], active_terminal=active_terminal) # Call the function with the required parameters

            elif stdIn.isspace() or stdIn == "":
                # On empty input make sure to jump up one console line
                ss.overwrite("\r")
            
            # Reset screen calibration logic
            elif stdIn.startswith('reset'):
                if "auto" in stdIn:
                    ss.auto_calibrate_screen()
                ss.calibrate_screen('player')
                ss.clear_screen()
                print(g.get('terminals'))
                for t in TERMINALS:
                    t.display()
                ss.set_cursor(0, 0)
                ss.update_terminal(active_terminal.index, active_terminal.index)
                ss.overwrite(COLORS.GREEN + "Screen calibrated.")
            
            elif ss.DEBUG and stdIn in ["game", "bal", "ttt", "tictactoe", "casino", "deed", "kill", "disable"]:
                ss.overwrite(COLORS.RED + "Network commands are not available in DEBUG mode." + COLORS.RESET)

            #elif stdIn == "kill":
                #active_terminal.kill()
            
            elif stdIn == "disable":
                active_terminal.disable()
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
                    ss.clear_screen()
                    print(g.get('terminals'))
                    for t in TERMINALS:
                        t.display()
                    ss.update_terminal(active_terminal.index, active_terminal.index)

                elif stdIn.startswith("kill"):
                    if(len(stdIn.split(" ")) == 3):
                        net.send_message(sockets[1], f'{player_id}' + stdIn)
                        ss.overwrite(COLORS.RED + net.receive_message(sockets[1]))
                    else:
                        ss.overwrite(COLORS.RED + "Invalid command. Syntax is 'kill PLAYER TERM' (ex. 'kill 0 3)")
                elif stdIn.startswith("disable"):
                    #TODO - This direct command is mostly for testing.
                    if(len(stdIn.split(" ")) == 4):
                        net.send_message(sockets[1], f'{player_id}' + stdIn)
                        ss.overwrite(COLORS.RED + net.receive_message(sockets[1]))
                    else:
                        ss.overwrite(COLORS.RED + "Invalid command. Syntax is 'disable PLAYER TERM LENGTH' (ex. 'disable 0 3 15)")
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
    if "-withnet" in sys.argv:
        NET_COMMANDS_ENABLED = True
    
    if "-local" in sys.argv:
        initialize(True, ["Player", "localhost", "33333"])
    elif(len(sys.argv) == 1 or sys.argv[1] != "-debug"):
        initialize()
        ss.make_fullscreen()
    elif sys.argv[1] == "-debug":
        ss.DEBUG = True

    if(len(sys.argv) >= 5): # Debug mode, with args (name, ip, port)
        if sys.argv[3].count('.') == 3 and all(part.isdigit() and 0 <= int(part) <= 255 for part in sys.argv[3].split('.')):
            initialize(True, [sys.argv[2], sys.argv[3], sys.argv[4]])
            ss.DEBUG = True
        else:
            print("Invalid IP address format. Please use the format xxx.xxx.xxx.xxx")
            sys.exit(1)    

    if not "-skipcalib" in sys.argv:
        ss.make_fullscreen()
        ss.auto_calibrate_screen()
        ss.calibrate_screen("player")
    else: 
        ss.choose_colorset("COMPAT_COLORS")

    ss.clear_screen()
    ss.initialize_terminals(TERMINALS)
    ss.update_terminal(active_terminal.index, active_terminal.index)

    if "-debug" in sys.argv:
        for i in range(ss.HEIGHT + 10):
            ss.set_cursor(155, i)
            print(i)
    
    # Prints help in quadrant 2 to orient player.
    TERMINALS[1].update(g.get('help'), padding=True)
    get_input()
    # print_w_dots("Goodbye!")

def shutdown():
    os.system("shutdown /s /f /t 3 /c \"Terminal Failure: Bankrupt!\"")