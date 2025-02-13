# SLOTS MACHINE
import random
from time import sleep
from style import graphics as g
import screenspace as ss
from screenspace import Terminal

game_title = "♕ Slots Machine"
header = "─" * ((75 - len(game_title)) // 2) + game_title + "─" * ((75 - len(game_title)) // 2)
loss_header = "─" * ((75 - len("Try Again!")) // 2) + "Try Again!" + "─" * ((75 - len("Try Again!")) // 2)
win_header = "WIN!!! " * (75 // len("WIN!!! ")) + "WIN!!!"[:75 % len("WIN!!! ")]

# 1. Create a list of symbols
slot_graphics = {name: g.get(name) for name in g.keys() if name.startswith("slots")}
slot_graphics.pop("slots_frame_up")
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

def play(bet: int) -> int:
    """
    Slots Module
    Author: Adam Gulde
    Version: 1.0
    Play the slots!
    """

    ss.set_cursor(0, 0)
    print(header)

    # 3. Display the slots
    print(up)
    for t in range(41): 
        ss.set_cursor(0, 0)
        sleep_time = exponential_increase(t)
        rotate_machine() if t % 2 == 0 else None
        print_frame_up_fast() if t % 2 == 0 else print_frame_down_fast()
        print_slots(t % 2 == 0)
        print()
        sleep(sleep_time)

    # 4. Check for matches
    bonus = check_bonus(bet)
    winnings = check_win(bet) + bonus[0]
    if winnings > 0:
        ss.set_cursor(0, 1)
        print(win_header,end="")
        ss.set_cursor(0, 15)
        print(g.get("slots_frame_win"))
        print_results(bet, bonus[1], winnings)
    else:
        ss.set_cursor(0, 1)
        print(loss_header,end="")
    return winnings

def print_results(bet: int, bonus: str, winnings: int) -> None:
    """
    Prints the winnings in a nice format.
    """
    ss.set_cursor(25, 17) # Bet
    print(bet)
    ss.set_cursor(43, 17) # Bonus 
    print(bonus)
    ss.set_cursor(28, 18) # Payout
    print(winnings)


def print_number_list():
    for i in range(22):
        ss.set_cursor(80, i)
    print(i)

def exponential_increase(t):
    """
    Exponential increase function, used for sleep time aka the spinning speed of the slots.
    """
    return 0.01 * (1.1 ** t)

def rotate_machine():
    """
    Rotate the entire slot machine. Allows for new symbols to be displayed.
    """
    wheel0.append(wheel0.pop(0))
    wheel1.append(wheel1.pop(0))
    wheel2.append(wheel2.pop(0))

    # Update the machine with the new wheels
    machine[0] = [wheel0[0], wheel0[1], wheel0[2]]
    machine[1] = [wheel1[0], wheel1[1], wheel1[2]]
    machine[2] = [wheel2[0], wheel2[1], wheel2[2]]

    return machine

def halve_image(image, top_half=True):
    """
    Halve an image by removing the top or bottom half
    """
    half_image = len(image) // 2
    return image[half_image:] if top_half else image[:half_image]

def print_slots(up=True):
    """
    Print the slot machine's symbols in a 3x3 grid format, each symbol in a 23x8 box.
    Not my greatest work... 
    """

    box_width = 23
    box_height = 8

    inc_x = 0
    inc_y = 0
    
    if up: # Print 1/2 top slots, middle slots, and 1/2 bottom slots
        top_left = halve_image(machine[0][0], True)
        for line in top_left:
            x_offset = 1
            ss.set_cursor(x_offset + inc_x, inc_y + 1)
            if "\n" in line:
                inc_y += 1
                inc_x = 0
            print(line, end="")
            inc_x += 1
        
        inc_x = 0
        inc_y = 0
        top_middle = halve_image(machine[1][0], True)
        for line in top_middle:
            x_offset = box_width + 2
            ss.set_cursor(x_offset + inc_x, inc_y + 1)
            if line == "\n":
                inc_y += 1
                inc_x = 0
            print(line, end="")
            inc_x += 1

        inc_x = 0
        inc_y = 0
        top_right = halve_image(machine[2][0], True)
        for line in top_right:

            x_offset = box_width*2 + 4

            ss.set_cursor(x_offset + inc_x, inc_y + 1)
            print(line, end="")
            inc_x += 1
            if line == "\n":
                inc_y += 1
                inc_x = 0

        inc_x = 0
        inc_y = 0
        middle_left = machine[0][1]
        for line in middle_left:
            y_offset = box_height - 1
            ss.set_cursor(inc_x + 2, y_offset + inc_y)
            print(line, end="")
            inc_x += 1
            if "\n" in line:
                inc_y += 1
                inc_x = 0

        inc_x = 0
        inc_y = 0
        middle_middle = machine[1][1]
        for line in middle_middle:
            x_offset = box_width + 3
            y_offset = box_height - 1
            ss.set_cursor(x_offset + inc_x, y_offset + inc_y)
            print(line, end="")
            inc_x += 1
            if line == "\n":
                inc_y += 1
                inc_x = 0

        inc_x = 0
        inc_y = 0
        middle_right = machine[2][1]
        for line in middle_right:
            x_offset = box_width * 2 + 4
            y_offset = box_height - 1
            ss.set_cursor(x_offset + inc_x, y_offset + inc_y)
            print(line, end="")
            inc_x += 1
            if line == "\n":
                inc_y += 1
                inc_x = 0

        inc_x = 0
        inc_y = 0
        bottom_left = halve_image(machine[0][2], False)
        for line in bottom_left:
            x_offset = 2
            y_offset = box_height * 2 + 1
            ss.set_cursor(x_offset + inc_x, y_offset + inc_y)
            print(line, end="")
            inc_x += 1
            if line == "\n":
                inc_y += 1
                inc_x = 0

        inc_x = 0
        inc_y = 0
        bottom_middle = halve_image(machine[1][2], False)
        for line in bottom_middle:
            x_offset = box_width * 1 + 3
            y_offset = box_height * 2 + 1
            ss.set_cursor(x_offset + inc_x,  y_offset + inc_y)
            print(line, end="")
            inc_x += 1
            if line == "\n":
                inc_y += 1
                inc_x = 0

        inc_x = 0
        inc_y = 0
        bottom_right = halve_image(machine[2][2], False)
        for line in bottom_right:
            x_offset = box_width * 2 + 4
            y_offset = box_height * 2 + 1
            ss.set_cursor(x_offset + inc_x, y_offset + inc_y)
            print(line, end="")
            inc_x += 1
            if line == "\n":
                inc_y += 1
                inc_x = 0
    if not up:
        inc_x = 0
        inc_y = 0
        middle_left = machine[0][1]
        for line in middle_left:
            y_offset = 2
            ss.set_cursor(inc_x + 2, y_offset + inc_y)
            print(line, end="")
            inc_x += 1
            if "\n" in line:
                inc_y += 1
                inc_x = 0

        inc_x = 0
        inc_y = 0
        middle_middle = machine[1][1]
        for line in middle_middle:
            x_offset = box_width + 3
            y_offset = 2
            ss.set_cursor(x_offset + inc_x, y_offset + inc_y)
            print(line, end="")
            inc_x += 1
            if line == "\n":
                inc_y += 1
                inc_x = 0

        inc_x = 0
        inc_y = 0
        middle_right = machine[2][1]
        for line in middle_right:
            x_offset = box_width * 2 + 4
            y_offset = 2
            ss.set_cursor(x_offset + inc_x, y_offset + inc_y)
            print(line, end="")
            inc_x += 1
            if line == "\n":
                inc_y += 1
                inc_x = 0
        inc_x = 0
        inc_y = 0

        bottom_left = machine[0][2]
        for line in bottom_left:
            x_offset = 2
            y_offset = box_height + 4
            ss.set_cursor(x_offset + inc_x, y_offset + inc_y)
            print(line, end="")
            inc_x += 1
            if line == "\n":
                inc_y += 1
                inc_x = 0

        inc_x = 0
        inc_y = 0
        bottom_middle = machine[1][2]
        for line in bottom_middle:
            x_offset = box_width * 1 + 3
            y_offset = box_height + 4
            ss.set_cursor(x_offset + inc_x,  y_offset + inc_y)
            print(line, end="")
            inc_x += 1
            if line == "\n":
                inc_y += 1
                inc_x = 0

        inc_x = 0
        inc_y = 0
        bottom_right = machine[2][2]
        for line in bottom_right:
            x_offset = box_width * 2 + 4
            y_offset = box_height + 4
            ss.set_cursor(x_offset + inc_x, y_offset + inc_y)
            print(line, end="")
            inc_x += 1
            if line == "\n":
                inc_y += 1
                inc_x = 0

def print_frame_up_fast():
    """
    Print the frame in the up position.
    Works faster than simply printing the frame, because not all spaces need to be replaced. 
    """
    ss.set_cursor(0, 2)
    # print("│                       │                       │                       │")
    print("│                       │                       │                       │")
    ss.set_cursor(0, 6)
    print("└───────────────────────┴───────────────────────┴───────────────────────┘")
    print("┌───────────────────────┬───────────────────────┬───────────────────────┐")
    ss.set_cursor(0, 11)
    print("│                       │                       │                       │")
    print("│                       │                       │                       │")
    ss.set_cursor(0, 16)
    print("└───────────────────────┴───────────────────────┴───────────────────────┘")
    print("┌───────────────────────┬───────────────────────┬───────────────────────┐")
    ss.set_cursor(0, 21)
    print("│                       │                       │                       │")

def print_frame_down_fast():
    """
    Print the frame in the down position.
    Works faster than simply printing the frame, because not all spaces need to be replaced.
    """
    ss.set_cursor(0, 2)
    print("┌───────────────────────┬───────────────────────┬───────────────────────┐")
    ss.set_cursor(0, 6)
    print("│                       │                       │                       │")
    print("│                       │                       │                       │")
    print("│                       │                       │                       │")
    ss.set_cursor(0, 11)
    print("└───────────────────────┴───────────────────────┴───────────────────────┘")
    print("┌───────────────────────┬───────────────────────┬───────────────────────┐")
    ss.set_cursor(0, 16)
    print("│                       │                       │                       │")
    print("│                       │                       │                       │")
    print("│                       │                       │                       │")
    ss.set_cursor(0, 21)
    print("└───────────────────────┴───────────────────────┴───────────────────────┘")
    print("                                                                         ")

def check_win(bet: int) -> int:
    """
    Check for matches in the slot machine.
    """
    profit = 0

    # Check for matches in the first row
    if machine[0][0] == machine[0][1] == machine[0][2]:
        profit += bet * 5
        draw_win_line(coordinates[0][0], coordinates[0][2])
    # Check for matches in the second row
    # if machine[1][0] == machine[1][1] == machine[1][2]:
        # profit += bet * 3
        # draw_win_line(coordinates[1][0], coordinates[1][2])
    # Check for matches in the third row
    if machine[2][0] == machine[2][1] == machine[2][2]:
        profit += bet * 5
        draw_win_line(coordinates[2][0], coordinates[2][2])
    # Check for matches in the first column
    if machine[0][0] == machine[1][0] == machine[2][0]:
        profit += bet * 5
        draw_win_line(coordinates[0][0], coordinates[2][0])
    # Check for matches in the second column
    if machine[0][1] == machine[1][1] == machine[2][1]:
        profit += bet * 5
        draw_win_line(coordinates[0][1], coordinates[2][1])
    # Check for matches in the third column
    if machine[0][2] == machine[1][2] == machine[2][2]:
        profit += bet * 5
        draw_win_line(coordinates[0][2], coordinates[2][2])
    # Check for matches in the diagonal from top left to bottom right
    if machine[0][0] == machine[1][1] == machine[2][2]:
        profit += bet * 5
        draw_win_line(coordinates[0][0], coordinates[2][2])
    # Check for matches in the diagonal from top right to bottom left
    if machine[0][2] == machine[1][1] == machine[2][0]:
        profit += bet * 5
        draw_win_line(coordinates[0][2], coordinates[2][0])
    return profit

def check_bonus(bet) -> list[int, str]:
    """
    Check for matches in the bonus (middle) line.

    Returns a list of the profit and the bonus symbol with its respective bonus multiplier.
    """
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
        draw_win_line(coordinates[winning_indices[0]][1], coordinates[winning_indices[1]][1])

        if machine[0][1] == machine[1][1] and machine[1][1] == machine[2][1]:
            profit += bet * 10 # Getting a 3 in a row on the bonus line pays out 10x
            multiplier = "3 IN A ROW on bonus line! 10x"
            return [profit, multiplier]
 
    return [profit, multiplier]


def draw_win_line(start: tuple, end: tuple):
    """
    Draw a line from the first symbol to the second symbol.
    """
    points = bresenham(start[0], start[1], end[0], end[1])
    for point in points:
        x, y = point
        ss.set_cursor(x, y)
        print("▓", end="")

def bresenham(x1, y1, x2, y2):
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
    play(100)
    ss.set_cursor(0, 25)
