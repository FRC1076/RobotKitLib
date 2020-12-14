import socket
import threading


import buffer
import os

import argparse
import sys
import logging

import subprocess

SEPARATOR = "/"
BUFFER_SIZE = 4096 

parser = argparse.ArgumentParser()
parser.add_argument("ip_addr", help="IP address of the server")
args = parser.parse_args()
host = args.ip_addr

port = 2345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

with s:
    sbuf = buffer.Buffer(s)

    hash_type = "abc"

    dir = os.getcwd()
    dir.split("/")

    if os.name == 'nt':
        try:
            # Note: this line will show an error on *nix machines, can be safely ignored
            p = subprocess.Popen(['C:\Program Files\Git\\bin\\bash.exe','-c',"./create_archive.sh"], stdout=subprocess.PIPE)
        except Exception as e:
            print(e)
            print("ERROR: Git Bash not installed")
            sys.exit()
    else:
        p = subprocess.Popen("./create_archive.sh", stdout=subprocess.PIPE)
    
    out, err = p.communicate()

    file_name = out.decode('utf-8').split('\n')[0] + ".tar.gz"
    print(file_name)
    
    
    sbuf.put_utf8(hash_type)
    sbuf.put_utf8(file_name)

    file_size = os.path.getsize(file_name)
    sbuf.put_utf8(str(file_size))

    with open(file_name, 'rb') as f:
        sbuf.put_bytes(f.read())
    print('File Sent')