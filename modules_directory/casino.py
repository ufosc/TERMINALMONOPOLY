from time import sleep
from style import MYCOLORS as c, graphics as g
import screenspace as ss
from screenspace import Terminal
import os
import networking as net
from socket import socket

name = "Casino Loader"
command = "casino"
description = "Gamble your money at the casino!"
help_text = "Type CASINO to enter the casino, where you can gamble your money for in high stakes and low stakes. There's a little something for everyone."
persistent = False # No need to run additional commands after switching
# No out of focus function needed, because the terminal closes after use

def run(player_id: int, server: socket, active_terminal: Terminal):
    """
    Casino Module
    Author: Jordan Brotherton (github.com/jordanbrotherton)
    Version: 1.3 - Moved to its own file
    Gamble your money away!
    A basic menu loader for casino_games.
    """
    wrong = 0
    while True:
        net.send_message(server, f"{player_id}bal")
        # sleep(0.1)
        balance = int(net.receive_message(server))
        ss.overwrite(c.RESET + "\rSelect a game through typing the associated command and wager. (ex. 'coin_flip 100')" + " " * 20)
        active_terminal.update("─" * 31 + "CASINO MODULE" + "─" * 31 + "\n" + f"AVAILABLE CASH: ${balance}".center(75) + "\n\nSelect a game by typing the command and wager.\n\n"
                       + "GAME SELECTION".ljust(37, ".") + " COMMAND\n\n" + get_submodules() + "\n☒ Exit (e)")
        if(wrong == 1):
            ss.overwrite(c.RESET + c.RED + "\rGame does not exist. Refer to the list of games. (ex. 'coin_flip 100')")
        elif(wrong == 2):
            ss.overwrite(c.RESET + c.RED + "\rInvalid input. Type in the name of the game followed by the wager. (ex. 'coin_flip 100')")
        elif(wrong == 3):
            ss.overwrite(c.RESET + c.RED + "\rWager has to be an integer greater than 0. Type in the name of the game followed by the wager. (ex. 'coin_flip 100')")
        game = input(c.backYELLOW+c.BLACK+f"\r").lower().split(" ")
        print(c.RESET, end="") #Reset the color
        ss.overwrite(c.RESET+"\r" + " " * 40)
        if(game[0] == ""):
            wrong = 2
        elif(game[0] == "e"):
            active_terminal.update(g.get("casino_exit"))
            active_terminal.command = "" # Clear the command to allow re-running
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

                net.send_message(server, f"{player_id}casino lose {wager}")
                sleep(0.1)
                balance = int(net.receive_message(server))

                ss.overwrite(c.RESET+"\r" + " " * 40)
                winnings = i.play(active_terminal,wager)
                net.send_message(server, f"{player_id}casino win {winnings}")
                sleep(0.1)
                balance = int(net.receive_message(server))
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
                modules_list += f"{i.game_title.ljust(37, '.')} {file}\n"
    return modules_list

def handle(cmds: str, client_socket, change_balance, add_to_output_area, id, name) -> None:
    """
    Handles casino-related commands for a client by updating their balance.

    Args:
        cmds (str): The command string containing the casino operation details.
                    Expected format: "casino [casino_id] [change_balance]"
                    - [delta] (str): The player's win or loss string.
                    - [change_balance] (int): The amount to change the client's balance by.
        current_client (Client): The client whose balance is to be updated.

    Returns:
        None

    Example:
        handle_casino("casino win 100", client)
        This will add 100 to the client's balance.
    """
    command_data = cmds.split(' ')
    delta = 1 if command_data[1] == 'win' else -1
    amount = int(command_data[2])
    money = change_balance(id, delta * amount)
    add_to_output_area("Casino", f"Updated {name}'s balance by {delta * amount}. New balance: {money}")
    net.send_message(client_socket, str(money))


if __name__ == "__main__":
    run(1)
