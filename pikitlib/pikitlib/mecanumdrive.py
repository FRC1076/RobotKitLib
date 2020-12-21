from .speedcontroller import SpeedController
from .robotdrivebase import RobotDriveBase

import math

class MecanumDrive(RobotDriveBase):

    def __init__(self, frontleft: SpeedController, frontright: SpeedController, backleft: SpeedController, backright: SpeedController):
        self.frontleft = frontleft
        self.frontright = frontright
        self.rearleft = backleft
        self.rearright = backright
        self.rightSideInvertMultiplier = -1.0
        RobotDriveBase.__init__(self)
    
    def driveCartesianA(self, xspeed: float, yspeed: float, zRotation: float, squareInputs: bool = True) -> None:

        xspeed = RobotDriveBase.limit(xspeed)
        xspeed = RobotDriveBase.applyDeadband(xspeed, self.deadband)

        yspeed = RobotDriveBase.limit(yspeed)
        yspeed = RobotDriveBase.applyDeadband(yspeed, self.deadband)

        if squareInputs:
            # Square the inputs (while preserving the sign) to increase fine
            # control while permitting full power.
            xspeed = math.copysign(xspeed * xspeed, xspeed)
            yspeed = math.copysign(yspeed * yspeed, yspeed)
            zRotation = math.copysign(zRotation * zRotation, zRotation)
        
        wheelSpeeds = [
            # Front Left
            input.x + input.y + zRotation,
            # Rear Left
            -input.x + input.y + zRotation,
            # Front Right
            -input.x + input.y - zRotation,
            # Rear Right
            input.x + input.y - zRotation,
        ]

        RobotDriveBase.normalize(wheelSpeeds)

        wheelSpeeds = [speed * self.maxOutput for speed in wheelSpeeds]

        self.frontleft.set(wheelSpeeds[0])
        self.rearleft.set(wheelSpeeds[1])
        self.frontright.set(wheelSpeeds[2] * self.rightSideInvertMultiplier)
        self.rearright.set(wheelSpeeds[3] * self.rightSideInvertMultiplier)

    def driveCartesianB(self, xspeed: float, yspeed: float, zRotation: float, squareInputs: bool = True) -> None:
        
        xspeed = RobotDriveBase.limit(xspeed)
        xspeed = RobotDriveBase.applyDeadband(xspeed, self.deadband)

        yspeed = RobotDriveBase.limit(yspeed)
        yspeed = RobotDriveBase.applyDeadband(yspeed, self.deadband)

        if squareInputs:
            # Square the inputs (while preserving the sign) to increase fine
            # control while permitting full power.
            xspeed = math.copysign(xspeed * xspeed, xspeed)
            yspeed = math.copysign(yspeed * yspeed, yspeed)
            zRotation = math.copysign(zRotation * zRotation, zRotation)

        rads = math.atan2(yspeed, xspeed)

        diag0 = math.sin(rads - (1/4 * math.pi)) * math.hypot(xspeed, yspeed) + zRotation
        diag1 = math.sin(rads + (1/4 * math.pi)) * math.hypot(xspeed, yspeed) + zRotation

        diag0 *= self.maxOutput
        diag1 *= self.maxOutput

        self.frontleft.set(diag1)
        self.rearleft.set(diag0)
        self.frontright.set(diag0 * self.rightSideInvertMultiplier)
        self.rearright.set(diag1 * self.rightSideInvertMultiplier)