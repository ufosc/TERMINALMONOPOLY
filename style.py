from colorama import Style, Fore

## Custom theme colors, could be adjusted with more RGB values for more creative themes!
## Use these in place of colorama's Fore and Back color literals.
## Should add a "compatible" color set for terminals that cannot play nice with RGB values.
COLORS = {"BROWN": "\033[38;2;138;96;25m",
          "LIGHTBLUE": "\033[38;2;43;249;255m",
          "ROUGE": "\033[38;2;240;93;231m",
          "ORANGE": "\033[38;2;246;160;62m",
          "RED": "\033[38;2;246;62;62m",
          "YELLOW": "\033[38;2;240;255;91m",
          "GREEN": "\033[38;2;41;129;32m",
          "BLUE": "\033[38;2;44;37;255m",
          "WHITE": "\033[38;2;255;255;255m",
          "CYAN": "\033[38;2;0;255;239m",
          "LIGHTGRAY": "\033[38;2;193;193;193m",
          "LIGHTBLACK": "\033[38;2;88;88;88m",
          "CHANCE": "\033[38;2;255;191;105m",
          "COMMUNITY": "\033[38;2;0;137;255m",
          "Player0": "\033[38;5;1m",
          "Player1": "\033[38;5;2m",
          "Player2": "\033[38;5;3m",
          "Player3": "\033[38;5;4m",}

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
    print(Fore.GREEN+text, end=Style.RESET_ALL+end)

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
    text_dict = {'help': text[0],
                 'properties': text[1],
                 # Use .strip() to remove whitespace if necessary
                 'divider': text[2].lstrip(),
                 'skull': text[3].lstrip(),
                 'gameboard': bytes(text[4].lstrip(), 'utf-8').decode('unicode_escape').encode('latin-1').decode('utf-8'),
                 'help 2': text[5],
                 'logo': text[6],
                 'history and status': text[7],
                 'commands': text[8],
                 'chance cards text': text[9].strip(),
                 'community chest text': text[10].strip(),
                 } 
    return text_dict