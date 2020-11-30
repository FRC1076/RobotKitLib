import socket
import threading


import buffer
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

port = 5001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

with s:
    sbuf = buffer.Buffer(s)

    hash_type = input('Enter hash type: ')

    files = input('Enter file(s) to send: ')
    files_to_send = files.split()

    for file_name in files_to_send:
        print(file_name)
        sbuf.put_utf8(hash_type)
        sbuf.put_utf8(file_name)

        file_size = os.path.getsize(file_name)
        sbuf.put_utf8(str(file_size))

        with open(file_name, 'rb') as f:
            sbuf.put_bytes(f.read())
        print('File Sent')