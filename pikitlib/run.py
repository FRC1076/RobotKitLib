# python run.py robot.py


#General Imports
import sys
import time
import threading

#Robot
import robot
import pikitlib
from networktables import NetworkTables



#Networking and Logging
import logging
import logging.handlers


logging.basicConfig(level=logging.DEBUG)



class main():
    def __init__(self):
        """
        Construct robot disconnect, and powered on
        """
        self.r = robot.MyRobot()
        self.current_mode = ""
        self.disabled = True
        

        self.timer = pikitlib.Timer()

        

        
    def connect(self):
        """
        Connect to robot NetworkTables server
        """
        NetworkTables.initialize()
        NetworkTables.addConnectionListener(self.connectionListener, immediateNotify=True)


    def connectionListener(self, connected, info):
        """
        Setup the listener to detect any changes to the robotmode table
        """
        #print(info, "; Connected=%s" % connected)
        logging.info("%s; Connected=%s", info, connected)
        sd = NetworkTables.getTable("RobotMode")
        sd.addEntryListener(self.valueChanged)

    def setupLogging(self):
        rootLogger = logging.getLogger('')
        rootLogger.setLevel(logging.DEBUG)
        socketHandler = logging.handlers.SocketHandler(str(NetworkTables.getRemoteAddress()),
            logging.handlers.DEFAULT_TCP_LOGGING_PORT)
        
        rootLogger.addHandler(socketHandler)


   
    def valueChanged(self, table, key, value, isNew):
        """
        Check for new changes and use them
        """
        #print("valueChanged: key: '%s'; value: %s; isNew: %s" % (key, value, isNew))
        if(key == "Mode"):
            self.setupMode(value)
        if(key == "Disabled"):
            self.disabled = value
        
    def start(self):    
        self.r.robotInit()
        self.rl = threading.Thread(target=self.robotLoop)
        self.rl.start()
        if self.rl.is_alive():
            logging.debug("Main thread created")

    def setupMode(self, m):
        """
        Run the init function for the current mode
        """
        #self.rl._stop()
        
        if m == "Teleop":
            self.r.teleopInit()
        elif m == "Auton":
            self.r.autonomousInit()

        self.current_mode = m
       
        #self.rl.start()

    def auton(self):
        self.r.autonomousPeriodic()

    def teleop(self):
        self.r.teleopPeriodic()
        
    def disable(self):
        m1 = pikitlib.SpeedController(0)
        m2 = pikitlib.SpeedController(2)
        m3 = pikitlib.SpeedController(4)
        m4 = pikitlib.SpeedController(6)
        m = pikitlib.SpeedControllerGroup(m1,m2,m3,m4)
        m.set(0)

    def mainLoopThread(self):
        """
        Loop the mode function
        """
        while True:
            if self.disabled:
                self.disable()
                #self.rl._stop()
                    
            time.sleep(0.02)

    def quit(self):
        logging.info("Quitting...")
        self.disable()
        sys.exit()
            
    def robotLoop(self):
        while True:
            if not self.disabled:
                self.timer.start()
                if self.current_mode == "Auton":
                    self.auton()
                elif self.current_mode == "Teleop":
                    self.teleop()
                self.timer.stop()
                ts = 0.02 -  self.timer.get()
                self.timer.reset()
                if ts < -0.5:
                    logging.critical("Program taking too long!")
                    self.quit()
                elif ts < 0:
                    logging.warning("%s has slipped by %s miliseconds!", self.current_mode, ts * -1000)
                else:        
                    time.sleep(ts)
            else:
                self.rl._stop
            

    def debug(self):
        self.disabled = False
        self.start()
        self.setupMode("Teleop")
        self.mainLoopThread()

    
            





if __name__ == "__main__":
    
    m = main()
    m.connect()
    m.start()
    try:
        m.mainLoopThread()
    except KeyboardInterrupt:
        m.quit()
    #x = threading.Thread(target=m.mainLoopThread)
    #x.start()
    #m.debug()

    
