import sys
import logging
from pikitlib.buffer import Buffer
import argparse
import os
import subprocess
import socket

parser = argparse.ArgumentParser()
parser.add_argument("ip_addr", help="IP address of the robot")
args = parser.parse_args()
host = args.ip_addr
port = 2345



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((host, port))
except ConnectionRefusedError:
    logging.error("Cannnot connect to robot")
    logging.error("Is the robot running, or do you have the right ip?")
    sys.exit()


with s:
    sbuf = Buffer(s)

    hash_type = "abc"

    dir = os.getcwd()
    dir.split("/")


    p = subprocess.Popen(["python", "setup.py", "bdist"], stdout=subprocess.PIPE)
    
    out, err = p.communicate()
    
    file_name = os.listdir("dist")[0]
    print(file_name)
    os.system("cp dist/" + file_name + " " + file_name)
    
    sbuf.put_utf8(hash_type)
    sbuf.put_utf8(file_name)

    file_size = os.path.getsize(file_name)
    sbuf.put_utf8(str(file_size))

    with open(file_name, 'rb') as f:
        sbuf.put_bytes(f.read())

    print('File Sent')
