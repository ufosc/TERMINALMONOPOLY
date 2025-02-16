import subprocess
import random
import socket
def get_open_ports():
    host = socket.gethostname()
    ports = []
    #get all the ports
    result = subprocess.run(['netstat', '-an'], capture_output=True, text=True)
    #print(result.stdout)
    for line in result.stdout.splitlines():
        #get open ports
        if "LISTENING" in line:
            address = line.split()[1].split(':')[0]
            port = line.split()[1].split(":")[-1]
            #if within the free use range and not a duplicate address (has the [::]) or offline (0.0.0.0)
            if 49151 < int(port) and '[' not in address and not '0.0.0.0' in address:
                ports.append(port)
    #random select
    #rolled_index = random.randint(0, len(addresses)-1)
    return ports
if __name__ == '__main__':
    print(get_open_ports())

