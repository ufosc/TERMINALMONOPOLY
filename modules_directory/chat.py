import screenspace as ss
from socket import socket
import networking as net
from style import MYCOLORS as c, graphics as g
import threading
import time

module_name = "Chat"
command = "chat"
title = c.WHITE + "THE CHAT".center(75) +'\n'
help_text = "The chat is closed. Type 'chat' to hop back in!"
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
    active_terminal.oof_callable = oof
    global oof_params
    oof_params = net.set_oof_params(player_id, server)

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

def oof() -> str:
    """
    Update function for when the chat terminal is out of focus.
    Receives any pending messages from the server.

    Returns:
        str: The latest chat history string.
    """
    server = oof_params["server"]
    player_id = oof_params["player_id"]
    global chat_history

    try:
        # Ask the server for updated chat history
        net.send_message(server, f'{player_id}chat,recieve_msg')
        new_history = net.receive_message(server)

        # Only update if there's a change
        if new_history != chat_history:
            chat_history = new_history

        lines = chat_history.split('\n')
        lines = [line if len(line) <= 75 else line[:75] for line in lines]
        lines = lines[-19:]
        # while len(lines) < 19:
        #     lines.insert(0, "")  # pad lines if needed

        output = title + '\n'.join(lines)
        return output

    except Exception as e:
        return title + '\n'.join(chat_history.split('\n')[-19:]) if chat_history else title


def chat_listener(player_id: int, server: socket, active_terminal: ss.Terminal, stop_event): 
    """
    Threading function that ensures any time a message is entered by anyone chat is updated for all. 

    Args:
    player_id (str): The id of the player.
    server (socket): The server connection.
    active_terminal (ss.Terminal): The terminal to display the information.
    stop_event: Whether or not thread was terminated. 

    Returns:
        None
    """
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

    Args:
    data: Data incoming from client.
    client_socket: Client connection.
    messages: Chat history global variable from banker.
    id: Client id. 
    name: Client

    Returns:
        None
    """
    data = data.split(',', 2)
    ret_val = ""

    if "recieve_msg" in data:
        """
        Recreate the chat history using global messages from banker.
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
        """
        Add incoming message from user to the chat history.
        """
        msg = data[2]
        messages.append(name + ',' + msg)

    if "get_name" in data:
        """
        Return the player's name.
        """
        ret_val += name

    net.send_message(client_socket, ret_val)







