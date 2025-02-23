import screenspace as ss
from screenspace import Terminal
import style as s
from style import graphics as g
from modules_directory.fishing import fishing_game
from modules_directory.tictactoe import destruct_board, construct_board
import shop
from socket import socket as Socket
import networking as net
import keyboard
import time

calculator_history_queue = []
calculator_history_current_capacity = 15

class Inventory():
    def __init__(self):
        """
        Initializes the inventory of the player.
        The inventory is a dictionary of items and their quantities.
        All items are stored here, to be extracted by the shop module.
        """
        self.items = {}
    
    def getinventory(self) -> dict:
        """
        Returns the inventory of the player.
        """
        return self.items
    
    def add_item(self, item: str, quantity: int) -> None:
        """
        Adds an item to the inventory.
        If the item already exists, it adds the quantity to the existing item.
        This could be a fish, or a Terminal upgrade, or an attack Module. 
        """
        if item in self.items:
            self.items[item] += quantity
        else:
            self.items[item] = quantity
    
    def remove_item(self, item: str, quantity: int) -> None:
        """
        Removes an item from the inventory.
        If the item does not exist, it does nothing.
        If the quantity is greater than the quantity of the item, it removes all of the item.
        """
        if item in self.items:
            if self.items[item] > quantity:
                self.items[item] -= quantity
            else:
                del self.items[item]

def calculator(active_terminal: Terminal) -> str:
    # Helper function that contructs terminal printing.
    def calculator_terminal_response(footer_option: int) -> str:
        calculator_header = "\nCALCULATOR TERMINAL\nHistory:\n"
        footer_options = ["Awaiting an equation...\nPress 'e' to exit the calculator terminal.", 
                      s.COLORS.BLUE+"Type 'calc' to begin the calculator!", 
                      s.COLORS.RED+"Equation either malformed or undefined! Try again!\nPress 'e' to exit the calculator terminal"+s.COLORS.RESET]
        response = calculator_header
        for i in range(len(calculator_history_queue)-1, -1, -1):
            response += calculator_history_queue[i][0]
        response += '\n' + footer_options[footer_option]
        
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

    #Uses recursion to calculate.
    def calculate(equation: str) -> float:
        for i in range(0, len(equation)-1):
            if(equation[i] == '+'):
                eqLeft = equation[:i]
                eqRight = equation[(i+1):]
                return calculate(eqLeft) + calculate(eqRight)
        
        for i in range(0, len(equation)-1):
            if(equation[i] == '-'):
                #Checks for unary operator '-'
                if(i == 0):
                    eqLeft = "0"
                else:
                    eqLeft = equation[:i]
                eqRight = equation[(i+1):]
                return calculate(eqLeft) - calculate(eqRight)
        
        for i in range(0, len(equation)-1):
            if(equation[i] == '*'):
                eqLeft = equation[:i]
                eqRight = equation[(i+1):]
                return calculate(eqLeft) * calculate(eqRight)

        for i in range(0, len(equation)-1):
            if(equation[i] == '/'):
                eqLeft = equation[:i]
                eqRight = equation[(i+1):]
                return calculate(eqLeft)/calculate(eqRight)
        
        for i in range(0, len(equation)-1):
            if(equation[i] == '%'):
                eqLeft = equation[:i]
                eqRight = equation[(i+1):]
                return calculate(eqLeft)%calculate(eqRight) 
            
        for i in range(0, len(equation)-1):
            if(equation[i] == '^'):
                eqLeft = equation[:i]
                eqRight = equation[(i+1):]
                return calculate(eqLeft) ** calculate(eqRight)
        
        return float(equation)

    # Initial comment in active terminal
    active_terminal.update(calculator_terminal_response(0), padding=True)
    # All other work is done on the work line (bottom of the screen)
    while True:
            
        response = '\nCALCULATOR TERMINAL\n' 
        digit_result = 0
        print("\r", end='')
        equation = input(s.COLORS.GREEN)
        print(s.COLORS.RESET, end="")
        if(equation == "e"):
            active_terminal.update(calculator_terminal_response(1), padding=True)
            break

        #Trims unnecessary spaces and pads operators with spaces
        equation = equation.replace(" ", "")
        for op in ['+', '-', '*', '/', '%', '^']:
            equation = equation.replace(op, " " + op + " ")
        #Removes spaces from negative number
        if(len(equation) > 1 and equation[1] == '-'):
            equation = "-" + equation[3:]

        try:
            digit_result = calculate(equation)
            responseEQ = f'{equation} = {digit_result}'

            #There are 75 columns for each terminal, making any string longer than 75 characters overflow.
            numOverflowingChar = len(responseEQ) - 75
            lineNumber = 0
            wrappedResponse = ""
            while(numOverflowingChar > 0):
                wrappedResponse += responseEQ[(75*lineNumber):(75*(lineNumber + 1))] + '\n'
                lineNumber = lineNumber + 1
                numOverflowingChar = numOverflowingChar - 75
            
            wrappedResponse += responseEQ[(75*lineNumber):(75*(lineNumber + 1)) + numOverflowingChar] + '\n'
            #response += wrappedResponse

            player_equation = wrappedResponse

            print(s.COLORS.RESET, end='')
            update_history(player_equation)
            active_terminal.update(calculator_terminal_response(0))
        except:
            active_terminal.update(calculator_terminal_response(2), padding=True)

def list_properties() -> str:
    """
    Lists all properties on the board by calling the property list stored in graphics.
    
    Parameters: None
    Returns: None
    """
    ret_val = ""
    props = g.get('properties').split('\n')
    for prop in props:
        if prop == '': 
            ret_val += ' '.center(75) + '\n' 
            continue
        first_word = prop.split()[0]
        color = getattr(s.COLORS, first_word.upper(), s.COLORS.RESET)
        centered_prop = prop.center(75)
        ret_val +=color+ centered_prop + s.COLORS.RESET + '\n'
    return ret_val

def ttt_handler(server: Socket, active_terminal: Terminal, player_id: int) -> None:
    net.send_message(server, f'{player_id}ttt,getgamestate')
    time.sleep(0.1)
    active_terminal.update("Waiting for server...", padding=True)
    game_data = net.receive_message(server)
    game_id = None 

    def get_printable_board(upper_text: str, board_data: str, lower_text) -> str:
        return f"{upper_text}\n{board_data}\n{lower_text}\nUse WASD to move, Enter to select, Esc to cancel."

    if 'create a new' in game_data:
        active_terminal.update(game_data, padding=True)
        game_id = ss.get_valid_int(prompt='Enter the game id: ', min_val=-1, max_val=0)
        if game_id == -1: # If creating a new game, ask who else is playing.
            while True:
                active_terminal.update("1: Player 1\n2: Player 2\n3: Player 3\n4: Player 4", padding=True)  # TODO: This is hardcoded for now, but should be dynamic
                opponent = ss.get_valid_int(prompt=f"Enter the opponent's ID (1-4), not including your ID): ",
                                            min_val=1, max_val=4)-1 # -1 for zero-indexing

                net.send_message(server, f'{player_id}ttt,joingame,{game_id},{opponent}')
                active_terminal.update("Attempting to join game...", padding=True)
                game_data = net.receive_message(server)
                if 'select a game' in game_data or (('X' in game_data and 'O' in game_data and (not '▒' in game_data)) or '▒' in game_data):
                    break
                else:
                    active_terminal.update(game_data + "\nEnter to continue...", padding=True)
                    input()
        else: 
            active_terminal.update("Not creating a new game.", padding=True)

    if 'select a game' in game_data:
        active_terminal.update(game_data, padding=True)    
        game_id = ss.get_valid_int(prompt='Enter the game id: ', min_val=-1, max_val=10) # 10 is incorrect! temp for now TODO
        # Send the server the game id to join. Should be validated on server side. 
        net.send_message(server, f'{player_id}ttt,joingame,{game_id}')

        # Wait for server to send back the new board
        game_data = net.receive_message(server)
        active_terminal.update(game_data, padding=True)

    if ('X' in game_data and 'O' in game_data and (not '▒' in game_data)) or '▒' in game_data: # If the game data sent back is a board, then we can play the game
        # TODO check this is going to work with player name's that have 'X' or 'O' in them, or hell, with the '▒' character
        simple_board = destruct_board(game_data)
        original_board = destruct_board(game_data)
        x,y = 0,0
        b = construct_board(simple_board)
        active_terminal.update(get_printable_board("New board:", b, f"Coordinates:\n({x},{y})"))

        # Only hook the keyboard after you are definitely IN a game. 
        ss.indicate_keyboard_hook(active_terminal.index) # update terminal border to show keyboard is hooked

        while True:

            if keyboard.read_event().event_type == keyboard.KEY_DOWN:
                simple_board[y][x] = s.COLORS.RESET + original_board[y][x]
                b = construct_board(simple_board)
                active_terminal.update(get_printable_board("New board:", b, f"Coordinates:\n({x},{y})"))

            if keyboard.is_pressed('w'):
                y = max(0, min(y-1, 2))
            if keyboard.is_pressed('a'):
                x = max(0, min(x-1, 2))
            if keyboard.is_pressed('s'):
                y = max(0, min(y+1, 2))
            if keyboard.is_pressed('d'):
                x = max(0, min(x+1, 2))

            simple_board[y][x] = s.COLORS.backYELLOW + original_board[y][x] + s.COLORS.RESET
            time.sleep(0.05)
            b = construct_board(simple_board)
            active_terminal.update(get_printable_board("New board:", b, f"Coordinates:\n({x},{y})"))
            
            if keyboard.is_pressed('enter'):
                # Send move to server
                if '▒' in simple_board[y][x]:
                    # At this point, the client can be sure that they have the
                    # correct game ID and that the move is valid. Thus, we add
                    # the game ID to the move string.
                    net.send_message(server, f'{player_id}ttt,move,{game_id},{x}.{y}')
                    # receive new board (for display) from server
                    active_terminal.update("Updated board:\n" + net.receive_message(server), padding=True)
                    ss.update_terminal(active_terminal.index, active_terminal.index) # reset terminal to normal
                    keyboard.unhook_all()
                    break
                else:
                    active_terminal.update(get_printable_board("New board:", b, f"Coordinates:\n({x},{y})\nInvalid move. Try again."))

            if keyboard.is_pressed('esc'):
                ss.update_terminal(active_terminal.index, active_terminal.index) # reset terminal to normal
                keyboard.unhook_all()
                break

fishing_game_obj = fishing_game() # fishing is played LOCALLY, not over the network
def fishing(gamestate: str, inventory: Inventory) -> tuple[str, str]:
    """
    Fishing module handler for player.py. Returns tuple of [visual data, gamestate] both as strings.
    """
    stdIn = ''
    if (gamestate == 'start'):
        return fishing_game_obj.start(inventory), 'playing'
    elif (gamestate == 'playing'):
        stdIn = fishing_game_obj.get_input()
        if stdIn == 'e':
            return '', 'e'
        return fishing_game_obj.results(), 'e'  
    elif (gamestate == 'e'):
        return '', 'start'  

def shop_handler(inventory: Inventory, active_terminal: Terminal) -> str:
    active_terminal.update(shop.Shop(inventory).display_shop()) # temporary, will be replaced with banker Shop communication

def kill() -> str:
    return g.get('skull')

def disable() -> str:
    result = ('X ' * round(ss.cols/2+0.5) + '\n' + 
                (' X' * round(ss.cols/2+0.5)) + '\n'
                ) * (ss.rows//2)
    return result

