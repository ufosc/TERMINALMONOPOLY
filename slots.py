# SLOTS MACHINE
import random
from time import sleep
from style import graphics as g
import screenspace as ss
from screenspace import Terminal

game_title = "♕ Slots Machine"
header = "─" * ((75 - len(game_title)) // 2) + game_title + "─" * ((75 - len(game_title)) // 2)

def play(bet: int):
    """
    Slots Module
    Author: Adam Gulde
    Version: 1.0
    Play the slots!
    """
    
    # 1. Create a list of symbols
    slot_graphics = {name: g.get(name) for name in g.keys() if name.startswith("slots")}
    slot_graphics.pop("slots_frame_up")
    slot_graphics.pop("slots_frame_down")
    
    # Correspond each symbol in symbols with a graphic from slot_graphics
    symbols = list(slot_graphics.values())
    # OK I KNOW this is inefficient. The correct way to do this is to keep the actual graphics 
    # in a dictionary and use the keys to access them. For now, we will directly swap the graphics
    # in the positions list.

    # 2. Generate three random symbols
    wheel0 = symbols.copy()
    random.shuffle(wheel0)
    wheel1 = symbols.copy()
    random.shuffle(wheel1)
    wheel2 = symbols.copy()
    random.shuffle(wheel2)

    # machine = [
    #     [wheel0[0], wheel1[0], wheel2[0]],
    #     [wheel0[1], wheel1[1], wheel2[1]],
    #     [wheel0[2], wheel1[2], wheel2[2]]
    # ]

    machine = [[slot_graphics['slots_test'] for _ in range(3)] for _ in range(3)]

    # 3. Display the slots
    ss.set_cursor(0, 0)
    # ss.clear_screen()
    print(header)
    
    up = g.get("slots_frame_up")
    down = g.get("slots_frame_down")

    def exponential_increase(t): # used for sleep time
        return 0.1 * (1.1 ** t)

    def rotate_column(col: int):
        """
        Rotate a column of the slot machine
        """
        # Rotate the column by removing the first element and appending it to the end
        machine[col].append(machine[col].pop(0))

        return machine
    
    def rotate_machine():
        """
        Rotate the entire slot machine
        """
        for i in range(3):
            rotate_column(i)
        return machine

    def print_slots():
        """
        Print the slot machine's symbols in a 3x3 grid format, each symbol in a 23x8 box.
        """

        print(up) # if n % 2 == 0 else print(down)

        box_width = 23
        box_height = 8

        inc_x = 0
        inc_y = 4
        
        for line in machine[0][0][23*8-2*box_height:box_height*box_width]:
            ss.set_cursor(inc_x + 2, inc_y)
            if "\n" in line:
                line.replace("\n", "")
                inc_y += 1
                inc_x = 0
            print(line, end="")
            inc_x += 1
        
        inc_x = 0
        inc_y = 0
        for line in machine[1][0]:
            x_offset = box_width + 3
            print(line, end="")
            ss.set_cursor(x_offset + inc_x, inc_y)
            inc_x += 1
            if line == "\n":
                inc_y += 1
                inc_x = 0

        inc_x = 0
        inc_y = 0
        for line in machine[2][0]:

            x_offset = box_width*2 + 4

            ss.set_cursor(x_offset + inc_x, inc_y)
            print(line, end="")
            inc_x += 1
            if line == "\n":
                inc_y += 1
                inc_x = 0

        inc_x = 0
        inc_y = 0
        for line in machine[0][1]:
            ss.set_cursor(inc_x + 2, inc_y + box_height)
            print(line)
            inc_x += 1
            if "\n" in line:
                inc_y += 1
                inc_x = 0

        inc_x = 0
        inc_y = 0
        for line in machine[1][1]:

            x_offset = box_width + 3

            ss.set_cursor(x_offset + inc_x, inc_y + box_height)
            print(line, end="")
            inc_x += 1
            if line == "\n":
                inc_y += 1
                inc_x = 0

        inc_x = 0
        inc_y = 0
        for line in machine[2][1]:

            x_offset = box_width * 2 + 4

            ss.set_cursor(x_offset + inc_x, inc_y + box_height)
            print(line, end="")
            inc_x += 1
            if line == "\n":
                inc_y += 1
                inc_x = 0

        inc_x = 0
        inc_y = 0
        for line in machine[0][2]:

            x_offset = 2
            y_offset = box_height * 2 + 2

            ss.set_cursor(x_offset + inc_x, inc_y + y_offset)
            print(line, end="")
            inc_x += 1
            if line == "\n":
                inc_y += 1
                inc_x = 0

        inc_x = 0
        inc_y = 0
        for line in machine[1][2]:

            x_offset = box_width * 1 + 3
            y_offset = box_height * 2 + 2

            ss.set_cursor(x_offset + inc_x, inc_y + y_offset)
            print(line, end="")
            inc_x += 1
            if line == "\n":
                inc_y += 1
                inc_x = 0

        inc_x = 0
        inc_y = 0
        for line in machine[2][2]:

            x_offset = box_width * 2 + 4
            y_offset = box_height * 2 + 2

            ss.set_cursor(x_offset + inc_x, inc_y + y_offset)
            print(line, end="")
            inc_x += 1
            if line == "\n":
                inc_y += 1
                inc_x = 0

    for t in range(21):
        ss.set_cursor(0, 0)
        sleep_time = exponential_increase(t)
        print(up if t % 2 == 0 else down)
        rotate_machine()
        print_slots()
        sleep(sleep_time)

    # 4. Check for matches
    # if slot1 == slot2 == slot3:
    #     return bet * 10
    # elif slot1 == slot2 or slot1 == slot3 or slot2 == slot3:
    #     return bet * 5
    # else:
    #     return -bet        

if __name__ == "__main__":
    play(100)
