import pikitlib
import time
from networktables import NetworkTables
# To see messages from networktables, you must setup logging
import logging
logging.basicConfig(level=logging.DEBUG)

import robotmap

LEFT_HAND = 0
RIGHT_HAND = 1

class MyRobot(pikitlib.TimedRobot):
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
        self.us = pikitlib.Ultrasonic()

        NetworkTables.initialize()
        self.driver = pikitlib.XboxController(0)

        self.us.startUltrasonic()

    def autonomousInit(self):
        self.timer = pikitlib.Timer()
        self.timer.start()


    def autonomousPeriodic(self):
        print(self.us.get())
        print(self.timer.get())
        if self.timer.get() < 2.0:
            self.myRobot.arcadeDrive(0.6, 0)
        elif self.timer.get() < 3.0:
            self.myRobot.arcadeDrive(0, 0.8)
        elif self.timer.get() < 4.0:
            self.myRobot.arcadeDrive(-0.7, 0)
        elif self.timer.get() < 7.0:
            self.myRobot.arcadeDrive(0, -0.8)
        else:
            self.myRobot.arcadeDrive(0,0)



    def teleopInit(self):
        """
        Configures appropriate robot settings for teleop mode
        """
        self.left.setInverted(False)
        self.right.setInverted(False)
        
    def deadzone(self, val, deadzone):
        if abs(val) < deadzone:
            return 0
        return val

    def teleopPeriodic(self):
        
        forward = self.driver.getY(LEFT_HAND)
        forward = 0.80 * self.deadzone(forward, robotmap.DEADZONE)

        if self.driver.getAButton():
            forward = forward * 0.5

        
        
        rotation_value = -0.8 * self.driver.getX(RIGHT_HAND)
        print("Forward: " + str(forward) + " Rotate: " + str(rotation_value))
        self.myRobot.arcadeDrive(forward, rotation_value)

if __name__ == "__main__":
    pikitlib.run(MyRobot)

