import screenspace as ss
from socket import socket
import networking as net
from style import MYCOLORS as c, graphics as g
import threading
import time

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
    Version: 1.0 - attempting to create a chat feature

    Args:
    player_id (int): The ID of the player.
        server (socket): The server socket to communicate with.
        active_terminal (ss.Terminal): The terminal to display the information.

    Returns:
        None

    """
    # clears the terminal, labels as a persistent module, and calls out of focu
    active_terminal.clear()
    active_terminal.persistent = persistent
    set_oof_params(player_id, server)

    # preps the title and welcome message to the chatter and prints to screen
    active_terminal.update(title)
    net.send_message(server, f"{player_id}chat,get_name")
    output = title + "\n" + "Welcome " + net.receive_message(server) + " to the chat!"
    active_terminal.update(output, False)

    stop_event = threading.Event() # sets ability to stop thread
    listener_thread = threading.Thread(target=chat_listener, args=(player_id, server, active_terminal, stop_event))
    # creates a thread that runs the chat_listener function, and passes the correct arguments to it
    listener_thread.daemon = True # tells python to not wait for the thread when exiting the program 
    listener_thread.start() # actually starts the thread in the background and polls the server every 0.5 seconds
    # while main thread waits for user input

    while True: # main loop
        ss.overwrite(c.RESET + f"\rEnter your message here: ") # ability to send message 
        ss.set_cursor(45, 0) # !!! should move the cursor back to the right location
        msg = input(c.LIGHTBLUE + f"\r") # takes user input
        
        if msg.lower() == "e": # quits chat
            print(c.RESET, end="") # clear everything 
            ss.overwrite(c.RESET + "\r" + " " * 40)
            stop_event.set()  # signal thread to stop
            break

        print(c.RESET, end="") 
        ss.overwrite(c.RESET + "\r" + " " * 40)
        net.send_message(server, f'{player_id}chat,add_msg,{msg}') # adds message to chat when input recieved



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

def oof():
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

def chat_listener(player_id: int, server: socket, active_terminal: ss.Terminal, stop_event): 
    global chat_history
    while not stop_event.is_set(): # when stop isn't True it runs
        try:
            net.send_message(server, f'{player_id}chat,recieve_msg')
            new_history = net.receive_message(server)

            if new_history != chat_history:
                chat_history = new_history
                lines = chat_history.split('\n')
                lines = [line if len(line) <= 75 else line[:75] for line in lines]
                lines = lines[-19:]
                output = title + '\n'.join(lines)
                active_terminal.update(output)

            time.sleep(0.5)  # add this to slow down polling
        except:
            pass


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







