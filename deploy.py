import socket
import threading


import buffer
import os

import argparse
import sys
import logging

import subprocess

"""
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

    
    #TODO: create archive, send it

    
    dir = os.getcwd()
    dir.split("/")

    #os.system("create_archive.sh")
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
"""

SEPARATOR = "/"
BUFFER_SIZE = 4096 

class Sender():

    def __init__(self, ip):
        
        self.host = ip

        self.port = 2345
    
    def connect(self):
        self.s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))

    def sendFile(self):
        with self.s:
            sbuf = buffer.Buffer(self.s)

            hash_type = "abc"
            
            dir = os.getcwd()
            dir.split("/")

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
            print(err)