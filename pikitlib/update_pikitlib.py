import sys
import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument("ip_addr", help="IP address of the robot")
args = parser.parse_args()
host = args.ip_addr


os.system("scp pikitlib/*.py pi@" + host + ":/home/pi/.local/lib/python3.7/site-packages/pikitlib")
os.system("ssh pi@" + host  + " 'sudo systemctl daemon-reload'")
os.system("ssh pi@" + host  + " 'sudo service robotrunner restart'")