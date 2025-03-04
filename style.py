## Custom theme colors, could be adjusted with more RGB values for more creative themes!
## Use these in place of colorama's Fore and Back color literals.
## Should add a "compatible" color set for terminals that cannot play nice with RGB values.
## [https://en.wikipedia.org/wiki/ANSI_escape_code] for more info on ANSI escape codes.
import os

# class for compatible colors for terminals that cannot utilize RGB values outside of the 8-bit ANSI colors
class COMPAT_COLORS:
    cBROWN = "\033[38;5;94m"
    cLIGHTBLUE = "\033[38;5;33m"
    cROUGE = "\033[38;5;13m"
    cORANGE = "\033[38;5;208m"
    
    # https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit 
    # Uses Standard colors (0-7) and High-Intensity colors (8-15) from 8-bit ANSI escape codes 
    cRED = "\033[38;5;1m"
    cGREEN = "\033[38;5;10m"
    cYELLOW = "\033[38;5;11m"
    cBLUE = "\033[38;5;4m"
    cCYAN = "\033[38;5;14m"
    cWHITE = "\033[38;5;15m"
    cLIGHTGRAY = "\033[38;5;247m"
    cLIGHTBLACK = "\033[38;5;8m"
    cCHANCE = "\033[38;5;214m"
    cCOMMUNITY = "\033[38;5;45m"
    cBLACK = "\033[38;5;0m"

    # Reset color[
    RESET = "\033[0m"
    # Player colors: red, green, yellow, blue, respectively
    playerColors = ["\033[38;5;1m", "\033[38;5;2m", "\033[38;5;3m", "\033[38;5;4m"]
    # display colors are used for printing text in Terminal, like error messages, etc. Not to be used on gameboard.
    dispGREEN = "\033[38;5;2m"
    dispRED = "\033[38;5;9m"
    dispBLUE = "\033[38;5;12m"

    backCompatBROWN = cBROWN.replace("38", "48")
    backCompatLIGHTBLUE = cLIGHTBLUE.replace("38", "48")
    backCompatROUGE = cROUGE.replace("38", "48")
    backCompatORANGE = cORANGE.replace("38", "48")
    backCompatRED = cRED.replace("38", "48")
    backCompatYELLOW = cYELLOW.replace("38", "48")
    backCompatGREEN = cGREEN.replace("38", "48")
    backCompatBLUE = cBLUE.replace("38", "48")
    backCompatWHITE = cWHITE.replace("38", "48")
    backCompatCYAN = cCYAN.replace("38", "48")
    backCompatLIGHTGRAY = cLIGHTGRAY.replace("38", "48")
    backCompatLIGHTBLACK = cLIGHTBLACK.replace("38", "48")
    backCompatCHANCE = cCHANCE.replace("38", "48")
    backCompatCOMMUNITY = cCOMMUNITY.replace("38", "48")
    backCompatBLACK = cBLACK.replace("38", "48")

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
    
    # TODO add default compatible colors for terminals that cannot handle RGB values (see issue #11). 
    cBROWN = ""
    cbBROWN = ""

def colortest():
    """
    Prints a test of all colors defined in the COLORS class.
    """
    # print("Testing foreground colors:")
    # for color in dir(COMPAT_COLORS):
    #     if not color.startswith('__') and not color.startswith('back') and color != "RESET":
    #         value = getattr(COMPAT_COLORS, color)
    #         if isinstance(value, list):  # Skip lists to avoid TypeError
    #             continue
    #         print(value + f"{color}" + COMPAT_COLORS.RESET)

    # print("\nTesting background colors:")
    # for color in dir(COMPAT_COLORS):
    #     if color.startswith('back'):
    #         value = getattr(COMPAT_COLORS, color)
    #         if isinstance(value, list):  # Skip lists to avoid TypeError
    #             continue
    #         print(value + f"{color}" + COMPAT_COLORS.RESET)
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

# if __name__ == "__main__":
#     colortest()