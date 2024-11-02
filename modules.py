import screenspace as ss
import style as s
from modules_directory.fishing import fishing_game
from modules_directory.tictactoe import destruct_board, construct_board
from socket import socket as Socket
import networking as net
import keyboard
import time

def calculator() -> str:
    """A simple calculator module that can perform basic arithmetic operations."""
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

    response = '\nCALCULATOR TERMINAL\n' 
    digit_result = 0
    print("\r", end='')
    equation = input(s.COLORS.GREEN)
    if(equation == "e"):
        return equation
    
    #Trims unnecessary spaces and pads operators with spaces
    equation = equation.replace(" ", "")
    for op in ['+', '-', '*', '/', '%', '^']:
        equation = equation.replace(op, " " + op + " ")
    
    #Removes spaces from negative number
    if(len(equation) > 1 and equation[1] == '-'):
        equation = "-" + equation[3:]

    try:
        digit_result = calculate(equation)
    except:
        return "error"
        
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

    print(s.COLORS.RESET, end='')
    return wrappedResponse

def list_properties() -> str:
    """
    Lists all properties on the board by calling the property list stored in ascii.txt.
    
    Parameters: None
    Returns: None
    """
    ret_val = ""
    props = s.get_graphics().get('properties').split('\n')
    for prop in props:
        if prop == '': 
            ret_val += ' '.center(75) + '\n' 
            continue
        first_word = prop.split()[0]
        color = getattr(s.COLORS, first_word.upper(), s.COLORS.RESET)
        centered_prop = prop.center(75)
        ret_val +=color+ centered_prop + s.COLORS.RESET + '\n'
    return ret_val

def trade():
    pass

def mortgage():
    pass

def roll():
    pass

def gamble():
    pass

def attack():
    pass

def stocks():
    pass

def ttt_handler(server: Socket, active_terminal: int):
    net.send_message(server, 'ttt,getgamestate')
    time.sleep(0.1)
    game_data = net.receive_message(server)
    game_id = None 

    def get_printable_board(upper_text: str, board_data: str, lower_text) -> str:
        return f"{upper_text}\n{board_data}\n{lower_text}\nUse WASD to move, Enter to select, Esc to cancel."

    if 'create a new' in game_data:
        ss.update_quadrant(active_terminal, game_data, padding=True)
        game_id = ss.get_valid_int(prompt='Enter the game id: ', min_val=-1, max_val=0)
        if game_id == -1: # If creating a new game, ask who else is playing.
            while True:
                ss.update_quadrant(active_terminal, "1: Player 1\n2: Player 2\n3: Player 3\n4: Player 4", padding=True)  # @ TODO: This is hardcoded for now, but should be dynamic
                opponent = ss.get_valid_int(prompt=f"Enter the opponent's ID (1-4), not including your ID): ",
                                            min_val=1, max_val=4)-1 # -1 for zero-indexing

                net.send_message(server, f'ttt,joingame,{game_id},{opponent}')
                ss.update_quadrant(active_terminal, "Attempting to join game...", padding=True)
                game_data = net.receive_message(server)
                if 'select a game' in game_data or (('X' in game_data and 'O' in game_data and (not '▒' in game_data)) or '▒' in game_data):
                    break
                else:
                    ss.update_quadrant(active_terminal, game_data + "\nEnter to continue...", padding=True)
                    input()
        else: 
            ss.update_quadrant(active_terminal, "Not creating a new game.", padding=True)

    if 'select a game' in game_data:
        ss.update_quadrant(active_terminal, game_data, padding=True)    
        game_id = ss.get_valid_int(prompt='Enter the game id: ', min_val=-1, max_val=10) # 10 is incorrect! temp for now @TODO
        # Send the server the game id to join. Should be validated on server side. 
        net.send_message(server, f'ttt,joingame,{game_id}')

        # Wait for server to send back the new board
        game_data = net.receive_message(server)
        ss.update_quadrant(active_terminal, game_data, padding=True)

    if ('X' in game_data and 'O' in game_data and (not '▒' in game_data)) or '▒' in game_data: # If the game data sent back is a board, then we can play the game
        # @TODO check this is going to work with player name's that have 'X' or 'O' in them, or hell, with the '▒' character
        simple_board = destruct_board(game_data)
        original_board = destruct_board(game_data)
        x,y = 0,0
        b = construct_board(simple_board)
        ss.update_quadrant(active_terminal, get_printable_board("New board:", b, f"Coordinates:\n({x},{y})"))

        # Only hook the keyboard after you are definitely IN a game. 
        ss.indicate_keyboard_hook(active_terminal) # update terminal border to show keyboard is hooked

        while True:

            if keyboard.read_event().event_type == keyboard.KEY_DOWN:
                simple_board[y][x] = s.COLORS.RESET + original_board[y][x]
                b = construct_board(simple_board)
                ss.update_quadrant(active_terminal, get_printable_board("New board:", b, f"Coordinates:\n({x},{y})"))

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
            ss.update_quadrant(active_terminal, get_printable_board("New board:", b, f"Coordinates:\n({x},{y})"))
            
            if keyboard.is_pressed('enter'):
                # Send move to server
                if '▒' in simple_board[y][x]:
                    # At this point, the client can be sure that they have the
                    # correct game ID and that the move is valid. Thus, we add
                    # the game ID to the move string.
                    net.send_message(server, f'ttt,move,{game_id},{x}.{y}')
                    # receive new board (for display) from server
                    ss.update_quadrant(active_terminal, "Updated board:\n" + net.receive_message(server), padding=True)
                    ss.update_terminal(active_terminal, active_terminal) # reset terminal to normal
                    keyboard.unhook_all()
                    break
                else:
                    ss.update_quadrant(active_terminal, get_printable_board("New board:", b, f"Coordinates:\n({x},{y})\nInvalid move. Try again."))

            if keyboard.is_pressed('esc'):
                ss.update_terminal(active_terminal, active_terminal) # reset terminal to normal
                keyboard.unhook_all()
                break

def battleship(server: Socket, gamestate: str) -> str:
    net.send_message(server, 'battleship')

fishing_game_obj = fishing_game() # fishing is played LOCALLY, not over the network
def fishing(gamestate: str) -> tuple[str, str]:
    """
    Fishing module handler for player.py. Returns tuple of [visual data, gamestate] both as strings.
    """
    stdIn = ''
    match gamestate:
        case 'start':
            return fishing_game_obj.start(), 'playing'
        case 'playing':
            stdIn = fishing_game_obj.get_input()
            if stdIn == 'e':
                return '', 'e'
            return fishing_game_obj.results(), 'e'  
        case 'e':
            return '', 'start'  

def kill() -> str:
    return s.get_graphics()['skull']

def disable() -> str:
    result = ('X ' * round(ss.cols/2+0.5) + '\n' + 
                (' X' * round(ss.cols/2+0.5)) + '\n'
                ) * (ss.rows//2)
    return result

def make_board(board_pieces) -> list[str]:
    board = [''] * 35
    # Hard coded for board printing specifically
    for i in range(35):
        for j in range(80):
            if board_pieces[i*80+j] != '\n':
                board[i] += (board_pieces[i*80+j])
    return board

