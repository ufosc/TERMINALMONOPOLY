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

def print_tutorial_screen(cols, rows, title, obj_list) -> None:
    """
    Parameters:
    cols (int): number of columns in the terminal
    rows (int): number of rows in the terminal
    title (str): text to go inline with the screen border
    obj_list (list[dict]): a list of dictionary objects with all text to render to the screen
        "x" (int): x position of the object
        "y" (int): y position of the object
        "num_lines" (int): the number of rows that the object takes up
        "text" (str): the text to render to the screen 

    Returns:
    None
    """
    if (len(obj_list) > 0):
        pass

    print("\033[1A" * (rows + 4), end='\r') #reset cursor to top left
    print(COLORS.LIGHTGRAY+'╔' + ('═' * (cols//2 - (len(title)//2) - 1)) + " " + title + " " + ('═' * (cols//2 - (len(title)//2) - 1 - (len(title)%2 == 1) * 1)) + '╗' + "   ")#super ugly ik

    screen_content = []
    for y in range(rows):
        screen_content.insert(y, "") #initializes index
        screen_content[y] = screen_content[y] + COLORS.LIGHTGRAY + '║'

        for obj in obj_list:
            if obj["y"] == y:
                data = obj["text"].split("\n")

                screen_content[y] = screen_content[y] + (" " * (obj["x"] - len(screen_content[y])))
                screen_content[y] = screen_content[y] + data[obj["y"] - y]

        screen_content[y] = screen_content[y] + (" " * (cols - len(screen_content[y])))

        screen_content[y] = screen_content[y] + '║'


    for y in range(rows):
        print(screen_content[y])

    print(COLORS.LIGHTGRAY+'╚' + ('═' * (cols//2 - (len(title)//2) - 1)) + " " + title + " " + ('═' * (cols//2 - (len(title)//2) - 1 - (len(title)%2 == 1) * 1)) + '╝' + "   ")

    input("Press Enter to continue...")


print_tutorial_screen(cols, rows, "Tutorial", [
    {"x": 10, "y": 1, "num_lines": 1, "text":"Welcome to:"},
    {"x": 1, "y": 2, "num_lines": 17, "text":graphics["logo"]}
])

# Fills the rest of the terminal
print(' ' * ss.WIDTH, end='\r')

