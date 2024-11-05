import os
import sys
import socket
from time import sleep
import style as s
from style import COLORS
import screenspace as ss
import modules as m
import networking as net

game_running = False
text_dict = {}
screen = 'terminal'
active_terminal = 1
sockets = (socket.socket, socket.socket)
ADDRESS = ""
PORT = 0
name = ""
balance = 0
properties = 0
calculator_history_queue = []
calculator_history_current_capacity = 15

def get_graphics():
    """Grab text from ascii.txt and split into dictionary"""
    global text_dict
    text_dict = s.get_graphics()

def initialize():
    """
    Initialize client receiver and sender network sockets, attempts to connect to a Banker by looping, then handshakes banker.

    ### This may be unnecessary: fix as necessary.
    Creates two sockets, a receiver and sender at the same address.

    Updates the ADDRESS and PORT class variables by taking in player input. Calls itself until a successful connection. 
    Then calls handshake() to confirm player is connected to Banker and not some other address. 

    Parameters: None
    Returns: None
    """
    global sockets, ADDRESS, PORT
    os.system("cls")
    print("Welcome to Terminal Monopoly, Player!")
    s.print_w_dots("Initializing client socket connection")     
    client_receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
    client_sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockets = (client_receiver, client_sender)
    ADDRESS = input("Enter Host IP: ")
    PORT = input("Enter Host Port: ")

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
        handshake(client_receiver)
    except Exception as e:
        print(e)
        n = input(COLORS.RED+"Handshake failed. Type 'exit' to quit or press enter to try again.\n"+COLORS.RESET)
        if n == "exit":
            quit()
        else:
            initialize()

    sleep(1)
    confirmation_msg = net.receive_message(sockets[0]) # sometimes gets hung up for player 2 TODO: Fix this
    if 'Game Start!' in confirmation_msg:
        print(f"You are player {confirmation_msg[-1]}.\nEnter to continue...")
        input()

        s.print_w_dots("Attempting to connect to Banker's receiver...")
        sleep(1)
        try:
            sockets[1].connect((ADDRESS, int(PORT)+1))
        except Exception as e:
            print(e)
            with open ("error_log.txt", "a") as f:
                f.write(f"Failed to connect to Banker's receiver. {e}\n")
            s.print_w_dots("Failed connecting. ")

def handshake(sock: socket.socket) -> str:
    """
    Used in ensuring the client and server are connected and can send/receive messages. 
    Parameters:
    sock (socket.socket) Client socket to receive message on.

    Returns:
    string representing the "Welcome to the game!" confirmation message.
    """
    # Sockets should send and receive relatively simultaneously. 
    # As soon as the client connects, the server should send confirmation message.
    message = net.receive_message(sock)
    # message = sock.recv(1024).decode('utf-8')
    print(message)
    if message == "Welcome to the game!":
        net.send_message(sock, "Connected!")
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
                print("End of turn. Press enter to return to terminal.")
                screen = 'terminal'
                input()
                ss.initialize_terminals()
                ss.update_terminal(active_terminal, active_terminal)

        
def calculate() -> None:
    """
    Helper method for calling calculator() in modules.py. Updates screen accordingly. 
    Parameters: None
    Returns: None
    
    Four parts of response
    Terminal header (i.e CALCULATOR TERMINAL)
    Calculator history
    Letting the user know they are able to input
    Prompt that lets the user know to press "e" to exit
    """
    calculator_header = "\nCALCULATOR TERMINAL\nHistory:\n"
    calculator_footer1 = "Awaiting an equation...\nPress \'e\' to exit the calculator terminal"
    calculator_footer2 = "Type \'calc\' to begin the calculator!"
    calculator_footer3 = "Equation either malformed or undefined! Try again!\nPress \'e\' to exit the calculator terminal"
    
    # Helper function that contructs terminal printing.
    def calculator_terminal_response(footer_option: int) -> str:
        response = calculator_header
        for i in range(len(calculator_history_queue)-1, -1, -1):
            response += calculator_history_queue[i][0]
        if footer_option == 1:
            response += calculator_footer1
        elif footer_option == 2:
            response += calculator_footer2
        elif footer_option == 3:
            response += calculator_footer3
        
        return response
    
    #Helper function to update calculator history
    def update_history(equation: str) -> None:
        global calculator_history_current_capacity

        numLines = (len(equation)//75) + 1
        while(numLines > calculator_history_current_capacity):
            calculator_history_current_capacity += calculator_history_queue[0][1]
            calculator_history_queue.pop(0)
        
        calculator_history_current_capacity -= numLines
        calculator_history_queue.append((equation, numLines))

    # Initial comment in active terminal
    ss.update_quadrant(active_terminal, calculator_terminal_response(1), padding=True)
    # All other work is done on the work line (bottom of the screen)
    while True:
        player_equation = m.calculator()
        if(player_equation == "e"):
            ss.update_quadrant(active_terminal, calculator_terminal_response(2), padding=True)
            break
        elif(player_equation == "error"):
            ss.update_quadrant(active_terminal, calculator_terminal_response(3), padding=True)
        else:
            update_history(player_equation)
            ss.update_quadrant(active_terminal, calculator_terminal_response(1))

def display_balance() -> None:
    """
    Display player's cash, assets, etc. 

    Parameters: None
    Returns: None
    """
    pass

def list_properties() -> None:
    """
    Temporary function to list all properties on the board by calling the property list stored in ascii.txt.
    Can be reworked to add color and better formatting.
    
    Parameters: None
    Returns: None
    """
    ss.update_quadrant(active_terminal, text_dict.get('properties'))

# Probably want to implement threading for printing and getting input.
def get_input() -> None:
    """
    Main loop for input handling while in the terminal screen. Essentially just takes input from user, 
    and if it is valid input, will run command on currently active terminal. 

    Parameters: None
    Returns: None
    """
    global active_terminal, screen
    stdIn = ""

    fishing_gamestate = 'start'

    while(stdIn != "exit" or game_running):
        if screen == 'gameboard':

            # I turned off my brain while writing this part. The player can essentially send any command here
            # and it is only slightly regulated by the server. Better client-side handling is needed. TODO

            stdIn = input(ss.COLORS.backBLACK+'\r').lower().strip()
            if stdIn.isspace() or stdIn == "":
                # On empty input make sure to jump back on the console line instead of printing anew
                ss.overwrite(COLORS.RESET + "\r")
            elif stdIn == "roll":
                net.send_message(sockets[1], 'mply,roll')
            elif stdIn == "b":
                net.send_message(sockets[1], 'mply,trybuy')
            elif stdIn == "p":
                net.send_message(sockets[1], 'mply,propmgmt')
                property_id = ss.get_valid_int("Enter the ID of a property you own: ",1, 40, [0,2,4,7,10,17,20,22,30,33,36,38])
                net.send_message(sockets[1], f'mply,propmgmt,{property_id}')

            elif stdIn == "d":
                net.send_message(sockets[1], 'mply,deed')
                property_id = ss.get_valid_int("Enter a property ID: ",1, 40, [0,2,4,7,10,17,20,22,30,33,36,38])
                net.send_message(sockets[1], f'mply,deed,{property_id}')
            elif stdIn == '':
                net.send_message(sockets[1], 'mply,continue')
            elif stdIn == 'e':
                net.send_message(sockets[1], 'mply,endturn')

        
        elif screen == 'terminal':
            stdIn = input(COLORS.WHITE+'\r').lower().strip()
            if screen == 'gameboard': # If player has been "pulled" into the gameboard, don't process input
                continue
            if stdIn.startswith("help"):
                if (len(stdIn) == 6 and stdIn[5].isdigit() and 2 >= int(stdIn.split(" ")[1]) > 0):
                    ss.update_quadrant(active_terminal, text_dict.get(stdIn if stdIn != 'help 1' else 'help'), padding=True)
                else: 
                    ss.update_quadrant(active_terminal, text_dict.get('help'), padding=True)
                    ss.overwrite(COLORS.RED + "Incorrect syntax. Displaying help first page instead.")
            elif stdIn == "game": # Simply displays the game board. Does not give player control.
                net.send_message(sockets[1], 'request_board')
                board_data = net.receive_message(sockets[1])
                ss.clear_screen()
                print(board_data + ss.set_cursor_str(0, ss.INPUTLINE) + "Viewing Gameboard screen. Press enter to return to Terminal screen.")
                input()
                ss.initialize_terminals() # Reinitialize terminals to clear the screen. TODO restore previous terminals state
                ss.update_terminal(active_terminal, active_terminal)
            elif stdIn == "calc":
                calculate()
            elif stdIn == "bal":
                ss.update_quadrant(active_terminal, f'Cash on hand: {balance}'.center(ss.cols), padding=True)
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
                    ss.update_quadrant(active_terminal, m.deed(stdIn[5:]), padding=True)
            elif stdIn == "disable":
                ss.update_quadrant(active_terminal, m.disable())
            elif stdIn == "kill":
                ss.update_quadrant(active_terminal, m.kill())
            elif stdIn == "exit" or stdIn.isspace() or stdIn == "":
                # On empty input make sure to jump up one console line
                ss.overwrite("\r")
            elif stdIn == "ships":
                # Access game from banker
                net.send_message(sockets[1], 'ships')
                sleep(0.1)
                board_data = net.receive_message(sockets[1])
                ss.update_quadrant(active_terminal, board_data, padding=False)

                # Get current gamestate and respond accordingly
                # gamestate = net.receive_message(sockets[1])

                # if gamestate == f'{name}\'s turn to place ships!':
                #     pass
                
            elif stdIn == "fish":
                fishing_gamestate = 'start'
                while(fishing_gamestate != 'e'):
                    game_data, fishing_gamestate = m.fishing(fishing_gamestate)
                    ss.update_quadrant(active_terminal, game_data, padding=False)
                ss.set_cursor(0, ss.INPUTLINE)

            elif stdIn == "ttt" or stdIn == "tictactoe":
                m.ttt_handler(sockets[1], active_terminal)

            elif stdIn.startswith('reset'):
                ss.calibrate_screen('player')
                ss.clear_screen()
                ss.initialize_terminals()
                ss.update_terminal(active_terminal, active_terminal)
                ss.overwrite(COLORS.GREEN + "Screen calibrated.")
            elif stdIn == "casino":
                import casino
                casino.module(active_terminal, sockets[1])
            else:
                # ss.overwrite('\n' + ' ' * ss.WIDTH)
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
        ss.calibrate_screen('player')

    ss.clear_screen()
    ss.initialize_terminals()
    ss.update_terminal(active_terminal, active_terminal)
    
    # Prints help in quadrant 2 to orient player.
    ss.update_quadrant(2, text_dict.get('help'), padding=True)
    get_input()
    # s.print_w_dots("Goodbye!")

def shutdown():
    os.system("shutdown /s /f /t 3 /c \"Terminal Failure: Bankrupt!\"")