import socket
import threading
import time
from networking import receive_message, send_message
from style import COLORS
from screenspace import notification, set_cursor_str
import random
import os

pad = 26
ln = 0
thread_list = {}

def print_nextln(msg):
    global ln
    ln = ln + 1
    thr_prefix = (thread_list[threading.current_thread().name] + threading.current_thread().name + COLORS.RESET + set_cursor_str(pad, ln + 1))
    print(thr_prefix + msg)
    threading.current_thread().native_id

def main():
    thread_list[threading.current_thread().name] = COLORS.YELLOW
    os.system('cls')
    cols = os.get_terminal_size().columns
    print("=" * int((cols/2 - 3)) + "CLIENT" + "=" * int((cols/2 - 3)))
    # Create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    s.connect(("localhost", 1234))

    # Start notification listener.
    client_addr = s.getsockname()
    client_ip, client_port = client_addr[0], client_addr[1]
    recv_thr = threading.Thread(target=notif_listener, args=(client_ip, client_port), daemon=True)
    recv_thr.start()
    
    # Send a message
    send_message(s, "Hello, server, this is client!")
    
    # Receive a message
    msg = receive_message(s)
    print_nextln(f"Received message: {msg}")
    
    # Close the socket
    # s.close()
    
    print_nextln("Sending another message.")
    send_message(s, 'Another message.')
    recv_thr.join()


def notif_listener(ip: str, port:int):
    thread_list[threading.current_thread().name] = COLORS.BLUE

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, port+1))
    s.listen(1)
    print_nextln("Listening for connections...")

    server_sock, server_addr = s.accept()
    server_ip, server_port = server_addr[0], server_addr[1]

    print_nextln(f"Connection received from {server_ip}:{server_port}")
    while True:
        msg = receive_message(server_sock)
        # notif = notification(msg, 1, COLORS.RED)
        if msg: break
    print_nextln(COLORS.RED + msg + COLORS.RESET)

if __name__ == "__main__":
    main()