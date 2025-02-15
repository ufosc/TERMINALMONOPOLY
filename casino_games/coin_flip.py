# COIN FLIP
import random
from time import sleep
import screenspace as ss
from style import get_graphics
from style import COLORS as c

game_title = "⛁ Coin Flip"
header = "─" * ((75 - len(game_title)) // 2) + game_title + "─" * ((75 - len(game_title)) // 2)

def play(active_terminal, bet, player_name):
    """
    Coin Flip

    Initializes a simple coin flip for casino.py
    A very simple base for a new casino_game
    Returns the wager to be sent to the player
    """
    score = [0,0,0,0]

    graphics = get_graphics()
    ss.update_quadrant(active_terminal, header + "\n" + graphics['coin_flip_heads'])
    
    choice = input(c.backYELLOW+c.BLACK+f"\rPlayer {player_name}: Heads or Tails? (h/T) ")
    ss.overwrite("\r" + " " * 40)
    flip = random.choice(['heads', 'tails'])
    
    #TODO - Make the animation asynchrnous.
    ss.update_quadrant(active_terminal,header + "\n" + graphics['coin_flip_heads'])
    sleep(0.2)
    ss.update_quadrant(active_terminal,header + "\n" + graphics['coin_flip_middle'])
    sleep(0.2)
    ss.update_quadrant(active_terminal,header + "\n" + graphics['coin_flip_tails'])
    sleep(0.2)
    ss.update_quadrant(active_terminal,header + "\n" + graphics['coin_flip_middle'])
    sleep(0.2)
    ss.update_quadrant(active_terminal,header + "\n" + graphics['coin_flip_heads' if flip == 'heads' else 'coin_flip_tails'])

    if(choice.lower() == "h" and flip == 'heads'):
        input(c.backYELLOW+c.BLACK+f"\rPlayer {player_name}: You got heads!")
        ss.overwrite("\r" + " " * 40)
        score[0] += 1
    elif(choice.lower() == "h" and flip == 'tails'):
        input(c.backYELLOW+c.BLACK+f"\r Player {player_name}: You got tails...")
        ss.overwrite("\r" + " " * 40)
    elif(flip == 'heads'):
        input(c.backYELLOW+c.BLACK+f"\rPlayer {player_name}: You got heads...")
        ss.overwrite("\r" + " " * 40)
    else:
        input(c.backYELLOW+c.BLACK+f"\rPlayer {player_name}: You got tails!")
        ss.overwrite("\r" + " " * 40)
        score[0] += 1

    if(score[0] == 1):
        ss.update_quadrant(active_terminal, header + f"\n{graphics['casino_win']}")
        bet *= 2
    else:
        ss.update_quadrant(active_terminal, header + f"\n{graphics['casino_lose']}")
        bet = 0
    input("\r")
    ss.overwrite("\r" + " " * 40)
    return bet
