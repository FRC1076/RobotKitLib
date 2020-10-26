# python run.py robot.py

import sys
import robot
import time
from networktables import NetworkTables
import threading
import logging


logging.basicConfig(level=logging.DEBUG)

ip = "10.10.10.10" #ip address

class main():
    def __init__(self):
        self.r = robot.MyRobot()
        self.connected = False

        #Disabled/Auton/Teleop
        self.current_mode = "Disabled"
        
    #inital connection to networktable, check for updates
    def connect(self):
        NetworkTables.initialize(server=ip)
        NetworkTables.addConnectionListener(self.connectionListener, immediateNotify=True)

        sd = NetworkTables.getTable("RobotMode")
        sd.addEntryListener(self.valueChanged)

    
    def connectionListener(self, connected, info):
        print(info, "; Connected=%s" % connected)
        self.connected = True

    #Print the values changed in the network table
    def valueChanged(self, table, key, value, isNew):
        print("valueChanged: key: '%s'; value: %s; isNew: %s" % (key, value, isNew))
        if(key == "Mode"):
            self.setupMode(value)
        
    def start(self):    
        self.r.robotInit()

    def setupMode(self, m):
        self.current_mode = m

        if m == "Teleop":
            self.r.teleopInit()
        elif m == "auton":
            self.r.autonomousInit()

    def auton(self):
        self.r.autonomousPeriodic
        time.sleep(0.02)

    def teleop(self):
        self.r.teleopPeriodic()
        time.sleep(0.02)

    def mainLoopThread(self):
        while self.current_mode != "Disabled":
            if self.current_mode == "Auton":
                self.auton()
            elif self.current_mode == "Teleop":
                self.teleop()
            





if __name__ == "__main__":
    m = main()
    m.connect()

    x = threading.Thread(target=m.mainLoopThread)
    x.start()


    
