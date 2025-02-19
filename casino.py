from time import sleep
from style import COLORS as c
import screenspace as ss
from screenspace import Terminal
import os
import networking as net
from socket import socket

module_name = "Casino"
module_command = "casino"
module_description = "Gamble your money at the casino!"

def module(socket: socket, active_terminal: Terminal, pid: int):
    """
    Casino Module
    Author: Jordan Brotherton (github.com/jordanbrotherton)
    Version: 1.1 - Revised to better use network commands to modify balance.
    Gamble your money away!
    A basic menu loader for casino_games.
    """
    wrong = 0
    while True:
        net.send_message(socket, f"{pid}bal")
        sleep(0.1)
        balance = int(net.receive_message(socket))
        ss.overwrite(c.RESET + "\rSelect a game through typing the associated command and wager. (ex. 'coin_flip 100')" + " " * 20)
        active_terminal.update("─" * 31 + "CASINO MODULE" + "─" * 31 + f"\n$ BALANCE = {balance} $\nSelect a game by typing the command and wager." + get_submodules() + "\n☒ Exit (e)")
        if(wrong == 1):
            ss.overwrite(c.RESET + c.RED + "\rGame does not exist. Refer to the list of games. (ex. 'coin_flip 100')")
        elif(wrong == 2):
            ss.overwrite(c.RESET + c.RED + "\rInvalid input. Type in the name of the game followed by the wager. (ex. 'coin_flip 100')")
        elif(wrong == 3):
            ss.overwrite(c.RESET + c.RED + "\rWager has to be an integer greater than 0. Type in the name of the game followed by the wager. (ex. 'coin_flip 100')")
        game = input(c.backYELLOW+c.BLACK+f"\r").lower().split(" ")
        ss.overwrite(c.RESET+"\r" + " " * 40)
        if(game[0] == ""):
            wrong = 2
        elif(game[0] == "e"):
            active_terminal.update("─" * 31 + "CASINO MODULE" + "─" * 31 + "\nType 'casino' to go back to the casino!")
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

                net.send_message(socket, f"{pid}casino lose {wager}")
                sleep(0.1)
                balance = int(net.receive_message(socket))

                ss.overwrite(c.RESET+"\r" + " " * 40)
                winnings = i.play(active_terminal,wager)
                net.send_message(socket, f"{pid}casino win {winnings}")
                sleep(0.1)
                balance = int(net.receive_message(socket))
            except ImportError:
                wrong = 1

def get_submodules():
    """
    Retrieves a list of available casino game submodules.

    This function scans the "casino_games" directory for Python files, dynamically 
    imports each module, and checks if the module has a 'game_title' attribute.
    If the attribute exists, the game's title along with its command name is added 
    to the formatted list.

    Returns:
        str: A formatted string listing all available casino games with their commands.
    """
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
