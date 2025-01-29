# COIN FLIP
import os
import random
from time import sleep
import screenspace as ss
from style import get_graphics

game_title = "⛁ Coin Flip"
header = "─" * ((75 - len(game_title)) // 2) + game_title + "─" * ((75 - len(game_title)) // 2)

def play(player, active_terminal, bet):
    score = [0,0,0,0]

    graphics = get_graphics()

    choice = input(player.COLORS.backYELLOW+player.COLORS.BLACK+f"\rPlayer {1}: Heads or Tails? (h/T) ")
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
        input(player.COLORS.backYELLOW+player.COLORS.BLACK+f"\rPlayer {1}: You got heads!")
        ss.overwrite("\r" + " " * 40)
        score[0] += 1
    elif(choice.lower() == "h" and flip == 'tails'):
        input(player.COLORS.backYELLOW+player.COLORS.BLACK+f"\rPlayer {1}: You got tails...")
        ss.overwrite("\r" + " " * 40)
    elif(flip == 'heads'):
        input(player.COLORS.backYELLOW+player.COLORS.BLACK+f"\rPlayer {1}: You got heads...")
        ss.overwrite("\r" + " " * 40)
    else:
        input(player.COLORS.backYELLOW+player.COLORS.BLACK+f"\rPlayer {1}: You got tails!")
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
