from socket import socket
import os
import importlib
import textwrap
from utils.screenspace import MYCOLORS as c, Terminal, overwrite

name = "Help List"
author = "https://github.com/narcistiq"
command = "help"
persistent = False
    
def run(player_id:int, server: socket, active_terminal: Terminal, param):
    """
    Show all help text located in each module.
    
    Parameters: None
    Returns: None
    """
    active_terminal.persistent = persistent
    help = get_module_text()
    module = param[0]
    module_text = f"=== HELP | {module.upper()} ==="
    module_text = "\n" + module_text.center(75) + "\n"
    module_text += "\n" + "-"*75 + "\n"

    overwrite(c.RESET+"\r" + " " * 40)
    if(module not in help.keys()):
        overwrite(c.RESET + c.RED + f"\r{module.upper()} help text not found.")
        return
    else:
        lines = textwrap.wrap(help[module], 70)
        pages = [lines[i:i+15] for i in range(0, len(lines), 15)] # TODO: Should perform extra checks for newline characters for better formatting
        if(len(pages) > 1):    
            overwrite(c.RESET + c.YELLOW + f"\rModule has {len(pages)} help pages available. Type `help <module> <page #>` for more information.")
        if(len(param) == 2):    # if page_num is provided
            page_num = int(param[1])
            if not(param[1].isdigit()):
                overwrite(c.RESET + c.RED + "\rInvalid parameter. Type `help <module> <page #>` for more information.")
                return
            elif(page_num < 1 or page_num > len(pages)):
                overwrite(c.RESET + c.RED + f"\r{module.upper()} help does not have page {int(param[1])}! Please select another page number.")
                return
            else:
                page = pages[page_num - 1]
                module_text += "\n".join(line.center(75) for line in page)
        else:   # just display the first page
            module_text += "\n".join(line.center(75) for line in pages[0])
        active_terminal.clear()
        active_terminal.update(module_text, padding=False)

def get_module_text() -> dict: 
    """
    Retrieves a list of available module commands and their corresponding functions.
    This function scans the "modules_directory" for Python files, dynamically
    imports each module, and checks if the module has a 'command' and 'help_text' attribute.
    If the attributes exist, the command and its corresponding function are added
    to the dictionary.
    
    Returns:
        dict: A dictionary mapping module commands to their corresponding functions.
    """
    pairs = {}
    for file in os.listdir("modules_directory"):
        if file.endswith(".py"):
            file = file[:-3]
            module = importlib.import_module("modules_directory." + file)
            if hasattr(module, 'help_text'): # Check if the module has 'command' and 'help_text' attributes
                pairs[module.command] = module.help_text # Add the command and its corresponding module to the dictionary
    return pairs