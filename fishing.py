import time
import random
from style import get_graphics, set_cursor, set_cursor_str

if __name__ == "__main__":
    import os
    os.system('cls')
    graphics = get_graphics()

    pictures = []

    fishies = graphics.copy()

    pictures.append(fishies.pop('fishing 1 idle'))
    pictures.append(fishies.pop('fishing 1 win'))

    print(pictures[0])

    start = int(time.time())
    delay = random.randint(5,25)
    catchtime = start + delay

    input('Press enter when you want to reel in the fish!')
    set_cursor(0,0)
    print(pictures[1])
    print()
    print()
    if catchtime - 7 < int(time.time()) < catchtime + 7:
        fish = random.choice(['carp', 'bass', 'salmon'])
        print('Nice job, you caught a ' + fish + '!')
        fish_graphic = fishies['fishing 1 ' + fish]
        set_cursor(37, 12)
        print(fish_graphic[0:3])
        set_cursor(37, 13)
        print(fish_graphic[3:6])
        set_cursor(37, 14)
        print(fish_graphic[6:9])
    else:    
        print('No luck!')
    set_cursor(0, 40)

