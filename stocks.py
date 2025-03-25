from time import sleep
from style import COLORS as c
import screenspace as ss
from screenspace import Terminal
import os
import networking
import stock_market as sm
from socket import socket

module_name = "Stocks"
module_command = "stocks"
module_description = "Welcome to The Market!"

def module(socket: socket, active_terminal: Terminal, pid: int, name: str):
    """
    Stocks Module
    Author: Hiral Shukla (github.com/hiralshukla)
    Author: Shan Sundal (github.com/ssundal)
    Version: 2.0 - Revised to use network commands and print to screen
    Welcome to The Market!

    """



    active_terminal.update("\033[0m     stocks loading...", padding=False)
    sm.market = sm.stock_market()
    sm.market.add_stock("PLZA", 20.00, -5, 5)
    sm.market.add_stock("FISH", 20.00, -5, 5)
    sm.market.add_stock("RCKT", 20.00, -5, 5)
    sm.market.add_stock("BLVD", 5.00, -10, 10)
    sm.market.add_stock("TRIS", 5.00, -10, 10)
    sm.market.add_stock("UTIL", 5.00, -10, 10)
    sm.market.add_stock("DRVE", 0.010, -15, 15)
    sm.market.add_stock("CYBR", 0.010, -15, 15)
    sm.market.add_stock("SYNC", 0.010, -15, 15)

    active_terminal.update(f"welcome {name}!")




if __name__ == "__main__":
    module(1)