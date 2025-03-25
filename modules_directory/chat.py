import screenspace as ss
from socket import socket
import networking as net
from style import MYCOLORS as c, graphics as g

module_name = "Chat"
command = "chat"
title = c.WHITE + f"THE CHAT".center(75)
help_text = "─" * 24 + "THE CHAT HAS BEEN CLOSED" + "─" * 25 + "\nType 'chat' to hop back in!"
persistent = True
oof_params = {"player_id": None, "server": None}

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
    
    # player_name = "0" # Placeholder for player name. 
    # # Maybe just query the server for the player name?

    net.send_message(server, f"{player_id}get_name")
    output = title + "\n" + net.receive_message(server)
    active_terminal.update(output, False)

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


    # active_terminal.update(output)



def set_oof_params(player_id: int, server: socket) -> None:
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



def handle(data, client_socket, messages, id, name):
    """
    Handles chat messages and player-related commands sent by a client.
    """
    ret_val = ""

    if "chat" in data:
        """
        Extract and format the message with the player's name.
        """
        parts = data.split(" ", 1)
        message = parts[1]
        ret_val += f"[{name}]: {message}"

    if "get_name" in data:
        """
        Return the player's name.
        """
        ret_val += name

    net.send_message(client_socket, ret_val)







