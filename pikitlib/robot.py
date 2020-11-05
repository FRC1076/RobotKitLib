import pikitlib
import time
from networktables import NetworkTables
# To see messages from networktables, you must setup logging
import logging
logging.basicConfig(level=logging.DEBUG)

import robotmap


class MyRobot():
    def robotInit(self):
        """Robot initialization function"""
        # object that handles basic drive operations
        self.leftBackMotor = pikitlib.SpeedController(robotmap.BACK_LEFT)
        self.leftFrontMotor = pikitlib.SpeedController(robotmap.FRONT_LEFT)
        self.rightBackMotor = pikitlib.SpeedController(robotmap.BACK_RIGHT)
        self.rightFrontMotor = pikitlib.SpeedController(robotmap.FRONT_RIGHT)

        self.left = pikitlib.SpeedControllerGroup(self.leftBackMotor, self.leftFrontMotor)
        self.right = pikitlib.SpeedControllerGroup(self.rightBackMotor, self.rightFrontMotor )

        self.myRobot = pikitlib.DifferentialDrive(self.left, self.right)
       # self.myRobot.setExpiration(0.1)

        self.DEADZONE = 0.4

        #self.buzz = pikitlib.IllegalBuzzer()

        NetworkTables.initialize()
        self.driver = pikitlib.XboxController(0)

    def autonomousInit(self):
        self.myRobot.tankDrive(0.8, 0.8)

    def autonomousPeriodic(self):
        self.myRobot.tankDrive(1, 0.5)

        buttonAPressed = self.driver.getAButtonPressed()
        if buttonAPressed:
            logging.debug('AButton has been pressed')
        buttonAReleased = self.driver.getAButtonReleased()
        if buttonAReleased:
            logging.debug('AButton has been released')
        buttonA = self.driver.getAButton() 
        if buttonA:
            logging.debug('AButton is DOWN on controller 0')
        else:
            logging.debug('AButton is UP on controller 0')
    

    def teleopInit(self):
        """
        Configures appropriate robot settings for teleop mode
        """
        self.left.setInverted(True)
        self.right.setInverted(True)
        
    def deadzone(self, val, deadzone):
        if abs(val) < deadzone:
            return 0
        return val

    def teleopPeriodic(self):
        #forward = -self.driver.getRawAxis(5) 
        #rotation_value = rotation_value = self.driver.getX(LEFT_HAND)
        
        # Test controller
        
        forward = self.driver.getX(0)
        forward = 0.80 * self.deadzone(forward, robotmap.DEADZONE)
        rotation_value = -0.8 * self.driver.getY(1)
        self.myRobot.arcadeDrive(forward,rotation_value)


        """
        forward = 0.7
        rotation_value = 0.2


        forward = self.deadzone(forward, 0.5)

        self.myRobot.arcadeDrive(forward, rotation_value)"""
