# This file contains the logic for the terminal screen

#TODO rewrite into classes: player & banker
# Terminal total width and height: 150x40
# This matches the default Windows terminal size nicely.
# os.get_terminal_size() should be looked into. 
WIDTH = 150
HEIGHT = 40
INPUTLINE = 45
import os
from style import COLORS
from style import set_cursor, set_cursor_str
from style import get_graphics
from player import gat
import platform
import ctypes
import shutil

# Each quadrant is half the width and height of the screen 
global rows, cols, quadrants
rows = HEIGHT//2
cols = WIDTH//2

quadrants = [['1' * cols] * rows, 
                ['2' * cols] * rows, 
                ['3' * cols] * rows, 
                ['4' * cols] * rows]

def print_board(gameboard: list[str]) -> None:
    """
    Used in printing the gameboard for the player. Overwrites the current screen to display the gameboard. 
    
    Parameters: 
    gameboard (list[str]): A representation of the gameboard as a list of strings. 

    Returns: None
    """
    # clear_screen()
    # Resets cursor position to top left
    print("\033[1A" * (HEIGHT + 4), end='\r')
    
    for y in range(len(gameboard)):
        print(gameboard[y])
    

def update_quadrant(n: int, data: str) -> None:
    """
    Creates a list of lines from the data string, and pads each line with spaces to match the width of the screen. 

    Parameters: 
    n (int): Quadrant number (1-4)
    data (str): String data to update quadrant. Separate lines must be indicated by \\n. 

    Returns: None

    """
    line_list = data.split('\n')
    for i in range(len(line_list)):
            line_list[i] = line_list[i] + ' ' * (cols - len(line_list[i]))
    for i in range(len(line_list), rows):
        line_list.append(' ' * cols)
    quadrants[n-1] = line_list

def update_quadrant_strictly(n: int, data: str):
    """ 
    Same as update_quadrant, but does not pad the lines with spaces.
    
    Could be useful for color formatting where update_quadrant fails.

    Parameters:
    n (int): Quadrant number (1-4)
    data (str): Data to update quadrant. String must be exactly the right length. (i.e. 75*20)

    Returns: None
    """
    line_list = data.split('\n')
    quadrants[n-1] = line_list

def update_quadrant_2(n: int, data: str, padding: bool = False):
    """
    Better quadrant update function.
    This exceeds others because it immediately updates a single quadrant with the new data.
    Previously, the screen would not update until print_screen() was called.
    Furthermore, print_screen() would overwrite the entire screen, which is not ideal / slower. 
    @TODO This function should be used in place of update_quadrant() in all cases.
    @TODO Also need to implement usage corrections to print_screen().
    """
    match n:
        case 1:
            x,y = 2,2
        case 2:
            x,y = cols+3, 2
        case 3:
            x,y = 2, rows+3
        case 4:
            x,y = cols+3, rows+3

    if data: # if any data is passed
        line_list = data.split('\n')
        for i in range(rows):
            set_cursor(x,y+i)
            if padding:
                line_list[i] = line_list[i] + " " * (cols - len(line_list[i]))

            if len(line_list) > i:
                print(line_list[i])
            else:
                print(" " * cols)
        print(COLORS.RESET, end='')
        set_cursor(0,INPUTLINE)
    else:
        for i in range(rows):
            set_cursor(x,y+i)
            print(f'{n}' * cols)

def update_terminal(n: int, x: int, y: int, active: bool = False):
    """

    """
    n = n - 1 # 0-indexed
    c = COLORS.GREEN if active else COLORS.LIGHTGRAY

    border_chars = [('╔','╦','╠','╬'),
                    ('╦','╗','╬','╣'),
                    ('╠','╬','╚','╩'),
                    ('╬','╣','╩','╝')]

    set_cursor(x,y)
    print(c, end='')
    print(border_chars[n][0] + '═' * cols + border_chars[n][1], end='')
    set_cursor(x,y+rows+1)
    print(border_chars[n][2] + '═' * cols + border_chars[n][3], end='')
    for i in range(y, y + rows):
        set_cursor(x, i+1)
        print('║')
        set_cursor(x+cols + (1 if (n + 1) % 2 == 0 else 2), i+1)
        print('║')
    
    set_cursor(0,INPUTLINE)
    print(COLORS.RESET, end='')

def update_active_terminal(n: int):
    """
    Updates the active terminal to the given number.

    Parameters:
    n (int): The terminal number to set as active.
    
    Returns: None
    """
    old_terminal = gat()
    active_terminal = n 
    x,y = -1,-1

    match old_terminal:
        case 1:
            x,y = 0,1
        case 2:
            x,y = cols+2, 1
        case 3:
            x,y = 0, rows+2
        case 4:
            x,y = cols+2, rows+2
    update_terminal(old_terminal, x, y, False)

    match active_terminal:
        case 1:
            x,y = 0,1
        case 2:
            x,y = cols+2, 1
        case 3:
            x,y = 0, rows+2
        case 4:
            x,y = cols+2, rows+2
    update_terminal(active_terminal, x, y, True)
    

def overwrite(text: str = ""):
    """
    Writes text over 2nd to last line of the terminal (input line).
    
    Use this method regularly.
    
    Parameters: 
    text (str): The text to overwrite with. Default is empty string.

    Returns: None
    """
    set_cursor(0, INPUTLINE)
    print(f'\033[1A\r{COLORS.RESET}{text}', end=' ' * (WIDTH - len(text)) + '\n' + ' ' * WIDTH + '\r')

def clear_screen():
    """
    Naively clears the terminal screen.

    Parameters: None
    Returns: None
    """
    print(COLORS['RESET'],end='')
    os.system('cls' if os.name == 'nt' else 'clear')

# def print_screen() -> None:
#     """
#     This function overwrites the previous terminal's display. 
    
#     Because Terminal Monopoly is not supposed to 
#     repeatedly print lines after lines (there should be no scrollbar in the terminal), this function overwrites 
#     all needed information. 
    
#     The class variables quadrants[0], quadrants[1], etc. are iterated through to print each character. Because
#     splitting the terminal is entirely artificial to this program, it stops at a hardcoded width value and 
#     begins printing the next quadrant.  
    
#     Parameters: None
#     Returns: None
#     """

#     # Resets cursor position to top left
#     print("\033[1A" * (HEIGHT + 4), end='\r')
#     # Prints the top border, with ternary conditions if terminal 1 or 2 are active
#     print(COLORS.backBLACK + COLORS.LIGHTGRAY+(COLORS.GREEN+'╔' if active_terminal == 1 else '╔')+('═' * (cols))+
#         (COLORS.GREEN if active_terminal == 1 or active_terminal == 2 else COLORS.LIGHTGRAY) +'╦'
#         +(COLORS.GREEN if active_terminal == 2 else COLORS.LIGHTGRAY)+('═' * (cols))+'╗' + COLORS.LIGHTGRAY + "   ") # Additional spaces to fill remaining 3 columns
    
#     # Prints the middle rows
#     for y in range(rows):
#         print((COLORS.GREEN if active_terminal == 1 else COLORS.LIGHTGRAY)+'║', end=COLORS.RESET) 
#         for x in range(2*cols):
#             if x < cols:
#                 print(quadrants[0][y][x], end='')
#             elif x == cols:
#                 print((COLORS.GREEN if active_terminal == 1 or active_terminal == 2 else COLORS.LIGHTGRAY)+'║'+COLORS.RESET + quadrants[1][y][x - cols], end='')
#             else:
#                 print(quadrants[1][y][x-cols], end='') 
#         print((COLORS.GREEN if active_terminal == 2 else COLORS.LIGHTGRAY)+'║'+COLORS.RESET + "   ")
    
#     # Middle divider
#     print((COLORS.GREEN if active_terminal == 1 or active_terminal == 3 else COLORS.LIGHTGRAY)+'╠' + '═' * (cols)
#         +COLORS.GREEN + '╬' + (COLORS.GREEN if active_terminal == 2 or active_terminal == 4 else COLORS.LIGHTGRAY)+ '═' * (cols) + '╣' + COLORS.RESET + "   ")
    
#     # Prints the bottom rows
#     for y in range(rows):
#         print((COLORS.GREEN if active_terminal == 3 else COLORS.LIGHTGRAY)+'║', end=COLORS.RESET) 
#         for x in range(2 * cols):
#             if x < cols:
#                 print(quadrants[2][y][x], end='')
#             elif x == cols:
#                 print((COLORS.GREEN if active_terminal == 3 or active_terminal == 4 else COLORS.LIGHTGRAY)+'║'+COLORS.RESET + quadrants[3][y][x - cols], end='')
#             else:
#                 print(quadrants[3][y][x - cols], end='')
#         print((COLORS.GREEN if active_terminal == 4 else COLORS.LIGHTGRAY)+'║'+COLORS.RESET + "   ")
    
#     # Print final row
#     print((COLORS.GREEN if active_terminal == 3 else COLORS.LIGHTGRAY)+'╚' + '═' * (cols) + 
#         (COLORS.GREEN if active_terminal == 3 or active_terminal == 4 else COLORS.LIGHTGRAY) +'╩'
#             + (COLORS.GREEN if active_terminal == 4 else COLORS.LIGHTGRAY) + '═' * (cols) + '╝'+ COLORS.RESET + "   ")
#     # Fills the rest of the terminal
#     print(' ' * WIDTH, end='\r')
#     set_cursor(0,INPUTLINE)

def initialize_terminals():
    update_quadrant_2(1, data=None)
    update_quadrant_2(2, data=None)
    update_quadrant_2(3, data=None)
    update_quadrant_2(4, data=None)
    update_active_terminal(1)

def make_fullscreen():
    current_os = platform.system()

    if current_os == "Windows":
        # Maximize terminal on Windows
        user32 = ctypes.WinDLL("user32")
        SW_MAXIMIZE = 3
        hWnd = user32.GetForegroundWindow()
        user32.ShowWindow(hWnd, SW_MAXIMIZE)

    elif current_os == "Linux" or current_os == "Darwin":
        # Maximize terminal on Linux/macOS
        os.system("printf '\033[9;1t'")
    else:
        print(f"Fullscreen not supported for OS: {current_os}")

def print_with_wrap(char, start_row, start_col):
    # Get the terminal size
    terminal_size = shutil.get_terminal_size()
    width = terminal_size.columns
    
    # If the position exceeds the terminal width, handle wrapping
    if start_col >= width:
        # Calculate new row and column if it exceeds width
        new_row = start_row + (start_col // width)
        new_col = start_col % width
        print(f"\033[{new_row};{new_col}H" + char, end="")
    else:
        # Default print
        print(f"\033[{start_row};{start_col}H" + char, end="")


def calibrate_screen(type: str) -> None:
    terminal_size = shutil.get_terminal_size()
    from monopoly import print_commands
    width = terminal_size.columns
    os.system('cls' if os.name == 'nt' else 'clear')
    current_os = platform.system()

    ## add color calibration here too

    if current_os == "Darwin":
        # Print out instructions for macOS users
        print("Please use Ctrl + \"Command\" + \"+\" or Ctrl + \"Command\" + \"-\" to zoom in/out and ensure everything is visible. Press enter to continue to scaling screen.")
    else:
        # Print out instructions for Linux/Windows users
        print("Please use \"Ctrl\" + \"-\" or \"Ctrl\" + \"+\" to zoom in/out and ensure everything is visible. Press enter to continue to scaling screen.")
    print("Proper scaling should only displays 4 cross that marks the corners of the board.")
    print("If you are having trouble with scaling, try entering r to reset the display.")
    print("After finishing scaling, please press enter to continue.")
    scaling_test = input()
    os.system('cls' if os.name == 'nt' else 'clear')
    if type == "gameboard":
        gameboard = get_graphics().get('gameboard')
        border = get_graphics().get('history and status').split('\n')
        history = []
        print(f"\033[0;0H" + gameboard, end="")
        for i in range(len(border)):
            print(f"\033[{i};79H", end="")
            if(len(history) - i<= 0):
                for j in range(len(border[i])):
                    print(border[i][j], end="")
        print_commands()
        print_with_wrap("X", 0, 0)
        print_with_wrap("X", 0, 156)
        print_with_wrap("X", 50, 156)
        print_with_wrap("X", 50, 0)
        print(f"\033[36;0H" + "Press enter to play or enter r to reset the display.", end="")
        scaling_test = input()
        while scaling_test != "":
            if scaling_test == "r":
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"\033[0;0H" + gameboard, end="")
                for i in range(len(border)):
                    print(f"\033[{i};79H", end="")
                    if(len(history) - i<= 0):
                        for j in range(len(border[i])):
                            print(border[i][j], end="")
                print_commands()
                print_with_wrap("X", 0, 0)
                print_with_wrap("X", 0, 156)
                print_with_wrap("X", 50, 156)
                print_with_wrap("X", 50, 0)
                print(f"\033[36;0H" + "Press enter to play or enter r to reset the display.", end="")
            scaling_test = input()
    elif type == "player":
        os.system('cls' if os.name == 'nt' else 'clear')
        initialize_terminals()

        print_with_wrap("X", 0, 0)
        print_with_wrap("X", 0, 153)
        print_with_wrap("X", 43, 153)
        print_with_wrap("X", 43, 0)
        print(f"\033[44;0H" + "Press enter to play or enter r to reset the display.", end="")
        scaling_test = input()
        while scaling_test != "":
            os.system('cls' if os.name == 'nt' else 'clear')
            initialize_terminals()
            print_with_wrap("X", 0, 0)
            print_with_wrap("X", 0, 153)
            print_with_wrap("X", 43, 153)
            print_with_wrap("X", 43, 0)
            print(f"\033[44;0H" + "Press enter to play or enter r to reset the display.", end="")
            scaling_test = input()
        os.system('cls' if os.name == 'nt' else 'clear')