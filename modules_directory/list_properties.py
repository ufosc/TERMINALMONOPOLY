from style import MYCOLORS as COLORS, graphics as g
import screenspace as ss
from socket import socket

name = "Properties List"
author = "https://github.com/adamgulde"
version = "1.1" # Moved to its own file
command = "list"
help_text = "Type LIST to view all properties on the board. View property deed details."
persistent = False
    
def run(player_id:int, server: socket, active_terminal: ss.Terminal):
    """
    Lists all properties on the board by calling the property list stored in graphics.
    
    Parameters: None
    Returns: None
    """
    active_terminal.persistent = persistent
    ret_val = ""
    props = g.get('properties').split('\n')
    for prop in props:
        if prop == '': 
            ret_val += ' '.center(75) + '\n' 
            continue
        first_word = prop.split()[0]
        color = getattr(COLORS, first_word.upper(), COLORS.RESET)
        prop = prop.replace(first_word, "")
        centered_prop = prop.center(75)
        ret_val +=color+ centered_prop + COLORS.RESET + '\n'
    active_terminal.update(ret_val, padding=False)