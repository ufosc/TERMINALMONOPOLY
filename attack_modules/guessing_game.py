import random
from time import sleep
from utils.utils import MYCOLORS as c # graphics is g

game_title = "Guessing Game"
header = "─" * ((75 - len(game_title)) // 2) + game_title + "─" * ((75 - len(game_title)) // 2)

from utils import utils as ss
from utils.utils import Terminal
from utils.utils import MYCOLORS as COLORS, g
#def render_hand(active_terminal: Terminal, attacker_picked_hand, outcome):
 #   if outcome == "WIN":
        #open hand with trick
  #  elif outcome == "LOSE":
        #open correct hand with trick and incorrect hand without trick
   # else:
        #both closed
    #active_terminal.update(header + f"\n\n{left_hand_str}" + '\n' * 5 + f"{right_hand_str}")
def guessing_game(active_terminal: Terminal,attacker_picked_hand):
    defender_picked_hand = ""
    is_valid = False
    while not is_valid:
        defender_picked_hand = "l";
        is_valid = defender_picked_hand.lower() == "l" or defender_picked_hand.lower() == "r";
        if attacker_picked_hand.upper() == defender_picked_hand.upper():
            input(c.backYELLOW + c.BLACK + f"\rYou picked the right hand! No Penalty!")
            return "WIN"
        elif is_valid:
            input(c.backYELLOW + c.BLACK + f"\rYou picked the wrong hand! Penalty!")
            return "LOSE"
        else:
            print("Invalid input! Try again!")


def play(active_terminal: Terminal, bet) -> int:
    """
    Guessing game
    2 hands
    1 with trick 1 w/o
    defender has to pick one with trick to be penalty free
    """
    score = [0, 0, 0, 0]
    active_terminal.update(header + "\n" + g['coin_flip_heads'])
    flip = random.choice(['l', 'r'])
    #ss.overwrite(COLORS.RED + flip)
    choice = ""
    choice = input(c.backYELLOW + c.BLACK + f"\rYou have been attacked! Left or Right? (L/R) ")
    while (not (choice.lower() == "r" or choice.lower() == "l")):
        ss.overwrite(COLORS.RED + "Invalid Choice!")
        choice = input(c.backYELLOW + c.BLACK + f"\rYou have been attacked! Left or Right? (L/R) ")
        ss.overwrite("\r" + " " * 40)

    # TODO - Make the animation asynchrnous.
    active_terminal.update(header + "\n" + g['coin_flip_heads'])
    sleep(0.2)
    active_terminal.update(header + "\n" + g['coin_flip_middle'])
    sleep(0.2)
    active_terminal.update(header + "\n" + g['coin_flip_tails'])
    sleep(0.2)
    active_terminal.update(header + "\n" + g['coin_flip_middle'])
    sleep(0.2)
    active_terminal.update(header + "\n" + g['coin_flip_heads' if flip == 'heads' else 'coin_flip_tails'])
    if (choice.lower() == flip):
        ss.overwrite(c.backYELLOW + c.BLACK + f"\rYou got the right hand! You avoided the penalty!")
        ss.overwrite("\r" + " " * 40)
        score[0] += 1
    else:
        ss.overwrite(c.backYELLOW + c.BLACK + f"\rYou got the wrong hand...")
        ss.overwrite("\r" + " " * 40)
        score[0] = 0


    if (score[0] == 1):
        active_terminal.update(header + "\n" + g['casino_win'])
        bet = 0
    else:
        active_terminal.update(header + "\n" + g['casino_lose'])
        bet *= 1
    #input("\r")
    ss.overwrite("\r" + " " * 40)
    return bet

