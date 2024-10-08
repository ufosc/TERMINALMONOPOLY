# monopoly notes
"""
turn based game, goal is to make money from other players while not going bankrupt
each turn player rolls 2 die, move around board clockwise
start on go (BR), 200 collected for passing
land on property, able to buy it if you can afford it
land on others' property, pay defined rent amount
rent can be increased by buying houses
utility/railroad: fixed rent, increases depending on other owned utility/railroad (seperate)
roll doubles, roll again, if 3 in a row go to jail tile, done collect money
jail: cant leave until you roll doubles or 3 turns
community chest/chance: given a card that may or may not benefit/move player
"""

# board info
"""
notes:
blue is comm chest
orange is chance
dark grey are railroads
SOMETHING are utilities
BR is go
BL is jail
TL is free parking
TR is go to jail
the color of the bottom right of a tile corresponds to player color
the  number of green voxels following that correspond to number of other util/railroads owned or number of houses
players represented by a colored tile with circle   '
"""

#notes for implementation
"""
- must be skipable
- possibly add additional argument for starting game without getting tutorial screen/question
- info section on different screens, enter to continue to next section screen
"""


import screenspace as ss
from style import COLORS
import style

cols = ss.WIDTH
rows = ss.HEIGHT
graphics = style.get_graphics()

skipped = False # set/used by print_tutorial_screen to determine whether to continue printing past 1st page

def print_tutorial_screen(cols:int, rows:int, title:str, obj_list:list[dict], border_color=COLORS.LIGHTGRAY) -> None:
    """
    Parameters:
    cols (int): number of columns in the terminal
    rows (int): number of rows in the terminal
    title (str): text to go inline with the screen border
    obj_list (list[dict]): a list of dictionary objects with all text to render to the screen
        "col" (int): x position of the object
        "row" (int): y position of the object
        "num_lines" (int): the number of rows that the object takes up
        "text" (str): the text to render to the screen 
    border_color (str): sets the color of the outer border of the screen. default is LightGray

    Renders a tutorial screen to the terminal with a title and a list of objects to render to the screen.
        Currently, custom coloring works only on the borders, support for the rest of e

    Returns:
    skipped (boolean) <- value used to determined whether to display following tutorial screens
    """
    option = ""
    
    screen_content = []

    title_padding = cols//2 - len(title)//2 - 1

    if (len(obj_list) > 0):
        pass
    
    #print top border with title
    screen_content.append(border_color +'╔' + ('═' * title_padding) + " " + title + " " + ('═' * (title_padding - (len(title)%2 == 1) * 1)) + '╗' + "   ")

    # split all text objects into a list of lines
    for obj in obj_list:
        temp = obj["text"].split("\n")
        obj["text"] = temp

    for y in range(1, rows):
        screen_content.append(border_color + "║ ")

        invisible_space = len(border_color)

        for obj in obj_list:
            if obj["row"] <= y and y <= obj["row"] + obj["num_lines"]:
                screen_content[y] += (" " * (obj["col"] + len(border_color) - len(screen_content[y])))
                screen_content[y] += COLORS.RESET + obj["text"][y - obj["row"]]
                invisible_space += len(COLORS.RESET)
                

        # fill in remaining empty space
        screen_content[y] += (" " * (cols + invisible_space - len(screen_content[y]))) + border_color + " ║"

    #print bottom border with title
    screen_content.append(border_color + '╚' + ('═' * title_padding) + " " + title + " " + ('═' * (title_padding - (len(title)%2 == 1) * 1)) + '╝' + "   ")

    print("\033[1A" * (rows + 4), end='\r') #reset cursor to top left
    for row in screen_content:
        print(row)

    # Checks if the current print is the first page, to determine whether to skip
    if title == "Terminal Monopoly":
        option = input(COLORS.LIGHTGRAY + "Would you like to skip the tutorial? (y/n)...")
    else:
        input(COLORS.LIGHTGRAY + "Press Enter to continue...")
    
    # Fills the rest of the terminal
    print(' ' * ss.WIDTH, end='\r')

    # Returns boolean to determine whether to skip (print rest of tutorial)
    if option == "y":
            return True
    else:
        return False


#prints all the tutorial screens, if the player hasnt skipped it
skipped = print_tutorial_screen(cols, rows, "Terminal Monopoly", [
    {"col": 7, "row": 3, "num_lines": 0, "text":"Welcome to:"},
    {"col": 10, "row": 6, "num_lines": 17, "text":graphics["logo"]},
    {"col": 15, "row": 27, "num_lines": 0, "text":"The Last Game You'll Ever Play..."}
], COLORS.CYAN)

if not skipped:
    print_tutorial_screen(cols, rows, "Page 1", [
        #all of the text is currently copilot nonsense to show that it works
        {"col": 3, "row": 2, "num_lines": 0, "text":"Firstly, what the hell is a Monopoly?"},
        {"col": 5, "row": 5, "num_lines": 0, "text":"Terminal Monopoly is a text-based version of the classic board game Monopoly."},
        {"col": 5, "row": 7, "num_lines": 0, "text":"The goal of the game is to make money from other players while avoiding bankruptcy."},
        {"col": 5, "row": 9, "num_lines": 0, "text":"Each turn, players roll two dice and move around the board."},
        {"col": 5, "row": 11, "num_lines": 0, "text":"Players start on the 'Go' tile and collect $200 for passing."},
    ])

    print_tutorial_screen(cols, rows, "Page 2", [

    ])


