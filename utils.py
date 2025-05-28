# Loading animation function
import itertools
import sys
import time
loading = True
def loading_animation():
    for frame in itertools.cycle(['|', '/', '-', '\\']):
        if not loading:
            break
        sys.stdout.write(f'\rLoading {frame}')
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rLoading complete!     \n')

import socket
import modules_directory.inventory as inv
class Client:
    def __init__(self, socket: socket.socket, id: int, name: str, inventory_object: inv.Inventory):
        self.socket = socket
        self.id = id
        self.name = name
        self.inventory = inventory_object
        self.can_roll = True
        self.num_rolls = 0
        self.terminal_statuses = ["ACTIVE", "ACTIVE", "ACTIVE", "ACTIVE"]
        self.trades = [{"name":"", "properties":[]}, {"name":"", "properties":[]}, {"name":"", "properties":[]}] # List of trades for this player
        self.PlayerObject = None # Player object for this client