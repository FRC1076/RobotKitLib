import pikitlib

import time
from networktables import NetworkTables
# To see messages from networktables, you must setup logging
import logging
logging.basicConfig(level=logging.DEBUG)

#import robotmap

LEFT_HAND = 1
RIGHT_HAND = 0

class MyRobot(pikitlib.TimedRobot):
    def robotInit(self):
        """Robot initialization function"""
        # object that handles basic drive operations
        self.leftBackMotor = pikitlib.SpeedController(1)
        self.leftFrontMotor = pikitlib.SpeedController(0)
        self.rightBackMotor = pikitlib.SpeedController(2)
        self.rightFrontMotor = pikitlib.SpeedController(3)

        self.left = pikitlib.SpeedControllerGroup(self.leftBackMotor, self.leftFrontMotor)
        self.right = pikitlib.SpeedControllerGroup(self.rightBackMotor, self.rightFrontMotor )

        self.myRobot = pikitlib.DifferentialDrive(self.left, self.right)

        self.DEADZONE = 0.4

        self.buzz = pikitlib.IllegalBuzzer()

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
        self.right.setInverted(False)
        
    def deadzone(self, val, deadzone):
        if abs(val) < deadzone:
            return 0
        return val

    def teleopPeriodic(self):
        
        forward = self.driver.getX(LEFT_HAND)
        forward = 0.80 * self.deadzone(forward, 0.2)
        rotation_value = -0.8 * self.driver.getY(RIGHT_HAND)
        self.myRobot.arcadeDrive(forward,rotation_value)

if __name__ == "__main__":
    pikitlib.run(MyRobot)
    