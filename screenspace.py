# This file contains the logic for the terminal screen

# Terminal total width and height: 150x40
WIDTH = 150
HEIGHT = 40
INPUTLINE = 45
import os
from style import COLORS
from style import set_cursor, set_cursor_str
from style import get_graphics
import platform
import ctypes
import shutil
import re

# Each quadrant is half the width and height of the screen 
global rows, cols
rows = HEIGHT//2
cols = WIDTH//2

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

def notification(msg: str, n: int, color: str) -> str:
    message = message + " " * max(0, (78 - len(message)))
        # Max 78 character popup for messaging the player.
    match n:
        case 1:
            x,y = 2+10,2+5
        case 2:
            x,y = cols+3+10, 2+5
        case 3:
            x,y = 2+10, rows+3+5
        case 4:
            x,y = cols+3+10, rows+3+5
        case -1:
            x,y = cols - 20, rows - 5

    p = color + set_cursor_str(x, y)
    outline = get_graphics()["popup 1"].split("\n")
    for i in range(len(outline)):
        p += set_cursor_str(x, y+i) + outline[i]
        if 0 < i < 4:
            # Custom text wrapping
            p += set_cursor_str(x+2, y+i) + message[(i-1)*26:(i-1)*26+26]
    writeto += p
    return writeto


def replace_sequence(match, x, y):
    # Extract the number N from the matched string
    nx = int(match.group(2))
    ny = int(match.group(1))

    # Calculate the new x and y coordinates
    new_x = nx + x
    new_y = ny + y
    # Return the new sequence
    return f"\033[{new_y};{new_x}H"

def update_quadrant(n: int, data: str, padding: bool = True):
    """
    Better quadrant update function.
    This exceeds others because it immediately updates a single quadrant with the new data.
    Previously, the screen would not update until print_screen() was called.
    Furthermore, print_screen() would overwrite the entire screen, which is not ideal and slower. 

    Set padding = True if you're not sure whether your module needs padding. 
    """

    # Sets the x and y coordinates based on the quadrant number corresponding to the top left corner of the quadrant plus border padding.
    match n:
        case 1:
            x,y = 2,2
        case 2:
            x,y = cols+3, 2
        case 3:
            x,y = 2, rows+3
        case 4:
            x,y = cols+3, rows+3

    if data:

        # These lines are taking any additional string fragments that use "set_cursor_string()" from 
        # style.py and update the x,y coordinates to 

        pattern = r'\033\[(\d+);(\d+)H'
        data = re.sub(pattern, lambda m: replace_sequence(m, x, y), data)
        
        line_list = data.split('\n')
        if len(line_list) > rows and padding:
            line_list = line_list[:rows] # Truncate if necessary bc someone might send a long string
        for i in range(len(line_list)):
            set_cursor(x,y+i)
            if padding:
                line_list[i] = line_list[i] + " " * (cols - len(line_list[i]))

            print(line_list[i][:cols] if len(line_list[i]) > cols and padding else line_list[i]) # Truncate if necessary bc someone might send a long string
        for i in range(len(line_list), rows):
            set_cursor(x,y+i)
            print(" " * cols)

        print(COLORS.RESET, end='')
        set_cursor(0,INPUTLINE)
    else:
        for i in range(rows):
            set_cursor(x,y+i)
            print(f'{n}' * cols)
        set_cursor(x=x-12 + cols//2, y= y-2+rows//2)
        print('╔══════════════════════╗')
        
        set_cursor(x=x-12 + cols//2, y= y-1+rows//2)
        print('║ Awaiting commands... ║')

        set_cursor(x=x-12 + cols//2, y= y-0+rows//2)
        print('╚══════════════════════╝')


def update_terminal(n: int, o: int):
    """
    Updates the terminal border to indicate the active terminal. Turns off the border for the inactive terminal.
    """
    x,y = -1,-1
    border_chars = [('╔','╦','╠','╬'),
                    ('╦','╗','╬','╣'),
                    ('╠','╬','╚','╩'),
                    ('╬','╣','╩','╝')]
    
    match o: 
        case 1:
            x,y = 0,1
        case 2:
            x,y = cols+2, 1
        case 3:
            x,y = 0, rows+2
        case 4:
            x,y = cols+2, rows+2
    o = o - 1 # 0-indexed
    c = COLORS.LIGHTGRAY
    set_cursor(x,y)
    print(c, end='')
    print(border_chars[o][0] + '═' * cols + border_chars[o][1], end='')
    set_cursor(x,y+rows+1)
    print(border_chars[o][2] + '═' * cols + border_chars[o][3], end='')
    for i in range(y, y + rows):
        set_cursor(x, i+1)
        print('║')
        set_cursor(x+cols + (1 if (o + 1) % 2 == 0 else 2), i+1)
        print('║')

    match n:
        case 1:
            x,y = 0,1
        case 2:
            x,y = cols+2, 1
        case 3:
            x,y = 0, rows+2
        case 4:
            x,y = cols+2, rows+2
    n = n - 1 # 0-indexed
    c = COLORS.GREEN

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
    
def overwrite(text: str = ""):
    """
    Writes text over 2nd to last line of the terminal (input line).
    
    Use this method regularly.
    
    Parameters: 
    text (str): The text to overwrite with. Default is empty string.

    Returns: None
    """
    set_cursor(0, INPUTLINE)
    print(f'\033[1A\r{COLORS.RESET}{text}', end=' ' * (WIDTH - len(text) + 3) + '\n' + ' ' * (WIDTH + 3) + '\r')

def clear_screen():
    """
    Naively clears the terminal screen.

    Parameters: None
    Returns: None
    """
    print(COLORS.RESET,end='')
    os.system('cls' if os.name == 'nt' else 'clear')

def initialize_terminals():
    """
    Initializes the terminal screen with the default number displays and terminal borders.
    """
    print(get_graphics()['terminals'])
    for i in range(4):
        update_quadrant(i+1, data=None)
    set_cursor(0,INPUTLINE)

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

def calibrate_print_commands():
    """
    Print commands, used in calibration screen.\n
    """
    commandsinfo = get_graphics().get('commands').split("\n")
    for i in range(len(commandsinfo)):
        for j in range(len(commandsinfo[i])):
            print(f"\033[{34+i};79H" + commandsinfo[i][:j], end="")

def calibrate_screen(type: str) -> None:
    terminal_size = shutil.get_terminal_size()
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
        calibrate_print_commands()
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
                calibrate_print_commands()
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