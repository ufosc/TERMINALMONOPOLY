import os
import socket
from time import sleep
import style as s
from style import COLORS
import screenspace as ss
import modules as m
import networking as net

game_running = False
text_dict = {}
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

    # temp vbls for local testing
    # ADDRESS = '192.168.56.1'
    # PORT = '3131'

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

    s.print_w_dots("Attempting to connect to Banker's receiver...")
    sleep(1)
    try:
        sockets[1].connect((ADDRESS, int(PORT)+1))
    except Exception as e:
        print(e)
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
    message = sock.recv(1024).decode('utf-8')
    print(message)
    if message == "Welcome to the game!":
        sock.send(bytes("Connected!", 'utf-8'))
        return message
    else:
        s.print_w_dots(COLORS.RED+"Handshake failed. Reason: Connected to wrong foreign socket.")

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
            ss.update_quadrant(active_terminal, calculator_terminal_response(1), padding=True)

def balance() -> None:
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
    ss.update_quadrant(active_terminal, text_dict.get('properties'), padding=True)

def game_input() -> None:
    """
    Main loop for ALL client-server interactions. Displays the gameboard. 
    Should take over "get_input" as input handler during this time, until stdIn == "back" 
    indicating return to terminal screen.

    Parameters: None
    Returns: None
    """
    stdIn = ""
    board = ["" for i in range(35)]
    try:
        sockets[1].send('request_board'.encode())
        sleep(0.1)

        size = sockets[1].recv(4)
        board_pieces = ""
        board_pieces = sockets[1].recv(int.from_bytes(size)).decode()
        sleep(0.1)
        board = m.make_board(board_pieces)
        ss.clear_screen()
        ss.print_board(board) ## Failing line
    except Exception as e:
        ss.overwrite(COLORS.RED + "Something went wrong. The Banker may not be ready to start the game.\n")
        print(e)
    
    while(stdIn != "back"):
        print(COLORS.GREEN+"Monopoly Screen: Type 'back' to return to the main menu.")
        stdIn = input(ss.COLORS.backBLACK+'\r').lower().strip()
        if stdIn == "back":
            print('backed out of game...')
            # Breaks the loop, returns to get_input() 
            return
        elif stdIn == "exit" or stdIn.isspace() or stdIn == "":
            # On empty input make sure to jump back on the console line instead of printing anew
            ss.overwrite(COLORS.RESET + "\n\r")
        else:
            # ss.overwrite('\n' + ' ' * ss.WIDTH)
            ss.overwrite(COLORS.RESET + COLORS.RED + "Invalid command. Type 'help' for a list of commands.")

    # sockets[1].close()

# Probably want to implement threading for printing and getting input.
def get_input() -> None:
    """
    Main loop for input handling while in the terminal screen. Essentially just takes input from user, 
    and if it is valid input, will run command on currently active terminal. 

    Parameters: None
    Returns: None
    """
    global active_terminal
    stdIn = ""

    fishing_gamestate = 'start'

    while(stdIn != "exit"):
        stdIn = input(COLORS.WHITE+'\r').lower().strip()
        if stdIn.startswith("help"):
            if (len(stdIn) == 6 and stdIn[5].isdigit() and 2 >= int(stdIn.split(" ")[1]) > 0):
                ss.update_quadrant(active_terminal, text_dict.get(stdIn if stdIn != 'help 1' else 'help'), padding=True)
            else: 
                ss.update_quadrant(active_terminal, text_dict.get('help'), padding=True)
                ss.overwrite(COLORS.RED + "Incorrect syntax. Displaying help first page instead.")
        elif stdIn == "game":
            game_input()
            stdIn = ""
            # stdIn = 'term 1'
        elif stdIn == "calc":
            calculate()
        elif stdIn == "bal":
            balance()
        elif stdIn == "list":
            list_properties()
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
            sockets[1].send('ships'.encode())
            sleep(0.1)
            board_data = net.receive_message(sockets[1])
            ss.update_quadrant(active_terminal, board_data, padding=False)

            # Get current gamestate and respond accordingly
            gamestate = net.receive_message(sockets[1])

            if gamestate == f'{name}\'s turn to place ships!':
                pass
            
        elif stdIn == "fish":
            fishing_gamestate = 'start'
            while(fishing_gamestate != 'e'):
                game_data, fishing_gamestate = m.fishing(fishing_gamestate)
                ss.update_quadrant(active_terminal, game_data, padding=False)

            ss.set_cursor(0, ss.INPUTLINE)
 
        elif stdIn.startswith('reset'):
            ss.calibrate_screen('player')
            ss.clear_screen()
            ss.initialize_terminals()
            ss.overwrite(COLORS.GREEN + "Screen calibrated.")
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