#This will pull all the ips from an ifconfig

#!/bin/python3

import re
import subprocess

def get_ipv4_addresses():
    # Run ifconfig command and capture its output
    output = subprocess.check_output(['ifconfig']).decode('utf-8')

    # Define regex pattern to match IPv4 addresses
    pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'

    # Find all matches of IPv4 addresses in the output
    ipv4_addresses = re.findall(pattern, output)

    return ipv4_addresses

if __name__ == "__main__":
    ipv4_addresses = get_ipv4_addresses()
    print("IPv4 Addresses found:")
    for address in ipv4_addresses:
        print(address)
