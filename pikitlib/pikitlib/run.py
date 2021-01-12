import sys
import logging
from .buffer import Buffer
import argparse
import os
import subprocess
import socket
from platform import uname
def run(robot_class):
    """
    """

    # sanity check
    if not hasattr(robot_class, "robotInit"):
        print("ERROR: run() must be passed a robot class!")
        sys.exit()

    parser = argparse.ArgumentParser()
    parser.add_argument("--action", help="deploy, update")

    parser.add_argument("--ip_addr", help="IP address of the server")
    args = parser.parse_args()
    action = args.action
    host = args.ip_addr

    if action is not None:
        if args.ip_addr == None:
            print("ERROR: enter ip address with --ip_addr IP_OF_ROBOT")
            sys.exit()
        else:
            deploy(host)

    

        
def deploy(h):
    host = h
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

        cmd = """dirname=$(pwd)
            cd ..
            shopt -s extglob           
            result=${dirname%%+(/)}    
            result=${result##*/}       
            printf '%s\n' "$result"
            tar --exclude='.git' -cvf $result.tar.gz -C $result .
            cp $result.tar.gz $result/$result.tar.gz
            rm $result.tar.gz
            cd $result
            echo $result"""

        if os.name == 'nt':
            try:
                # Note: this line will show an error on *nix machines, can be safely ignored
                
                p = subprocess.Popen(['C:\Program Files\Git\\bin\\bash.exe','-c',cmd], stdout=subprocess.PIPE)
            except Exception as e:
                print(e)
                print("do you have git bash installed?")
                sys.exit()
        else:
            p = subprocess.Popen(["sh", "-c", cmd], stdout=subprocess.PIPE)
        
        out, err = p.communicate()

        file_name = out.decode('utf-8').split('\n')[0] + ".tar.gz"
        print(file_name)
        
        
        sbuf.put_utf8(hash_type)
        sbuf.put_utf8(file_name)

        file_size = os.path.getsize(file_name)
        sbuf.put_utf8(str(file_size))

        with open(file_name, 'rb') as f:
            sbuf.put_bytes(f.read())

        os.system("rm RobotCode.tar.gz")

        print('File Sent')

    