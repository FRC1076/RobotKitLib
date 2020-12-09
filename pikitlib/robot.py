import pikitlib
import time
from networktables import NetworkTables
# To see messages from networktables, you must setup logging
import logging
logging.basicConfig(level=logging.DEBUG)

import robotmap

LEFT_HAND = 1
RIGHT_HAND = 0

class MyRobot():
    def robotInit(self):
        """Robot initialization function"""
        # object that handles basic drive operations
        self.leftBackMotor = pikitlib.SpeedController(robotmap.BACK_LEFT)
        self.leftFrontMotor = pikitlib.SpeedController(robotmap.FRONT_LEFT)
        self.rightBackMotor = pikitlib.SpeedController(robotmap.BACK_RIGHT)
        self.rightFrontMotor = pikitlib.SpeedController(robotmap.FRONT_RIGHT)

        self.myRobot = pikitlib.MecanumDrive(self.frontleft, self.frontright, self.rearleft, self.rearright)
       # self.myRobot.setExpiration(0.1)

        self.DEADZONE = 0.4

        #self.buzz = pikitlib.IllegalBuzzer()

        NetworkTables.initialize()
        self.driver = pikitlib.XboxController(0)

    def autonomousInit(self):
        self.myRobot.tankDrive(0.8, 0.8)

    def autonomousPeriodic(self):
        self.myRobot.tankDrive(1, 0.5)

    def teleopInit(self):
        """
        Configures appropriate robot settings for teleop mode
        """
        self.left.setInverted(False)
        self.right.setInverted(True)
        
    def deadzone(self, val, deadzone):
        if abs(val) < deadzone:
            return 0
        return val

    def teleopPeriodic(self):
        
        xspeed = self.driver.getx(LEFT_HAND)
        xspeed = 0.80 * self.deadzone(xspeed, robotmap.DEADZONE)
        yspeed = self.driver.gety(LEFT_HAND)
        yspeed = 0.80 * self.deadzone(yspeed, robotmap.DEADZONE)
        zRotation = -0.8 * self.driver.getY(RIGHT_HAND)
        self.myRobot.tankDrive(left,right)
