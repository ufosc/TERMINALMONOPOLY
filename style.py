## Custom theme colors, could be adjusted with more RGB values for more creative themes!
## Use these in place of colorama's Fore and Back color literals.
import os

# class for compatible colors for terminals that cannot utilize RGB values outside of the 8-bit ANSI colors
class COMPAT_COLORS:
    BROWN = "\033[38;5;94m"
    LIGHTBLUE = "\033[38;5;33m"
    ROUGE = "\033[38;5;13m"
    ORANGE = "\033[38;5;208m"
    
    # https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit 
    # Uses Standard colors (0-7) and High-Intensity colors (8-15) from 8-bit ANSI escape codes 
    RED = "\033[38;5;1m"
    YELLOW = "\033[38;5;11m"
    GREEN = "\033[38;5;10m"
    BLUE = "\033[38;5;4m"
    WHITE = "\033[38;5;15m"
    CYAN = "\033[38;5;14m"
    LIGHTGRAY = "\033[38;5;247m"
    LIGHTBLACK = "\033[38;5;8m"
    CHANCE = "\033[38;5;214m"
    COMMUNITY = "\033[38;5;45m"
    BLACK = "\033[38;5;0m"

    # Reset color
    RESET = "\033[0m"
    # Player colors: red, green, yellow, blue, respectively
    playerColors = ["\033[38;5;1m", "\033[38;5;2m", "\033[38;5;3m", "\033[38;5;4m"]
    # display colors are used for printing text in Terminal, like error messages, etc. Not to be used on gameboard.
    dispGREEN = "\033[38;5;2m"
    dispRED = "\033[38;5;9m"
    dispBLUE = "\033[38;5;12m"

    backBROWN = BROWN.replace("38", "48")
    backLIGHTBLUE = LIGHTBLUE.replace("38", "48")
    backROUGE = ROUGE.replace("38", "48")
    backORANGE = ORANGE.replace("38", "48")
    backRED = RED.replace("38", "48")
    backYELLOW = YELLOW.replace("38", "48")
    backGREEN = GREEN.replace("38", "48")
    backBLUE = BLUE.replace("38", "48")
    backWHITE = WHITE.replace("38", "48")
    backCYAN = CYAN.replace("38", "48")
    backLIGHTGRAY = LIGHTGRAY.replace("38", "48")
    backLIGHTBLACK = LIGHTBLACK.replace("38", "48")
    backCHANCE = CHANCE.replace("38", "48")
    backCOMMUNITY = COMMUNITY.replace("38", "48")
    backBLACK = BLACK.replace("38", "48")

class DEFAULT_COLORS:
    BROWN = "\033[38;2;138;96;25m"
    LIGHTBLUE = "\033[38;2;43;249;255m"
    ROUGE = "\033[38;2;240;93;231m"
    ORANGE = "\033[38;2;246;160;62m"
    RED = "\033[38;2;246;62;62m"
    YELLOW = "\033[38;2;240;255;91m"
    GREEN = "\033[38;2;41;129;32m"
    BLUE = "\033[38;2;44;37;255m"
    WHITE = "\033[38;2;255;255;255m"
    CYAN = "\033[38;2;0;255;239m"
    LIGHTGRAY = "\033[38;2;193;193;193m"
    LIGHTBLACK = "\033[38;2;88;88;88m"
    CHANCE = "\033[38;2;255;191;105m"
    COMMUNITY = "\033[38;2;0;137;255m"
    BLACK = "\033[38;5;0m"

    # Reset color
    RESET = "\033[0m"
    # Player colors: red, green, yellow, blue, respectively
    playerColors = ["\033[38;5;1m", "\033[38;5;2m", "\033[38;5;3m", "\033[38;5;4m"]
    # display colors are used for printing text in Terminal, like error messages, etc. Not to be used on gameboard.
    dispGREEN = "\033[38;5;2m"
    dispRED = "\033[38;5;9m"
    dispBLUE = "\033[38;5;12m"

    backBROWN = BROWN.replace("38", "48")
    backLIGHTBLUE = LIGHTBLUE.replace("38", "48")
    backROUGE = ROUGE.replace("38", "48")
    backORANGE = ORANGE.replace("38", "48")
    backRED = RED.replace("38", "48")
    backYELLOW = YELLOW.replace("38", "48")
    backGREEN = GREEN.replace("38", "48")
    backBLUE = BLUE.replace("38", "48")
    backWHITE = WHITE.replace("38", "48")
    backCYAN = CYAN.replace("38", "48")
    backLIGHTGRAY = LIGHTGRAY.replace("38", "48")
    backLIGHTBLACK = LIGHTBLACK.replace("38", "48")
    backCHANCE = CHANCE.replace("38", "48")
    backCOMMUNITY = COMMUNITY.replace("38", "48")
    backBLACK = BLACK.replace("38", "48")

class MYCOLORS:
    """
    This is the colorset a player chooses to use in the game.
    """
    BROWN = ""
    LIGHTBLUE = ""
    ROUGE = ""
    ORANGE = ""
    RED = ""
    YELLOW = ""
    GREEN = ""
    BLUE = ""
    WHITE = ""
    CYAN = ""
    LIGHTGRAY = ""
    LIGHTBLACK = ""
    CHANCE = ""
    COMMUNITY = ""
    BLACK = ""
    RESET = ""
    playerColors = ["", "", "", ""]
    dispGREEN = ""
    dispRED = ""
    dispBLUE = ""
    backBROWN = ""
    backLIGHTBLUE = ""
    backROUGE = ""
    backORANGE = ""
    backRED = ""
    backYELLOW = ""
    backGREEN = ""
    backBLUE = ""
    backWHITE = ""
    backCYAN = ""
    backLIGHTGRAY = ""
    backLIGHTBLACK = ""
    backCHANCE = ""
    backCOMMUNITY = ""
    backBLACK = ""

def choose_colorset(colorset: str) -> None:
    """
    This function sets the colorset for the game. It takes a string as an argument, which is the name of the colorset.
    It then sets the colorset to the chosen colorset, and sets the background colors to the chosen colorset.
    Parameters:
    colorset (str): The name of the colorset to be used.
    Returns:
    None
    """
    global MYCOLORS
    if colorset == "COMPAT_COLORS":
        # Set the colorset to the compatible colors
        for attr in dir(COMPAT_COLORS):
            if not attr.startswith('__'):
                setattr(MYCOLORS, attr, getattr(COMPAT_COLORS, attr))

    elif colorset == "DEFAULT_COLORS":
        # Set the colorset to the default defined colors
        for attr in dir(DEFAULT_COLORS):
            if not attr.startswith('__'):
                setattr(MYCOLORS, attr, getattr(DEFAULT_COLORS, attr))
    else:
        raise ValueError("Invalid colorset. Please choose either 'COMPAT_COLORS' or 'DEFAULT_COLORS'.")

def colortest():
    """
    Prints a test of all colors defined in the COLORS class.
    """
    print("\033[2J", end="")  # Clear the screen.. using escape sequence dont do this use screenspace clear_screen instead
    print(COMPAT_COLORS.WHITE, end="")  # Reset foreground to white for better visibility
    
    sets = [DEFAULT_COLORS, COMPAT_COLORS, MYCOLORS] # Add to this list to add more color sets to the test.
    
    for x in range(len(sets)):
        y = 0
        set_cursor(x*40, y+1)
        print(f"Testing color set {sets[x].__name__}:")
        set_cursor(x*40, y+2)
        print("Testing foreground colors:\n")
        for color in dir(sets[x]):
            if not color.startswith('__') and not color.startswith('back') and color != "RESET":
                value = getattr(sets[x], color)
                if isinstance(value, list):  # Skip lists to avoid TypeError
                    for item in value:
                        set_cursor(x*40, y+3)
                        print(item + f"{color}" + sets[x].RESET)
                        y += 1
                else: 
                    set_cursor(x*40, y+3)
                    print(value + f"{color}" + sets[x].RESET)
                    y += 1

        print(COMPAT_COLORS.WHITE, end="")  # Reset foreground to white for better visibility
        set_cursor(x*40, y+3)
        print("Testing background colors:")
        for color in dir(sets[x]):
            print(COMPAT_COLORS.WHITE, end="")  # Reset foreground to white for better visibility
            if color.startswith('back'):
                value = getattr(sets[x], color)
                set_cursor(x*40, y+4)
                print(value + f"{color}" + sets[x].RESET)
                y += 1

def print_w_dots(text: str, size: int=50, end: str='\n') -> None:
    """
    Prints a green string with predetermined dot padding after it.
    
    Parameters: 
    text (str): string to pad dots after. 
    size (int): integer of how long the padded string should be. Default 50.
    end (str): value to print immediately at the end of the text (after clearing color formatting). Default newline.

    Returns: 
    None
    """
    for i in range(size-len(text)):
        text += '.'
    print(DEFAULT_COLORS.dispGREEN+text, end=DEFAULT_COLORS.RESET+end)

def center_lines(text, width):
        lines = text.split('\n')
        centered_lines = [line.center(width) for line in lines]
        return '\n'.join(centered_lines)

def get_graphics() -> dict:
    """
    Reads all graphics from the ascii directory into a dictionary.

    Parameters: None

    Returns: 
    Dictionary with the key names of the graphics and the value of the graphic itself.
    The graphics are read from the ascii folder, where the key is the filename and the value is the graphic.
    """
    text_dict = {}
    for dir_name, sub_dirs, files in os.walk("./ascii/"):
        for file in files:
            with open(os.path.join(dir_name, file), encoding='utf-8') as ascii_text:
                full_file = ascii_text.read()
                split_file = full_file.splitlines(True)
                no_header_ascii = ''.join(split_file[1:])
                if (split_file[0].strip() == "GAMEBD"):
                    text_dict[file] = bytes(no_header_ascii, 'utf-8').decode('unicode_escape').encode('latin-1').decode('utf-8')
                elif (split_file[0].strip() == "CENTER"):
                    text_dict[file] = center_lines(no_header_ascii, 75)
                elif (split_file[0].strip() == "NWLCUT"):
                    text_dict[file] = no_header_ascii.replace('\n', '')
                elif (split_file[0].strip() == "NSTRIP"):
                    text_dict[file] = no_header_ascii.strip()
                elif (split_file[0].strip() == "LSTRIP"):
                    text_dict[file] = no_header_ascii.lstrip()
                elif (split_file[0].strip() == "RSTRIP"):
                    text_dict[file] = no_header_ascii.rstrip()
                else:
                    text_dict[file] = '\n' + full_file
    return text_dict

# Use this object to access all graphics, instead of calling get_graphics() every time.
graphics = get_graphics()

def set_cursor(x: int, y: int) -> None:
    print(f"\033[{y};{x}H",end="")

def set_cursor_str(x:int ,y:int) -> str:
    return f"\033[{y};{x}H"

if __name__ == "__main__":
    colortest()