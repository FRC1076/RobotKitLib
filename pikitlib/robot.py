import pikitlib
import time
import random
from networktables import NetworkTables
# To see messages from networktables, you must setup logging
import logging
logging.basicConfig(level=logging.DEBUG)

import robotmap

LEFT_HAND = 1
RIGHT_HAND = 0

MOVE_OUT = 0
REST_OUT = 1
MOVE_BACK = 2
REST_BACK = 3

ARCADE = 0
TANK = 1

PHASE_LENGTH = 1.0

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

        self.drive_train = pikitlib.DifferentialDrive(self.left, self.right)
       # self.drive_train.setExpiration(0.1)

        self.DEADZONE = 0.4

        #self.buzz = pikitlib.IllegalBuzzer()

        NetworkTables.initialize()
        self.driver = pikitlib.XboxController(0)
        self.drive_style = TANK

    def autonomousInit(self):
        self.rr_phase = REST_BACK # will transition to MOVE_OUT right away
        self.update_state()

    def autonomousPeriodic(self):
        print('autonPeriodic')
        self.random_robot()

    def teleopInit(self):
        """
        Configures appropriate robot settings for teleop phase
        """
        print('teleopInit')
        self.left.setInverted(False)
        self.right.setInverted(False)
        
    def deadzone(self, val, deadzone):
        if abs(val) < deadzone:
            return 0
        return val

    def teleopPeriodic(self):
        print('teleopPeriodic')

        if self.drive_style == ARCADE:
            forward = self.driver.getX(LEFT_HAND)
            forward = 0.80 * self.deadzone(forward, robotmap.DEADZONE)
            rotation_value = -0.8 * self.driver.getY(RIGHT_HAND)
            self.drive_train.arcadeDrive(forward,rotation_value)
        
        else: # drive_style == TANK      
            left = self.driver.getY(LEFT_HAND)
            left = 0.80 * self.deadzone(left, robotmap.DEADZONE)
            right = self.driver.getY(RIGHT_HAND)
            right = 0.80 * self.deadzone(right, robotmap.DEADZONE)
            self.drive_train.tankDrive(left, -1.0 * right)



    def random_robot(self):
        '''
        phase_length: duration of move/rest phases in ms
        '''
        now = time.perf_counter()
        if now > self.rr_deadline:
            self.update_state()
        else:
            self.enact_state()

    def update_state(self):

        if self.rr_phase == MOVE_OUT:
            self.rr_phase = REST_OUT

        elif self.rr_phase == REST_OUT:
            self.rr_phase = MOVE_BACK
            self.rr_left = -1.0 * self.rr_left
            self.rr_right = -1.0 * self.rr_right

        elif self.rr_phase == MOVE_BACK:
            self.rr_phase = REST_BACK

        elif self.rr_phase == REST_BACK:
            self.rr_phase = MOVE_OUT
            self.rr_left = 1.0 - (random.random() / 2.0)
            self.rr_right = 1.0 - (random.random() / 2.0)
            if (random.random() > 0.5):
                self.rr_left = -1.0 * self.rr_left
                self.rr_right = -1.0 * self.rr_right

        self.rr_deadline = time.perf_counter() + 1.0

    def enact_state(self):
        if self.rr_phase == REST_BACK or self.rr_phase == REST_OUT:
            pass
            self.drive_train.tankDrive(0.0, 0.0)
        else:
            pass
            self.drive_train.tankDrive(self.rr_left, self.rr_right)
        print(self.rr_phase, self.rr_left, self.rr_right)
