import socket
import threading
import time
import networking as net
import os

def main():
    os.system('cls')
    cols = os.get_terminal_size().columns
    print("=" * int((cols/2 - 3)) + "SERVER" + "=" * int((cols/2 - 3)))
    # Create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    s.bind(('localhost', 1234))
    
    s.listen(1)
    print("Listening for connections...")

    client_socket, client_addr = s.accept()
    client_ip, client_port = client_addr[0], client_addr[1]

    print(f"Connection received from {client_ip}:{client_port}")
    print("Waiting for messages...")

    msg = net.receive_message(client_socket)
    print(f"Received message: {msg}")
    
    # Send a message
    net.send_message(client_socket, "Hello, client, this is server!")
    

    print(f"client_socket peername: {client_socket.getpeername()}")
    print(f"client_socket sockname: {client_socket.getsockname()}")
    # Send a notification
    net.send_notif(client_socket, "This is a notification.")
    
    # Close the socket
    # s.close()

    print(net.receive_message(client_socket))

if __name__ == "__main__":
    main()