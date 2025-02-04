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
import sys
import keyboard
import time

# Each quadrant is half the width and height of the screen 
global rows, cols
rows = HEIGHT//2
cols = WIDTH//2

def notification(message: str, n: int, color: str) -> str:
    """
    Generates a notification popup message for the player.
    Parameters:
        message (str): The message to be displayed in the notification.
        n (int): The position identifier for the popup. 
                 1 - Top-left, 2 - Top-right, 3 - Bottom-left, 4 - Bottom-right, -1 - Custom position.
        color (str): The color code for the popup text.
    Returns:
        str: The formatted string with the notification message and its position.
    """
    message = message + " " * max(0, (78 - len(message)))
    # Max 78 character popup for messaging the player.
    x,y = -1,-1
    writeto = ""
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
    return writeto + set_cursor_str(0, INPUTLINE)

def replace_sequence(match, x, y):
    """
    Replaces the x and y coordinates in the matched string with the new x and y coordinates.
    Useful when updating the cursor position in a string, allowing for set_cursor_str() to 
    be used in any quadrant.
    """
    # Extract the number N from the matched string
    nx = int(match.group(2))
    ny = int(match.group(1))

    # Calculate the new x and y coordinates
    new_x = nx + x
    new_y = ny + y
    # Return the new sequence
    return f"\033[{new_y};{new_x}H"

def update_quadrant(n: int, data: str, padding: bool = True) -> None:
    """
    Better quadrant update function.
    This exceeds others because it immediately updates a single quadrant with the new data.
    Previously, the screen would not update until print_screen() was called.
    Furthermore, print_screen() would overwrite the entire screen, which is not ideal and slower.\n
    Set padding = True if you're not sure whether your module needs padding.
    
    Parameters: 
        n (int): Number (1-4) of the terminal to change data. 
        data (str): The string (with newlines to separate lines) to populate the quadrant with.
        padding (bool): (default True) a flag whether or not your module needs extra padding 
                (blank spaces) to fill in any missing lines
    Returns: 
        None
    """

    # If you're really desparate to add padding, for some edge case you can add it to the data string.
    if not padding:
        if 'PAD ME PLEASE!' in data:
            data = data.replace('PAD ME PLEASE!', '')
            padding = True

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

def indicate_keyboard_hook(t: int):
    """
    Indicates that the keyboard hook is active for a certain terminal. 
    Changes the color of the terminal border.
    This is important for the player to know why they can't type on the input line.
    """
    x,y = -1,-1
    border_chars = [('╔','╦','╠','╬'),
                    ('╦','╗','╬','╣'),
                    ('╠','╬','╚','╩'),
                    ('╬','╣','╩','╝')]
    
    match t: 
        case 1:
            x,y = 0,1
        case 2:
            x,y = cols+2, 1
        case 3:
            x,y = 0, rows+2
        case 4:
            x,y = cols+2, rows+2
    t = t - 1 # 0-indexed
    c = COLORS.LIGHTBLUE
    set_cursor(x,y)
    print(c, end='')
    print(border_chars[t][0] + '═' * cols + border_chars[t][1], end='')
    set_cursor(x,y+rows+1)
    print(border_chars[t][2] + '═' * cols + border_chars[t][3], end='')
    for i in range(y, y + rows):
        set_cursor(x, i+1)
        print('║')
        set_cursor(x+cols + (1 if (t + 1) % 2 == 0 else 2), i+1)
        print('║')

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

def get_valid_int(prompt, min_val = -1000000000, max_val = 1000000000, disallowed = [], allowed = []): # arbitrary large numbers
    """
    Prompts the user to enter an integer within a specified range and validates the input.
    Parameters:
        prompt (str): The message displayed to the user when asking for input.
        min_val (int, optional): The minimum acceptable value (inclusive). Defaults to -1000000000.
        max_val (int, optional): The maximum acceptable value (inclusive). Defaults to 1000000000.
        disallowed (list, optional): A list of disallowed values. Defaults to an empty list.
        allowed (list, optional): A list of allowed values. Defaults to an empty list. 
            If a space is in the whitelist, user is allowed to skip input (enter key), returning an empty string.
    Returns:
        int: A valid integer input by the user within the specified range. (or an empty string if allowed)
    Raises:
        None: All exceptions are caught and handled by the function.
    """
    while True:
        try:
            set_cursor(0, INPUTLINE)
            value = int(input(prompt))
            if value in allowed:
                return value
            if value < min_val or value > max_val or value in disallowed:
                raise ValueError
            return value
        except ValueError:
            try:
                value # check if value is defined. If not, the input was empty and the user pressed enter.
            except UnboundLocalError:
                if " " in allowed:
                    return "" # This is the signal to skip input
            overwrite("Invalid input. Please enter a valid integer.")
            set_cursor(0, INPUTLINE)

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
    clear_screen()
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

def auto_calibrate_screen() -> None:
    """
    Automatically calibrates the screen. The player doesn't really know what screen size is 
    optimal, but we do. This function will automatically adjust the screen size to the ensure 
    minimum requirements are met.
    """
    if os.name == 'nt': # Windows
        while os.get_terminal_size().lines - 5 < HEIGHT or os.get_terminal_size().columns - 5 < WIDTH:
            keyboard.press('ctrl')
            keyboard.send('-')
            keyboard.release('ctrl')
            time.sleep(0.1)

        while os.get_terminal_size().lines > HEIGHT + 40 or os.get_terminal_size().columns > WIDTH + 40:
            keyboard.press('ctrl')
            keyboard.send('+')
            keyboard.release('ctrl')
            time.sleep(0.1)
    elif os.name == 'posix': # Linux/macOS
        while shutil.get_terminal_size().lines < HEIGHT or shutil.get_terminal_size().columns < WIDTH:
            os.system("printf '\033[1;1t'")
            time.sleep(0.1)

        while shutil.get_terminal_size().lines > HEIGHT + 10 or shutil.get_terminal_size().columns > WIDTH + 10:
            os.system("printf '\033[1;1t'")
            time.sleep(0.1)

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

    # auto_calibrate_screen("player")