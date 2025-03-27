import screenspace as ss
from socket import socket
import networking as net
from style import MYCOLORS as c, graphics as g
import threading

module_name = "Chat"
command = "chat"
title = c.WHITE + "THE CHAT".center(75) +'\n'
help_text = "─" * 24 + "THE CHAT HAS BEEN CLOSED" + "─" * 25 + "\nType 'chat' to hop back in!"
persistent = True
oof_params = {"player_id": None, "server": None}
chat_history = ""

def run(player_id: int, server: socket, active_terminal: ss.Terminal):
    """
    Chat Module
    Author: Hiral Shukla (github.com/hiralshukla)
    Author: Shan Sundal (github.com/ssundal)
    Version: 1.0 - attempting to create a chat feature

    Args:
    player_id (int): The ID of the player.
        server (socket): The server socket to communicate with.
        active_terminal (ss.Terminal): The terminal to display the information.

    Returns:
        None

    """
    active_terminal.clear()
    active_terminal.persistent = persistent
    active_terminal.oof_callable = oof
    set_oof_params(player_id, server)

    active_terminal.update(title)


    net.send_message(server, f"{player_id}chat,get_name")
    output = title + "\n" + "Welcome " + net.receive_message(server) + " to the chat!"
    active_terminal.update(output, False)

    # start threading 
    #kill thread at end of run
    while True:

        # net.send_message(server, f'{player_id}chat,recieve_msg')
        # chat_history = net.receive_message(server)

        #get_message() #implement in handle 
        #threading
        #kill last line of run


        ss.overwrite(c.RESET + f"\rEnter your message here: " + " " * 20)
        msg = input(c.LIGHTBLUE + f"\r")

        if msg.lower() == "e":
            print(c.RESET, end="")
            ss.overwrite(c.RESET + "\r" + " " * 40)
            break

        print(c.RESET, end="")
        ss.overwrite(c.RESET + "\r" + " " * 40)
        net.send_message(server, f'{player_id}chat,add_msg,{msg}')
        net.receive_message(server)
        net.send_message(server, f'{player_id}chat,recieve_msg')
        chat_history = net.receive_message(server)

        lines = chat_history.split('\n')
        lines = [line if len(line) <= 75 else line[:75] for line in lines]     
        lines = lines[-19:]                
        chat_history = '\n'.join(lines)
        output = title + chat_history


        active_terminal.update(output)



def set_oof_params(player_id: int, server: socket) -> None:
    return None
    """
       Sets the parameters for the out of focus function.

       Args:
           player_name (str): The name of the player.
           server (socket): The server connection.
           incoming_msg (str): The incoming message of a user

       Returns:
           None
       """
    oof_params["player_id"] = id
    oof_params["server"] = server

def oof() -> str:
    return None
    """
       Update function for when the chat terminal is out of focus.
       Receives any pending messages from the server.

       Returns:
           str: The latest chat message.
       """
    server = oof_params["server"]
    player_id = oof_params["player_id"]
    
    # player_name = "0" # Placeholder for player name. 
    # # Maybe just query the server for the player name?

    # net.send_message(server, f"{player_id}get_name")
    # player_name = net.receive_message(server)

    # output = title
    # chat_history = []

    # net.send_message(server, f'{player_id}chat')
    # ss.overwrite(c.RESET + f"\rEnter your message here: " + " " * 20)

    # msg = input(c.LIGHTBLUE + f"\r")
    # print(c.RESET, end="")
    # ss.overwrite(c.RESET + "\r" + " " * 40)

    # # if msg.lower() == "e":
    # #     break

    # net.send_message(server, f'{player_id}chat {msg}')
    # incoming_msg = net.receive_message(server)


    # if len(chat_history) > 10:
    #     chat_history.pop(0)
    # else:
    #     output = output + c.LIGHTBLUE + player_name + c.RESET + msg + incoming_msg

    # return output

def get_message(player_id: int, server: socket, active_terminal: ss.Terminal): 
    return 0


def handle(data, client_socket, messages, id, name):
    """
    Handles chat messages and player-related commands sent by a client.
    """
    data = data.split(',', 2)
    ret_val = ""

    if "recieve_msg" in data:
        """
        Extract and format the message with the player's name.
        """
        for line in messages:
            if line != "":
                line = line.split(',', 1)
                username = line[0]
                msg = line[1]
                ret_val += f"[{username}]: {msg}\n"
            else:
                net.send_message(client_socket, ret_val)

    if "add_msg" in data: 
        msg = data[2]
        messages.append(name + ',' + msg)

    if "get_name" in data:
        """
        Return the player's name.
        """
        ret_val += name

    net.send_message(client_socket, ret_val)







