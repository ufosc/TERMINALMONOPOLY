HEADERSIZE = 10 # Max length of the header, meaning the max length of the message is 10^10 bytes
import socket

# Credit to sentdex's video @ https://www.youtube.com/watch?v=8A4dqoGL62E 
# for helping me understand how to send and receive messages over sockets.
# - admagulde

def format_message(text: str) -> tuple:
    """
    Formats a message to be sent over a socket connection.
    
    Parameters:
    text (str) The message to be sent.

    Returns:
    tuple (bytes, bytes) containing the header and the message with padding (body).
    """
    FOOTERSIZE = (16 - ((len(text) + HEADERSIZE) % 16)) % 16 # Padding to make sure the message is a multiple of 16 bytes

    msg = bytearray(text.encode('utf-8'))

    header = f"{(HEADERSIZE + len(msg) + FOOTERSIZE):<{HEADERSIZE}}" # Header containing the total length of the message

    return (bytes(header, 'utf-8'), msg + bytes((' ' * FOOTERSIZE), "utf-8")) # Return the header and the message with padding

def send_message(other: socket.socket, text: str):
    """
    Sends a message to a client socket.
    
    Parameters:
    client (socket.socket) The client socket to send the message to.
    text (str) The message to be sent.
    """
    header, body = format_message(text)
    other.send(header)
    other.send(body)

def receive_message(other: socket.socket) -> str:
    """
    Receives a message from a client socket.
    
    Parameters:
    client (socket.socket) The client socket to receive the message from.
    
    Returns:
    str representing the message received.
    """
    full_msg = bytearray(b'')
    new_msg = True
    while True:
        msg = other.recv(16)
        if new_msg:
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        full_msg.extend(msg)

        if len(full_msg) == msglen:
            return full_msg[HEADERSIZE:].decode("utf-8").strip()