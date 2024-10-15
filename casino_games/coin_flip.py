# BLACKJACK
import os
import random
from time import sleep

game_title = "⛁ Coin Flip"

# 0 - Heads, 1 - Middle/Flip, 2 - Tails
flip_anims = ["                                                                           \n                    █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█                   \n                    █                                  █                   \n                    █                                  █                   \n                    █        █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█        █                   \n                    █        █                █        █                   \n                    █        █                █        █                   \n                    █        █    █      █    █        █                   \n                    █        █    █      █    █        █                   \n                    █        █                █        █                   \n                    █        █                █        █                   \n                    █        █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█        █                   \n                    █             ▉      ▉             █                   \n                    █             ▉      ▉             █                   \n                    █       █▀▀▀▀▀▀      ▀▀▀▀▀▀█       █                   \n                    █      █                    █      █                   \n                    █     █                      █     █                   \n                    █    █                        █    █                   \n                    █▄▄▄█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█▄▄▄█                   \n                                                                           \n",
              "                                                                           \n                                                                           \n                                                                           \n                                                                           \n                                                                           \n                                                                           \n                   ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                    \n                   █                                  █                    \n                   █                                  █                    \n                   █                                  █                    \n                   █                                  █                    \n                   █                                  █                    \n                   █                                  █                    \n                   █                                  █                    \n                   ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀                    \n                                                                           \n                                                                           \n                                                                           \n                                                                           \n                                                                           \n",
              "                                                                           \n                   █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█                    \n                   █                                  █                    \n                   █                                  █                    \n                   █                                  █                    \n                   █      ██████████████████████      █                    \n                   █     ▀▀▀█▀▀▀█▀▀▀██▀▀▀█▀▀▀█▀▀▀     █                    \n                   █        █   █   ██   █   █        █                    \n                   █        █   █   ██   █   █        █                    \n                   █        █   █   ██   █   █        █                    \n                   █        █   █   ██   █   █        █                    \n                   █        █   █   ██   █   █        █                    \n                   █        █   █   ██   █   █        █                    \n                   █        █   █   ██   █   █        █                    \n                   █    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀    █                    \n                   █                                  █                    \n                   █                                  █                    \n                   █                                  █                    \n                   █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█                    \n                                                                           \n"]

status = ["                                                                           \n                                                                           \n     ██████           █████████████ ███████████████ ██████████████████     \n     ██████           █████████████ ███████████████ ██████████████████     \n     ██████           █████████████ ███████████████ ██████████████████     \n     ██████           ████     ████ ████            ████                   \n     ██████           ████     ████ ████            ████                   \n     ██████           ████     ████ ████            ████                   \n     ██████           ████     ████ ████            ██████████████████     \n     ██████           ████     ████ ███████████████ ██████████████████     \n     ██████           ████     ████ ███████████████ ██████████████████     \n     ██████           ████     ████ ███████████████ ████                   \n     ██████           ████     ████            ████ ████                   \n     ██████           ████     ████            ████ ████                   \n     ████████████████ ████     ████            ████ ████                   \n     ████████████████ █████████████ ███████████████ ██████████████████     \n     ████████████████ █████████████ ███████████████ ██████████████████     \n     ████████████████ █████████████ ███████████████ ██████████████████     \n                                                                           \n                                                                           \n",
          "                                                                           \n                                                                           \n        ██████     █████      ██████ ████████ █████████████████████        \n        ██████     █████      ██████ ████████ █████████████████████        \n        ██████     █████      ██████ ████████ █████████████████████        \n        ██████     █████      ██████ ████████ █████████████████████        \n        ██████     █████      ██████ ████████ ███████       ███████        \n        ██████     █████      ██████ ████████ ███████       ███████        \n        ██████     █████      ██████ ████████ ███████       ███████        \n        ██████     █████      ██████ ████████ ███████       ███████        \n        ██████     █████      ██████ ████████ ███████       ███████        \n        ██████     █████      ██████ ████████ ███████       ███████        \n        ██████     █████      ██████ ████████ ███████       ███████        \n        ██████     █████      ██████ ████████ ███████       ███████        \n        ████████████████████████████ ████████ ███████       ███████        \n        ████████████████████████████ ████████ ███████       ███████        \n        ████████████████████████████ ████████ ███████       ███████        \n        ████████████████████████████ ████████ ███████       ███████        \n                                                                           \n                                                                           \n"]

header = "─" * ((75 - len(game_title)) // 2) + game_title + "─" * ((75 - len(game_title)) // 2)

def play(player, active_terminal, bet):
    score = [0,0,0,0]

    choice = input(player.COLORS.backYELLOW+player.COLORS.BLACK+f"\nPlayer {1}: Heads or Tails? (h/T) ")
    player.ss.overwrite("\r" + " " * 40)
    flip = random.randint(0,1)
    
    #TODO - Make the animation asynchrnous.
    player.ss.update_quadrant(active_terminal,header + "\n" + flip_anims[0])
    player.ss.print_screen()
    sleep(0.2)
    player.ss.update_quadrant(active_terminal,header + "\n" + flip_anims[1])
    player.ss.print_screen()
    sleep(0.2)
    player.ss.update_quadrant(active_terminal,header + "\n" + flip_anims[2])
    player.ss.print_screen()
    sleep(0.2)
    player.ss.update_quadrant(active_terminal,header + "\n" + flip_anims[1])
    player.ss.print_screen()
    sleep(0.2)
    player.ss.update_quadrant(active_terminal,header + "\n" + flip_anims[2 if flip == 1 else 0])
    player.ss.print_screen()

    if(choice.lower() == "h" and flip == 0):
        input(player.COLORS.backYELLOW+player.COLORS.BLACK+f"\rPlayer {1}: You got heads!")
        player.ss.overwrite("\r" + " " * 40)
        score[0] += 1
    elif(choice.lower() == "h" and flip == 1):
        input(player.COLORS.backYELLOW+player.COLORS.BLACK+f"\rPlayer {1}: You got tails...")
        player.ss.overwrite("\r" + " " * 40)
    elif(flip == 0):
        input(player.COLORS.backYELLOW+player.COLORS.BLACK+f"\rPlayer {1}: You got heads...")
        player.ss.overwrite("\r" + " " * 40)
    else:
        input(player.COLORS.backYELLOW+player.COLORS.BLACK+f"\rPlayer {1}: You got tails!")
        player.ss.overwrite("\r" + " " * 40)
        score[0] += 1

    if(score[0] == 1):
        player.ss.update_quadrant(active_terminal, header + f"\n{status[1]}")
        bet *= 2
    else:
        player.ss.update_quadrant(active_terminal, header + f"\n{status[0]}")
        bet = 0
    player.ss.print_screen()
    input("\r")
    player.ss.overwrite("\r" + " " * 40)
    return bet
