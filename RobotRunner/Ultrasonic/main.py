#Ultrasonic process that handels all ultrasonic  things, then posts to a socket

import ultrasonic
import socket
import time
import pikitlib

u = ultrasonic()
s = socket.socket()
host = 'localhost'
port = 1235
s.connect((host,port))


starttime = time.time()
while True:
    val = u.getRangeInches()
    time.sleep(2 - ((time.time() - starttime) % 2))