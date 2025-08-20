HEADERSIZE = 10 # Max length of the header, meaning the max length of the message is 10^10 bytes
import socket
import threading
from collections import deque
player_mtrw = False # Store here if the player associated with this script is waiting on messages in their main thread

# OOF message routing system
oof_message_queue = deque()  # Queue for OOF-tagged messages
oof_queue_lock = threading.Lock()  # Thread-safe access to the queue

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

def send_message(other: socket.socket, text: str) -> None:
    """
    Sends a message to a client socket.
    
    Parameters:
        client (socket.socket) The client socket to send the message to.
        text (str) The message to be sent.

    Returns:
        None
    """
    header, body = format_message(text)
    other.send(header)
    other.send(body)

def send_notif(other: socket.socket, text: str, header: str="NOTF:") -> None:
    """
    Sends a notification to a client socket. This is sent to the client's 
    second socket, which is used for notifications only. This socket is
    always listening for notifications and does not send any data back.
    Notifications are NOT activeterminal-based.
    
    Parameters:
        client (socket.socket) The client socket to send the notification to.
        text (str) The notification to be sent.
        header (str) The header for the type of notification
    
    Returns:
        None
    """
    other_address, other_port = other.getpeername()
    
    # Create a new socket
    new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the port 1 above the normal port of "other"
    new_port = other_port + 1
    new_socket.connect((other_address, new_port))
    
    # Send the message
    send_message(new_socket, header + f"{text}")
    
    # Close the new socket
    new_socket.close()

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
            message = full_msg[HEADERSIZE:].decode("utf-8").strip()
            
            # Check if this is an OOF-tagged response
            if message.startswith("OOF:"):
                # Add to OOF queue and return empty string to caller
                with oof_queue_lock:
                    oof_message_queue.append(message[4:])  # Remove "OOF:" prefix
                return ""  # Return empty to indicate this was handled
            
            return message

def send_oof_message(other: socket.socket, text: str) -> None:
    """
    Sends an OOF-tagged message to the server.
    
    Parameters:
        other (socket.socket): The server socket to send the message to.
        text (str): The message to be sent (will be prefixed with "OOF:").
        
    Returns:
        None
    """
    send_message(other, f"OOF:{text}")

def receive_oof_message() -> str:
    """
    Receives the next OOF message from the queue.
    
    Returns:
        str: The OOF message, or empty string if none available.
    """
    with oof_queue_lock:
        if oof_message_queue:
            return oof_message_queue.popleft()
    return ""

def has_oof_messages() -> bool:
    """
    Check if there are pending OOF messages in the queue.
    
    Returns:
        bool: True if there are OOF messages waiting.
    """
    with oof_queue_lock:
        return len(oof_message_queue) > 0