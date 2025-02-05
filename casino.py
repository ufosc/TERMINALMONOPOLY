from time import sleep
import player
import screenspace as ss
import os
import networking as net

module_name = "Casino"
module_command = "casino"
module_description = "Gamble your money at the casino!"

def module(active_terminal, socket):
    """
    Casino Module
    Author: Jordan Brotherton (github.com/jordanbrotherton)
    Version: 1.0
    Gamble your money away!
    A basic menu loader for casino_games.
    """
    wrong = 0
    while True:
        net.send_message(socket, "bal 0")
        sleep(0.1)
        balance = int(net.receive_message(socket))
        ss.overwrite(player.COLORS.RESET + "\rSelect a game through typing the associated command and wager. (ex. 'coin_flip 100')" + " " * 20)
        ss.update_quadrant(active_terminal, "─" * 31 + "CASINO MODULE" + "─" * 31 + f"\n$ BALANCE = {balance} $\nSelect a game by typing the command and wager." + get_submodules() + "\n☒ Exit (e)")
        if(wrong == 1):
            ss.overwrite(player.COLORS.RESET + player.COLORS.RED + "\rGame does not exist. Refer to the list of games. (ex. 'coin_flip 100')")
        elif(wrong == 2):
            ss.overwrite(player.COLORS.RESET + player.COLORS.RED + "\rInvalid input. Type in the name of the game followed by the wager. (ex. 'coin_flip 100')")
        elif(wrong == 3):
            ss.overwrite(player.COLORS.RESET + player.COLORS.RED + "\rWager has to be an integer greater than 0. Type in the name of the game followed by the wager. (ex. 'coin_flip 100')")
        game = input(player.COLORS.backYELLOW+player.COLORS.BLACK+f"\r").lower().split(" ")
        ss.overwrite(player.COLORS.RESET+"\r" + " " * 40)
        if(game[0] == ""):
            wrong = 2
        elif(game[0] == "e"):
            ss.update_quadrant(active_terminal, "─" * 31 + "CASINO MODULE" + "─" * 31 + "\nType 'casino' to go back to the casino!")
            break
        elif(len(game) == 1):
            wrong = 2
        elif(not game[1].isdigit()):
            wrong = 3
        elif(game[1] == "0"):
            wrong = 3
        elif(game[0] == "game"):
            wrong = 1 #Don't import the template...
        else:
            try:
                wrong = 0
                i = __import__('casino_games.' + game[0], fromlist=[''])

                wager = int(game[1])
                if(wager == 0): continue

                #player.balance -= bet
                net.send_message(socket, "bal -" + str(wager))
                sleep(0.1)
                balance = int(net.receive_message(socket))

                ss.overwrite(player.COLORS.RESET+"\r" + " " * 40)
                net_change = i.play(player,active_terminal,wager)
                net.send_message(socket, "bal " + str(net_change))
                sleep(0.1)
                balance = int(net.receive_message(socket))
            except ImportError:
                wrong = 1

def get_submodules():
    modules_list = ""
    for file in os.listdir("casino_games"):
        if file.endswith(".py"):
            file = file[:-3]
            i = __import__('casino_games.' + file, fromlist=[''])
            if(hasattr(i, 'game_title')):
                modules_list += f"\n{i.game_title} ({file})"
    return modules_list

if __name__ == "__main__":
    module(1)
