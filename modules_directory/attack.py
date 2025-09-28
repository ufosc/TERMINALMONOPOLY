from utils.utils import MYCOLORS as c, g # g is graphics
from utils.utils import screenspace as ss
from utils.utils import Terminal
import os
import networking as net
from socket import socket

name = "Attack Loader"
command = "attack"
help_text = "Switch to the attack module to attack another player! Attacking other players is a crucial part of Terminal Monopoly. Successfully attacking other players will cripple their mobility on their terminals, and put them in precarious situations on the gameboard. All attacks are played out by winning against another player in some **active** module."
persistent = False # No need to run additional commands after switching
# No out of focus function needed, because the terminal closes after use

def run(player_id: int, server: socket, active_terminal: Terminal):
    """
    Attack Module
    Author: Chi Xu
    Version: 1.0 - Moved to its own file
    Attack fellow players!
    A basic menu loader for attack_games.
    """
    active_terminal.persistent = persistent
    wrong = 0
    while True:
        #net.send_message(server, f"{player_id}bal")
        # sleep(0.1)
        #balance = int(net.receive_message(server))
        ss.overwrite(c.RESET + "\rSelect a game through typing the associated command, amount, and player id. (ex. 'guessing_game 20 2')" + " " * 20)
        active_terminal.update("─" * 31 + "ATTACK MODULE" + "─" * 31 + "\n" + "\n\nSelect a game by typing the command and wager.\n\n"
                       + "GAME SELECTION".ljust(37, ".") + " COMMAND\n\n" + get_submodules() + "\n☒ Exit (e)")
        if(wrong == 1):
            ss.overwrite(c.RESET + c.RED + "\rGame does not exist. Refer to the list of games. (ex. 'guessing_game 20 2 0')")
        elif(wrong == 2):
            ss.overwrite(c.RESET + c.RED + "\rInvalid input. Type in the name of the game followed by the penalty amount, and attacked player id. (ex. 'guessing_game 20 2 or guessing_game 100 0')")
        elif(wrong == 3):
            ss.overwrite(c.RESET + c.RED + "\rAmount has to be an integer greater than 0. Type in the name of the game followed by the amount. (ex. 'guessing_game 20 2 0')")
        elif(wrong == 4):
            ss.overwrite(c.RESET + c.RED + "\rID picked is not valid. (ex. 'guessing_game 20 2')")
        game = input(c.backYELLOW+c.BLACK+f"\r").lower().split(" ")
        print(c.RESET, end="") #Reset the color
        ss.overwrite(c.RESET+"\r" + " " * 40)
        if active_terminal.status != "ACTIVE":
            break  # Exit the loop if the Terminal is no longer active
        if(game[0] == ""):
            wrong = 2
        elif(game[0] == "e"):
            active_terminal.update(g.get("attack_exit"))
            active_terminal.command = "" # Clear the command to allow re-running
            break
        elif(len(game) < 3):
            wrong = 2
        elif(not game[1].isdigit()):
            wrong = 3
        elif(game[1] == "0"):
            wrong = 3
        elif(game[0] == "game"):
            wrong = 1 #Don't import the template...
        elif (game[2]).strip() == str(player_id) or not (game[2]).isdigit():
            wrong = 4 #don't attack self
        else:
            #need formating game[2] is id game[0] is game game[1] is bet
            net.send_message(server, f"{player_id}attack {game[2]} {game[0]} {game[1]} {player_id}")

            #active_terminal.enable(False, server, player_id)
            return

            """
            try:
                wrong = 0
                # needs to load on attacked player not attacking player
                i = __import__('attack_modules.' + game[0], fromlist=[''])

                type = (game[1])
                amt = int(game[2])
                if (amt == 0): continue
                attacked_player_id = game[3]
                net.send_message(server, f"{attacked_player_id}attack lose {type, amt}")
                sleep(0.1)
                ss.overwrite(c.RESET + "\r" + " " * 40)
                winnings = i.play(active_terminal, amt)
                net.send_message(server, f"{attacked_player_id}attack win {type, amt}")
                sleep(0.1)
            except ImportError:
                wrong = 1
            except IndexError:
                wrong = 4
            """


def get_submodules():
    """
    Retrieves a list of available attack game submodules.

    This function scans the "attack_games" directory for Python files, dynamically
    imports each module, and checks if the module has a 'game_title' attribute.
    If the attribute exists, the game's title along with its command name is added
    to the formatted list.

    Returns:
        str: A formatted string listing all available attack games with their commands.
    """
    modules_list = ""
    for file in os.listdir("attack_modules"):
        if file.endswith(".py"):
            file = file[:-3]
            i = __import__('attack_modules.' + file, fromlist=[''])
            if(hasattr(i, 'game_title')):
                modules_list += f"{i.game_title.ljust(37, '.')} {file}\n"
    return modules_list
"""
def handle_attack_game(cmds: str, client_socket, change_balance, add_to_output_area, id, name) -> None:
    
    Handles attack-related commands for a client by updating their balance.

    Args:
        cmds (str): The command string containing the attack operation details.
                    Expected format: "attack [attack_id] [change_balance]"
                    - [delta] (str): The player's win or loss string.
                    - [change_balance] (int): The amount to change the client's balance by.
        current_client (Client): The client whose balance is to be updated.

    Returns:
        None

    Example:
        handle_attack("attack win 100", client)
        This will add 100 to the client's balance.
    
    command_data = cmds.split(' ')
    delta = 0 if command_data[1] == 'win' else -1
    amount = int(command_data[2])
    money = change_balance(id, delta * amount)
    add_to_output_area("attack", f"Updated {name}'s balance by {delta * amount}. New balance: {money}")
    #this sends to self need to send to client
    net.send_message(client_socket, str(money))

"""
if __name__ == "__main__":
    run(1)
