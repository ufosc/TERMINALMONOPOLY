## Custom theme colors, could be adjusted with more RGB values for more creative themes!
## Use these in place of colorama's Fore and Back color literals.
## Should add a "compatible" color set for terminals that cannot play nice with RGB values.
## [https://en.wikipedia.org/wiki/ANSI_escape_code] for more info on ANSI escape codes.
class COLORS:
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
    # Player colors: red, green, yellow, blue, respectively
    playerColors = ["\033[38;5;1m", "\033[38;5;2m", "\033[38;5;3m", "\033[38;5;4m"]
    # display colors are used for printing text in Terminal, like error messages, etc. Not to be used on gameboard.
    dispGREEN = "\033[38;5;2m"
    dispRED = "\033[38;5;9m"
    dispBLUE = "\033[38;5;12m"
    RESET = "\033[0m" # Reset color

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
    
    # @TODO add default compatible colors for terminals that cannot handle RGB values (see issue #11). 
    cBROWN = ""
    cbBROWN = ""

def colortest():
    """
    Prints a test of all colors defined in the COLORS class.
    """
    i = 0
    for color in dir(COLORS):
        if not color.startswith('__'):
            print(str(i) + ": " + getattr(COLORS, color) + color + COLORS.RESET)
            i += 1

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
    print(COLORS.dispGREEN+text, end=COLORS.RESET+end)

def center_lines(text, width):
        lines = text.split('\n')
        centered_lines = [line.center(width) for line in lines]
        return '\n'.join(centered_lines)

def get_graphics() -> dict:
    """
    Reads all graphics from ascii.txt into a dictionary.

    Parameters: None

    Returns: 
    Dictionary with the following keys:
    - 'help' A page of useful information to the player.
    - 'properties' List of properties in the game.
    - 'divider' ASCII graphic used throughout gameplay, i.e. printing deed information.
    - 'skull' ASCII graphic used on a killed terminal.
    - 'gameboard' The default gameboard. needs to be decoded  with 'unicode_escape' and 'utf-8' 
    - 'help 2' Displays additional information. 
    - 'logo' The game logo.
    - 'history and status' Information about the game history and status.
    """
    with open("ascii.txt", encoding='utf-8') as f:
        text = f.read().split("BREAK_TEXT")
    text_dict = {'help': text[0].rstrip(),
                 'properties': text[1],
                 'divider': text[2].lstrip(),
                 'skull': text[3].lstrip(),
                 'gameboard': bytes(text[4].lstrip(), 'utf-8').decode('unicode_escape').encode('latin-1').decode('utf-8'),
                 'help 2': center_lines(text[5], 75),
                 'logo': text[6],
                 'history and status': text[7],
                 'commands': text[8],
                 'chance cards text': text[9].strip(),
                 'community chest text': text[10].strip(),
                 'popup 1': text[11].strip(),
                 'terminals': text[12].strip(),
                 'fishing 1 idle': text[13].lstrip(),
                 'fishing 1 win': text[14].lstrip(),
                 'fishing 1 carp': text[15].replace('\n', ''),
                 'fishing 1 bass': text[16].replace('\n', ''),
                 'fishing 1 salmon': text[17].replace('\n', '')
                 } 
    return text_dict

def set_cursor(x: int, y: int) -> None:
    print(f"\033[{y};{x}H",end="")

def set_cursor_str(x:int ,y:int) -> str:
    return f"\033[{y};{x}H"