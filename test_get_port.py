import subprocess
import random
def select_open_port_and_address():
    addresses = []
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
            if int(port) > 49151 and '[' not in address and '0.0.0.0' not in address:
                addresses.append(address)
                ports.append(port)
    #random select
    rolled_index = random.randint(0, len(addresses)-1)
    return addresses[rolled_index], ports[rolled_index]
#if __name__ == '__main__':
 #   print(select_open_port_and_address())
