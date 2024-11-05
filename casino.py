from time import sleep
import player
import screenspace as ss
import os
import networking as net

module_name = "Casino"
module_command = "casino"
module_description = "Gamble your money at the casino!"

def module(active_terminal, socket):
    wrong = False
    while True:
        net.send_message(socket, "bal 0")
        sleep(0.1)
        balance = int(net.receive_message(socket))
        ss.overwrite(player.COLORS.RESET + "\rSelect a game through typing the associated command." + " " * 20)
        ss.update_quadrant(active_terminal, "─" * 31 + "CASINO MODULE" + "─" * 31 + f"\n$ BALANCE = {balance} $\nSelect a game by typing the command." + get_submodules() + "\n☒ Exit (e)")
        if(wrong):
            ss.overwrite(player.COLORS.RESET + player.COLORS.RED + "\rGame does not exist. Refer to the list of games.")
        game = input(player.COLORS.backYELLOW+player.COLORS.BLACK+f"\r").lower().split(" ")
        ss.overwrite(player.COLORS.RESET+"\r" + " " * 40)
        if(game[0] == "e"):
            ss.update_quadrant(active_terminal, "─" * 31 + "CASINO MODULE" + "─" * 31 + "\nType 'casino' to go back to the casino!")
            break
        elif(game[0] == "game"):
            wrong = True #Don't import the template...
        else:
            try:
                wrong = False
                i = __import__('casino_games.' + game[0], fromlist=[''])

                bet = get_bet()
                if(bet == 0): continue

                #player.balance -= bet
                net.send_message(socket, "bal -" + str(bet))
                sleep(0.1)
                balance = int(net.receive_message(socket))

                ss.overwrite(player.COLORS.RESET+"\r" + " " * 40)
                net_change = i.play(player,active_terminal,bet)
                net.send_message(socket, "bal " + str(net_change))
                sleep(0.1)
                balance = int(net.receive_message(socket))
            except ImportError:
                wrong = True

def get_bet():
    ss.overwrite(player.COLORS.RESET + "\rType in your bet. (0 to cancel)" + " " * 20)
    while True:
        try:
            bet = int(input(player.COLORS.backYELLOW+player.COLORS.BLACK+f"\r"))
            if(bet < 0):
                ss.overwrite(player.COLORS.RESET + player.COLORS.RED+"\rYou need to bet a number above 0. (0 to cancel)" + " " * 20)
            else:
                ss.overwrite(player.COLORS.RESET+"\r" + " " * 60)
                return bet
        except ValueError:
            ss.overwrite(player.COLORS.RESET + player.COLORS.RED+"\rType in a valid number for your bet. (0 to cancel)" + " " * 20)

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
