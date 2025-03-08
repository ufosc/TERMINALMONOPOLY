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

import os
import screenspace as ss
import style
from style import MYCOLORS as COLORS, graphics as g

cols = ss.WIDTH
rows = ss.HEIGHT

skipped = False # set/used by print_tutorial_screen to determine whether to continue printing past 1st page

def print_tutorial_screen(cols:int, rows:int, title:str, obj_list:list[dict], border_color=COLORS.LIGHTGRAY) -> bool:
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

    os.system('cls' if os.name == 'nt' else 'clear')
    
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
    {"col": 10, "row": 6, "num_lines": 17, "text":g.get("logo")},
    {"col": 15, "row": 27, "num_lines": 0, "text":"The Last Game You'll Ever Play..."}
])

if not skipped:
    print_tutorial_screen(cols, rows, "Page 1/4", [
        #all of the text is currently copilot nonsense to show that it works
        {"col": 3, "row": 2, "num_lines": 0, "text":"Firstly, what the hell is a Monopoly?"},
        {"col": 5, "row": 5, "num_lines": 0, "text":"• Monopoly is a classic board game where your goal is to make all of your friends go bankrupt!"},
        {"col": 5, "row": 7, "num_lines": 0, "text":"• Each turn, players roll dice to go around the board, landing on properties as they go."},
        {"col": 5, "row": 9, "num_lines": 0, "text":"• If you land on a property that is not owned by anybody, you can purchase it for yourself,"},
        {"col": 9, "row": 10, "num_lines": 0, "text":"otherwise, you pay the person who owns it a fixed amount determined by the property card."},
        {"col": 5, "row": 12, "num_lines": 0, "text":"• Properties are grouped into color sets. If you own all of the properties in a color set,"},
        {"col": 9, "row": 13, "num_lines": 0, "text":"you can build houses on the properties, which increases the amount players will need to pay."}
    ])

    print_tutorial_screen(cols, rows, "Page 2/4", [
        {"col": 3, "row": 2, "num_lines": 0, "text":"So, what makes Terminal Monopoly so special?"},
        {"col": 5, "row": 5, "num_lines": 0, "text":"• Terminal Monopoly is run entirely... in your terminal."},
        {"col": 5, "row": 7, "num_lines": 0, "text":"• The coolest part is that while you wait for you turn there are a variety of minigames to play,"},
        {"col": 9, "row": 8, "num_lines": 0, "text":"which can be opened and accessed by moving between four (4) modules."},
        {"col": 5, "row": 10, "num_lines": 0, "text":"• Some minigames require active attention, like Battleship, while others can run in the background, like Stocks."}
    ])

    print_tutorial_screen(cols, rows, "Page 3/4", [
        {"col": 3, "row": 2, "num_lines": 0, "text":"What the basics?"},
        {"col": 5, "row": 5, "num_lines": 0, "text":"• Every turn you will be prompted to roll the dice."},
        {"col": 5, "row": 7, "num_lines": 0, "text":'• When you land on an available property you can choose to purchase with "y" or "n".'},
        {"col": 5, "row": 9, "num_lines": 0, "text":"• After making an action you will promoted with three (3) options:"},
        {"col": 9, "row": 10, "num_lines": 0, "text":'• "e" to end your turn,'},
        {"col": 9, "row": 11, "num_lines": 0, "text":'• "p" to manage your owned properties,'},
        {"col": 9, "row": 12, "num_lines": 0, "text":'• "d" to view the deed of a property to dont own.'}
    ])

    print_tutorial_screen(cols, rows, "Page 4/4",[
        {"col": 3, "row": 2, "num_lines": 0, "text":"How do you interpret the board?"},
        {"col": 5, "row": 5, "num_lines": 0, "text":"• Each tile has number one (1) to thirty-nine (39)"},
        {"col": 5, "row": 7, "num_lines": 0, "text":'• Each property has a color at the top corresponding to its "monopoly".'},
        {"col": 5, "row": 9, "num_lines": 0, "text":"• Entirely blue tiles are Community Chest, and entirely orange tiles are Chance."},
        {"col": 5, "row": 11, "num_lines": 0, "text":"• The grey tiles are:"}, 
        {"col": 9, "row": 12, "num_lines": 0, "text":"• bottom right: GO,"},
        {"col": 9, "row": 13, "num_lines": 0, "text":"• bottom left: jail,"},
        {"col": 9, "row": 14, "num_lines": 0, "text":"• top right: go to jail,"},
        {"col": 9, "row": 15, "num_lines": 0, "text":"• top left: free parking,"},
        {"col": 9, "row": 16, "num_lines": 0, "text":"• all others: railroads and utilities."},
        {"col": 5, "row": 18, "num_lines": 0, "text":"• Player locations are represented by a small dot colored to correspond to the player."},
        {"col": 5, "row": 20, "num_lines": 0, "text":"• If a property is owned, the bottom left will be that player's color instead of grey."},
        {"col": 5, "row": 22, "num_lines": 0, "text":"• The number of houses owned by a player is represented by a number of green squares on the bottom of a tile."},   
    ])

