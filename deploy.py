import socket
import tqdm
import os
import argparse
import sys
import logging

SEPARATOR = "/"
BUFFER_SIZE = 4096 

parser = argparse.ArgumentParser()
parser.add_argument("ip_addr", help="IP address of the server")
args = parser.parse_args()
host = args.ip_addr

#host = "localhost"

port = 5001

filename = "robot.py"

try:
    filesize = os.path.getsize(filename)
except FileNotFoundError:
    logging.critical("ERROR: " + filename + " not found!")
    sys.exit()

s = socket.socket()

print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")

s.send(f"{filename}{SEPARATOR}{filesize}".encode())

progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    for _ in progress:
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            break

        s.sendall(bytes_read)

        progress.update(len(bytes_read))

s.close()