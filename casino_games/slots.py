# SLOTS MACHINE
import random
from time import sleep
from style import graphics as g
import screenspace as ss

game_title = "♕ Slots Machine"
header = game_title.center(75,"─")
mode = "terminal"


# 1. Create a list of symbols
slot_graphics = {name: g.get(name) for name in g.keys() if name.startswith("slots")}
slot_graphics.pop("slots_frame_up")
slot_graphics.pop("slots_frame_lose")
slot_graphics.pop("slots_frame_down")
slot_graphics.pop("slots_frame_win")

# Correspond each symbol in symbols with a graphic from slot_graphics
symbols = list(slot_graphics.values())
# The correct way to do this is to keep the actual graphics in a dictionary and use the 
# keys to access them. For now, we will directly swap the graphics in the positions list.

coordinates = [
    [(3, 2), (3, 12), (3, 20)],
    [(38, 2), (38, 12), (38, 20)],
    [(70, 2), (70, 12), (70, 20)]
]

# Get the frame graphics
up = g.get("slots_frame_up")
down = g.get("slots_frame_down")

# 2. Generate three random sets of the symbols
wheel0 = symbols.copy()
random.shuffle(wheel0)
wheel1 = symbols.copy()
random.shuffle(wheel1)
wheel2 = symbols.copy()
random.shuffle(wheel2)

machine = [
    [wheel0[0], wheel1[0], wheel2[0]],
    [wheel0[1], wheel1[1], wheel2[1]],
    [wheel0[2], wheel1[2], wheel2[2]]
]

def play(active_terminal: ss.Terminal, bet: int) -> int:
    """
    Slots Module
    Author: Adam Gulde
    Version: 1.3 - Integrated with player.py
    Play the slots!
    """
    if mode == "terminal":
        active_terminal.clear()
    ss.set_cursor(0, 0)

    # 3. Display the slots
    rng = random.randint(0, 3) # Randomly select a column to rotate
    for t in range(31): # Must be odd
        ss.set_cursor(0, 0)
        sleep_time = exponential_increase(t)

        rotate_column(0) if t % 2 == 0 else None
        rotate_column(1) if t % 2 == 1 else None
        rotate_column(2) if t % 2 == 0 else None
        if mode == "terminal":
            active_terminal.update(print_column(0, t % 2 == 0), padding=False)
            active_terminal.update(print_column(1, t % 2 == 1), padding=False)
            active_terminal.update(print_column(2, t % 2 == 1), padding=False)
        else: 
            print(print_column(0, t % 2 == 0), end="")
            print(print_column(1, t % 2 == 1), end="")
            print(print_column(2, t % 2 == 1), end="")
        sleep(sleep_time/3) 
        if rng != 3: # If not rotating all wheels, Rotate the wheels that was not selected to rotate
            rotate_column(rng) if t % 2 == 1 else None
            rotate_column((rng + 1) % 3) if t % 2 == 1 else None

            if mode == "terminal":
                active_terminal.update(print_column(rng, t % 2 == 1), padding=False)
                active_terminal.update(print_column((rng + 1) % 3, t % 2 == 1), padding=False)
            else:
                print(print_column(rng, t % 2 == 1), end="")
                print(print_column((rng + 1) % 3, t % 2 == 1), end="")

            sleep(sleep_time / 3)

            rotate_column(rng) if t % 2 == 0 else None
            if mode == "terminal":
                active_terminal.update(print_column(rng, t % 2 == 0), padding=False)
            else: 
                print(print_column(rng, t % 2 == 0), end="")

            sleep(sleep_time / 3)
        
    sleep(0.5) 
    if mode == "terminal":
        active_terminal.update(print_column(0, True), padding=False) # Print all the columns, to give a clicking into place effect
    else: 
        print(print_column(0, True), end="")
    rotate_column(1)
    if mode == "terminal":
        active_terminal.update(print_column(1, True), padding=False)
        active_terminal.update(print_column(2, True), padding=False)
    else:
        print(print_column(1, True), end="")
        print(print_column(2, True), end="")

    # 4. Check for matches
    sleep(1)
    bonus = check_bonus(bet)
    extrabonus, lines = check_win(bet)
    winnings = extrabonus + bonus[0]
    if mode == "terminal":
        # if bonus[2] != "":
        #     active_terminal.update(bonus[2], padding=False)
        if lines != "":
            active_terminal.update(lines, padding=False)
        ss.overwrite("Enter to continue...") 
        input() # Wait for the user to press enter
    ret_val = ""
    if winnings > 0:
        if mode == "terminal": 
            ret_val += g.get("slots_frame_win")
            ret_val = "\n" * 15 + print_results(bet, bonus[1], winnings, ret_val)
        else:
            ss.set_cursor(0, 20) 
            print(g.get("slots_frame_win"))
    else:
        if mode == "terminal": 
            ret_val += g.get("slots_frame_lose")
            ret_val = "\n" * 15 + print_results(bet, "No Bonus", winnings, ret_val)
        else:
            ss.set_cursor(0, 20)
            print(g.get("slots_frame_lose"), end="") # Print the loss frame
    
    if mode == "terminal":
        active_terminal.update(ret_val, padding=False)
        ss.overwrite("Enter to continue...") 
        input() # Wait for the user to press enter

    return winnings

def print_results(bet: int, bonus: str, winnings: int, ret_val: str = "") -> str:
    """
    Prints the winnings in a nice format.
    """
    if mode == "standalone":
        ss.set_cursor(25, 22) # Bet
        print(bet)
        ss.set_cursor(43, 22) # Bonus 
        print(bonus)
        ss.set_cursor(28, 23) # Payout
        print(winnings)
        return "" 
    else: 
        ret_val += ss.set_cursor_str(25, 17) + str(bet) # Bet
        ret_val += ss.set_cursor_str(43, 17) + bonus
        ret_val += ss.set_cursor_str(28, 18) + str(winnings)
        return ret_val

def exponential_increase(t):
    """
    Exponential increase function, used for sleep time aka the spinning speed of the slots.
    """
    return 0.01 * (1.1 ** t)

def rotate_column(column: int):
    """
    Rotate a column of the slot machine. Allows for new symbols to be displayed.
    """
    if column == 0:
        wheel0.append(wheel0.pop(0))
        machine[0][0] = wheel0[0]
        machine[0][1] = wheel0[1]
        machine[0][2] = wheel0[2]
    elif column == 1:
        wheel1.append(wheel1.pop(0))
        machine[1][0] = wheel1[0]
        machine[1][1] = wheel1[1]
        machine[1][2] = wheel1[2]
    elif column == 2:
        wheel2.append(wheel2.pop(0))
        machine[2][0] = wheel2[0]
        machine[2][1] = wheel2[1]
        machine[2][2] = wheel2[2]

def halve_image(image, top_half=True):
    """
    Halve an image by removing the top or bottom half

    top_half: If True, keep the top half. If False, keep the bottom half.
    """
    half_image = len(image) // 2
    return image[half_image:] if top_half else image[:half_image]

def print_square(symbol, is_half_image: bool, top: bool, x_offset:int, y_offset:int) -> str:
    ret_val = ""
    inc_x = 0
    inc_y = 0
    top_left = ""
    if is_half_image:
        top_left = halve_image(symbol, top)
        # Print a half frame around the symbol.
        if mode == "standalone": ss.set_cursor(x_offset, y_offset)
        else: ret_val += ss.set_cursor_str(x_offset, y_offset)
        # Ternary operator to determine the frame characters based on the if the symbol is located on the side, top, or bottom of the screen.
        if mode == "standalone": print((("┌" if x_offset < 10 else "┬") if x_offset < 40 else "┬") + "───────────────────────" + ("┐")) if not top else print()
        else: ret_val += (("┌" if x_offset < 10 else "┬") + "───────────────────────" + ("┬" if x_offset < 40 else "┐")) if not top else ""
        for i in range(1, 5):
            if mode == "standalone":
                ss.set_cursor(x_offset, y_offset + i)
                print("│")
                ss.set_cursor(x_offset + 24, y_offset + i)
                print("│")
            else:
                ret_val += ss.set_cursor_str(x_offset, y_offset + i)
                ret_val += "│"
                ret_val += ss.set_cursor_str(x_offset + 24, y_offset + i)
                ret_val += "│"
        if mode == "standalone": ss.set_cursor(x_offset, y_offset + 5)
        else: ret_val += ss.set_cursor_str(x_offset, y_offset + 5)
        if mode == "standalone": print(("└" if x_offset < 10 else "┴") + "───────────────────────" + ("┴" if x_offset < 40 else "┘") if top else ("┬" if x_offset < 10 else "┐")) if top else print()
        else: ret_val += (("└" if x_offset < 10 else "┴") + "───────────────────────" + ("┴" if x_offset < 40 else "┘")) if top else ""
    else:
        top_left = symbol

        # Print the full frame around the symbol.
        if mode == "standalone": 
            ss.set_cursor(x_offset, y_offset)
            print(("┌" if x_offset < 10 else "┬") + "───────────────────────" + ("┬" if x_offset < 40 else "┐"))
        else: 
            ret_val += ss.set_cursor_str(x_offset, y_offset)
            ret_val += (("┌" if x_offset < 10 else "┬") + "───────────────────────" + ("┬" if x_offset < 40 else "┐"))
        for i in range(1, 9):
            # For efficiency, only print the left and right sides of the frame.
            if mode == "standalone": 
                ss.set_cursor(x_offset, y_offset + i)
                print("│")
                ss.set_cursor(x_offset + 24, y_offset + i)
                print("│")
            else:
                ret_val += ss.set_cursor_str(x_offset, y_offset + i)
                ret_val += "│"
                ret_val += ss.set_cursor_str(x_offset + 24, y_offset + i)
                ret_val += "│"
        if mode == "standalone": ss.set_cursor(x_offset, y_offset + 9)
        else: ret_val += ss.set_cursor_str(x_offset, y_offset + 9)
        # 
        if mode == "standalone": print(("└" if x_offset < 10 else "┴") + "───────────────────────" + ("┴" if x_offset < 40 else "┘"))
        else: ret_val += (("└" if x_offset < 10 else "┴") + "───────────────────────" + ("┴" if x_offset < 40 else "┘"))
    
    # Print the symbol in the square
    for line in top_left:
        if mode == "standalone": ss.set_cursor(x_offset + inc_x, y_offset + inc_y)
        else: ret_val += ss.set_cursor_str(x_offset + inc_x, y_offset + inc_y)
        if "\n" in line:
            inc_y += 1
            inc_x = 0
        if mode == "standalone": print(line, end="")
        else: ret_val += line
        inc_x += 1
    
    # Return the string to be printed in the terminal.
    return ret_val

def print_column(row: int, up: bool) -> str:
    """
    Print a column of the slot machine.
    """
    ret_val = ""
    box_width = 23
    box_height = 8
    if up:
        if row == 0:
            ret_val += print_square(machine[0][0], True, True, 1, -1)
            ret_val += print_square(machine[0][1], False, False, 1, box_height - 3)
            ret_val += print_square(machine[0][2], True, False, 1, box_height * 2 - 1)
        elif row == 1:
            ret_val += print_square(machine[1][0], True, True, box_width + 2, -1)
            ret_val += print_square(machine[1][1], False, False, box_width + 2, box_height - 3)
            ret_val += print_square(machine[1][2], True, False, box_width + 2, box_height * 2 - 1)
        elif row == 2:
            ret_val += print_square(machine[2][0], True, True, box_width * 2 + 3, - 1)
            ret_val += print_square(machine[2][1], False, False, box_width * 2 + 3, box_height - 3)
            ret_val += print_square(machine[2][2], True, False, box_width * 2 + 3, box_height * 2 - 1)
    else:
        if row == 0:
            ret_val += print_square(machine[0][1], False, True, 1, 0)
            ret_val += print_square(machine[0][2], False, False, 1, box_height + 2)
        elif row == 1:
            ret_val += print_square(machine[1][1], False, True, box_width + 2, 0)
            ret_val += print_square(machine[1][2], False, False, box_width + 2, box_height + 2)
        elif row == 2:
            ret_val += print_square(machine[2][1], False, True, box_width * 2 + 3, 1)
            ret_val += print_square(machine[2][2], False, False, box_width * 2 + 3, box_height + 2)
    return ret_val

def check_win(bet: int, ret_val:str = "") -> tuple[int, str]:
    """
    Check for matches in the slot machine.
    """

    profit = 0

    # Check for matches in the first row
    if machine[0][0] == machine[1][0] == machine[2][0]:
        profit += bet * 5
        ret_val += draw_win_line(coordinates[0][0], coordinates[2][0])
    # Check for matches in the third row
    if machine[0][2] == machine[1][2] == machine[2][2]:
        profit += bet * 5
        ret_val += draw_win_line(coordinates[0][2], coordinates[2][2])
    # Check for matches in the diagonal from top left to bottom right
    if machine[0][0] == machine[1][1] == machine[2][2]:
        profit += bet * 5
        ret_val += draw_win_line(coordinates[0][0], coordinates[2][2])
    # Check for matches in the diagonal from top right to bottom left
    if machine[0][2] == machine[1][1] == machine[2][0]:
        profit += bet * 5
        ret_val += draw_win_line(coordinates[0][2], coordinates[2][0])

    return (profit, ret_val)

def check_bonus(bet) -> tuple[int, str, str]:

    """
    Check for matches in the bonus (middle) line.

    Returns a list of the profit and the bonus symbol with its respective bonus multiplier.
    """
    ret_val = ""
    profit = 0
    multiplier = ""
    if machine[0][1] == machine[1][1] or machine[1][1] == machine[2][1]:
        winning_indices = [0, 1, 2]
        if machine[0][1] == machine[1][1]:
            winning_indices.remove(2)
        elif machine[1][1] == machine[2][1]:
            winning_indices.remove(0)
        
        if ("        ┌┼┐        " in machine[1][1] or "/_  __/__ ______ _   " in machine[1][1] or "  ________ $ ______ __ " in machine[1][1] or "    .-~-.    .-~-.  "   in machine[1][1] or 
        "      ,d88b.d88b,      " in machine[1][1]):
            profit += bet * 2 # Dollar sign, Terminal Monopoly, Cash, Heart, Club pays out 2x 
            if "  ________ $ ______ __ " in machine[1][1]:
                multiplier = "Cash Bonus! 2x"
            if "/_  __/__ ______ _   " in machine[1][1]:
                multiplier = "Terminal Monopoly Bonus! 2x"
            elif "    .-~-.    .-~-.  " in machine[1][1]:
                multiplier = "Clubs! 2x"
            elif "      ,d88b.d88b,      " in machine[1][1]:
                multiplier = "Hearts! 2x"
            elif "        ┌┼┐        " in machine[1][1]:
                multiplier = "Cash! 2x"
        elif "┌┼┐  ┌┼┐  ┌┼┐" in machine[1][1]:
            profit += bet * 3 # Triple cash pays out 3x
            multiplier = "Triple Cash! 3x"
            # finish here 
        elif "█╔══██╗██╔══██╗██╔══██╗" in machine[1][1] or "       (^\/^\/^)       " in machine[1][1]:
            profit += bet * 4 # BAR, King pays out 4x
            if "█╔══██╗██╔══██╗██╔══██╗" in machine[1][1]:
                multiplier = "BAR! 4x"
            elif "       (^\/^\/^)       " in machine[1][1]:
                multiplier = "Kings! 4x"
        elif "    _ /_|_____|_\ _    " in machine[1][1]:
            profit += bet * 5 # Diamonds pays out 5x
            multiplier = "Diamonds! 5x"
        elif " ╚═══██║╚═══██║╚═══██║ " in machine[1][1]:
            profit += bet * 7 # Sevens pays out 7x
            multiplier = "Sevens! 7x"
        ret_val += draw_win_line(coordinates[winning_indices[0]][1], coordinates[winning_indices[1]][1])

        if machine[0][1] == machine[1][1] and machine[1][1] == machine[2][1]:
            profit += bet * 10 # Getting a 3 in a row on the bonus line pays out 10x
            multiplier = "3 IN A ROW on bonus line! 10x"
            return (profit, multiplier, ret_val)
 
    return (profit, multiplier, ret_val)

def print_number_sidebar():
    # For debugging purposes, print the numbers on the side of the screen.
    for i in range(0, 25):
        ss.set_cursor(77, i)
        print(i, end="")

def draw_win_line(start: tuple, end: tuple) -> str:
    """
    Draw a line from the first symbol to the second symbol.
    """
    ret_val = ""
    points = bresenham(start[0], start[1], end[0], end[1])
    for point in points:
        x, y = point
        if mode == "standalone": 
            ss.set_cursor(x, y) 
            print("▓", end="")
        else: 
            ret_val += ss.set_cursor_str(x, y)
            ret_val += "▓"
    
    return ret_val

def bresenham(x1, y1, x2, y2):
    """
    Function to calculate the points of a line using Bresenham's line algorithm.
    """
    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        points.append((x1, y1))
        if x1 == x2 and y1 == y2:
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

    return points

if __name__ == "__main__":
    print_number_sidebar()
    mode = "standalone"
    play(None, 100)
    ss.set_cursor(0, 25)
