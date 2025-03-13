from time import sleep
from style import COLORS as c
import screenspace as ss
from screenspace import Terminal
import os
import networking as net
import stock_market as sm
from socket import socket
import style as st

module_name = "Chat"
module_command = "chat"
title = c.WHITE + "\033[0m THE CHAT\n\n"
output = title


def render(active_terminal: Terminal, name: str, msg: str, person: int):
    global output

    if person == 1:
        output += c.LIGHTBLUE + " " + name + "\n"
        output += c.WHITE + " " + msg + "\n\n"

    if person == 2:
        output += c.ORANGE + " " + name + "\n"
        output += c.WHITE + " " + msg + "\n\n"

    if person == 3:
        output += c.RED + " " + name + "\n"
        output += c.WHITE + " " + msg + "\n\n"

    if person == 4:
        output += c.GREEN + " " + name + "\n"
        output += c.WHITE + " " + msg + "\n\n"

    active_terminal.update(output, padding=False)


# def delete_last_message(text):
#     lines = text.splitlines(keepends=True)  # Split string into lines
#     preserved_title = lines[:3]
#     chat_messages = lines[3:]
#
#     if len(chat_messages) >= 2:
#         chat_messages = chat_messages[2:]
#
#     new_text = "\n".join(preserved_title + chat_messages)
#
#     return new_text


def module(socket: socket, active_terminal: Terminal, pid: int, name: str):
    """
    Stocks Module
    Author: Hiral Shukla (github.com/hiralshukla)
    Author: Shan Sundal (github.com/ssundal)
    Version: 1.0 - attempting to create a chat feature

    """
    global output
    msg_counter = 0
    person = 1
    active_terminal.clear()
    active_terminal.update(title, padding=False)
    while True:
        net.send_message(socket, f"{pid}chat_name")
        sleep(0.1)
        name = str(net.receive_message(socket))
        ss.overwrite(c.RESET + f"\rEnter your message here: " + " " * 20)
        msg = input(c.LIGHTBLUE + f"\r")
        # if msg_counter >= 6:
        #     output = delete_last_message(output)
        render(active_terminal, name, msg, person)
        msg_counter += 1

        if person == 5:
            person = 1
        else:
            person += 1

        if msg == "e":
            active_terminal.clear()
            active_terminal.update("─" * 24 + "THE CHAT HAS BEEN CLOSED" + "─" * 25 + "\nType 'chat' to hop back in!")
            ss.overwrite(c.RESET + "\r" + " " * 40)
            break
