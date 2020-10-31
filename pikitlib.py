#import Motor
from networktables import NetworkTables
import RPi.GPIO as GPIO
from PCA9685 import PCA9685
import enum


class XboxController():


    class Hand(enum.IntEnum):

        kLeft = 0
        kRight = 1
    
    class Button(enum.IntEnum):
        kBumperLeft = 4
        kBumperRight = 5
        kA = 0
        kB = 1
        kX = 2
        kY = 3
        kBack = 6
        kStart = 7
        kBig = 8

    def __init__(self, id):
        self.id = id
        self.nt = NetworkTables.getTable("DriverStation/XboxController{}".format(id))
        # must initialize the state of all controls here, because
        # if the first inquiry asks if a button was pressed, then
        # it has to know if the state has changed since the last
        # time...
        # get and save button state
        
        # A-0,B-1,X-2,Y-3

        # A, B, X, Y, L bumpter, R bumber, back, start, big shinny button
        self.buttons = [0,0,0,0,0,0,0,0]

        # LHand Y, LHand X, L trigger, RHand X, RHand Y, R trigger
        self.axis_values = [0,0,0,0,0,0]


        for i in range(len(self.buttons)):
            self.buttons[i] = self.nt.getNumberArray("Buttons", 0)[i]
        
        for j in range(len(self.axis_values)):
            self.axis_values[j] = self.nt.getNumberArray("Axis", 0)[j]


    def getRawButton(self, v) -> bool:
        newB = self.nt.getNumberArray("Buttons", 0)[v]
        self.buttons[v] = newB
        return newB

    def getRawButtonPressed(self, v) -> bool:
        newB = self.nt.getNumberArray("Buttons", 0)[v]
        pressed = newB and not self.buttons[v]
        self.buttons[v] = newB
        return pressed

    def getRawButtonReleased(self, v) -> bool:
        newB = self.nt.getNumberArray("Buttons", 0)[v]
        released =  not newB and self.buttons[v]
        self.buttons[v] = newB
        return released

    def getX(self, hand):
        """Get the x position of the controller.

        :param hand: which hand, left or right

        :returns: the x position
        """
        if hand == self.Hand.kLeft:
            self.axis_values[1] = self.nt.getNumberArray("Axis", 0)[1]
            return self.axis_values[1]
        else:
            self.axis_values[4] = self.nt.getNumberArray("Axis", 0)[4]
            return self.axis_values[4]

    def getY(self, hand):
        """Get the y position of the controller.

        :param hand: which hand, left or right

        :returns: the y position
        """
        if hand == self.Hand.kLeft:
            self.axis_values[0] = self.nt.getNumberArray("Axis", 0)[0]
            return self.axis_values[0]
        else:
            self.axis_values[3] = self.nt.getNumberArray("Axis", 0)[3]
            return self.axis_values[3]

    def getBumper(self, hand) -> bool:
        """Read the values of the bumper button on the controller.
        :param hand: Side of controller whose value should be returned.
        :return: The state of the button
        """
        if hand == GenericHID.Hand.kLeft:
            return self.getRawButton(self.Button.kBumperLeft)
        else:
            return self.getRawButton(self.Button.kBumperRight)

    def getBumperPressed(self, hand):
        """Whether the bumper was pressed since the last check.
        :param hand: Side of controller whose value should be returned.
        :returns: Whether the button was pressed since the last check.
        """
        if hand == self.Hand.kLeft:
            return self.getRawButtonPressed(self.Button.kBumperLeft)
        else:
            return self.getRawButtonPressed(self.Button.kBumperRight)
    
    def getBumperReleased(self, hand) -> bool:
        """Whether the bumper was released since the last check.
        :param hand: Side of controller whose value should be returned.
        :returns: Whether the button was released since the last check.
        """
        if hand = self.Hand.kLeft:
            return self.getRawButtonReleased(self.Button.kBumperLeft)
        else:
            return self.getRawButtonReleased(self.Button.kBumperRight)

    def getAButton(self) -> bool:
        """Read the value of the A button on the controller
        :return: The state of the A button
        """
        return self.getRawButton(self.Button.kA)

    def getAButtonPressed(self) -> bool:
        """Whether the A button was pressed since the last check.
        :returns: Whether the button was pressed since the last check.
        """
        return self.getRawButtonPressed(self.Button.kA)

    def getAButtonReleased(self) -> bool:
        """Whether the A button was released since the last check.
        :returns: Whether the button was released since the last check.
        """
        return self.getRawButtonReleased(self.Button.kA)

    def getBButton(self) -> bool:
        """Read the value of the B button on the controller
        :return: The state of the B button
        """
        return self.getRawButton(self.Button.kB)

    def getBButtonPressed(self) -> bool:
        """Whether the B button was pressed since the last check.
        :returns: Whether the button was pressed since the last check.
        """
        return self.getRawButtonPressed(self.Button.kB)

    def getBButtonReleased(self) -> bool:
        """Whether the B button was released since the last check.
        :returns: Whether the button was released since the last check.
        """
        return self.getRawButtonReleased(self.Button.kB)

    def getXButton(self) -> bool:
        """Read the value of the X button on the controller
        :return: The state of the X button
        """
        return self.getRawButton(self.Button.kX)

    def getXButtonPressed(self) -> bool:
        """Whether the X button was pressed since the last check.
        :returns: Whether the button was pressed since the last check.
        """
        return self.getRawButtonPressed(self.Button.kX)

    def getXButtonReleased(self) -> bool:
        """Whether the X button was released since the last check.
        :returns: Whether the button was released since the last check.
        """
        return self.getRawButtonReleased(self.Button.kX)

    def getYButton(self) -> bool:
        """Read the value of the Y button on the controller
        :return: The state of the Y button
        """
        return self.getRawButton(self.Button.kY)

    def getYButtonPressed(self) -> bool:
        """Whether the Y button was pressed since the last check.
        :returns: Whether the button was pressed since the last check.
        """
        return self.getRawButtonPressed(self.Button.kY)

    def getYButtonReleased(self) -> bool:
        """Whether the Y button was released since the last check.
        :returns: Whether the button was released since the last check.
        """
        return self.getRawButtonReleased(self.Button.kY)

    def getBackButton(self) -> bool:
        """Read the value of the Back button on the controller
        :return: The state of the Back button
        """
        return self.getRawButton(self.Button.kBack)

    def getBackButtonPressed(self) -> bool:
        """Whether the Back button was pressed since the last check.
        :returns: Whether the button was pressed since the last check.
        """
        return self.getRawButtonPressed(self.Button.kBack)

    def getBackButtonReleased(self) -> bool:
        """Whether the Back button was released since the last check.
        :returns: Whether the button was released since the last check.
        """
        return self.getRawButtonReleased(self.Button.kBack)

    def getStartButton(self) -> bool:
        """Read the value of the Start button on the controller
        :return: The state of the Start button
        """
        return self.getRawButton(self.Button.kStart)

    def getStartButtonPressed(self) -> bool:
        """Whether the Start button was pressed since the last check.
        :returns: Whether the button was pressed since the last check.
        """
        return self.getRawButtonPressed(self.Button.kStart)

    def getStartButtonReleased(self) -> bool:
        """Whether the Start button was released since the last check.
        :returns: Whether the button was released since the last check.
        """
        return self.getRawButtonReleased(self.Button.kStart)

class IllegialBuzzer():
    """
    1: On 0: Off
    """
    def __init__(self):
        print("Never use this outside testing")
        GPIO.setwarnings(False)
        self.Buzzer_Pin = 17
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.Buzzer_Pin,GPIO.OUT)

    def set(self, value):
        if value == 0:
            GPIO.output(self.Buzzer_Pin,False)
        else:
            GPIO.output(self.Buzzer_Pin,True)


class SpeedController():
    def __init__(self, channel):
        self.motor = PCA9685(0x40, debug=True)
        self.motor.setPWMFreq(50)
        self.channel = channel
        self.current_val = 0
        self.isInverted = False

    def convert(self, value, scale=2000):
        #TODO: perhaps make this math a bit better, might not be needed
        return int(value * scale)

    def set(self, value) -> None:
        """
        Set the motor at the specified channel to the inputed value
        """
        speed = self.convert(value)
        if self.isInverted:
            speed *= -1
        self.current_val = speed
        if self.channel == 2:
            speed *= -1
        
        if speed > 0:
            self.motor.setMotorPwm(self.channel, 0)
            self.motor.setMotorPwm(self.channel + 1, speed)
        elif speed < 0:
            self.motor.setMotorPwm(self.channel + 1, 0)
            self.motor.setMotorPwm(self.channel, abs(speed))
        else:
            self.motor.setMotorPwm(self.channel, 4095)
            self.motor.setMotorPwm(self.channel + 1, 4095)

    def get(self) -> float:
        return self.current_val

    def setInverted(self, isInverted):
        """
        bool isInverted
        """
        self.isInverted = isInverted

    def getInverted(self) -> bool:
        return self.isInverted


class SpeedControllerGroup(SpeedController):

    def __init__(self, *argv):
        self.motors = []
        for motor in argv:
            self.motors.append(motor)
        self.current_speed = 0
        self.isInverted = False

    def set(self, value):
        self.current_speed = value
        for m in self.motors:
            m.set(value)

    def setInverted(self, isInverted):
        """
        bool isInverted
        """
        self.isInverted = isInverted
        for m in self.motors:
            m.setInverted(isInverted)
    
    def getInverted(self) -> bool:
        return self.isInverted

    def get(self):
        return self.current_speed
        
class DifferentialDrive():

    def __init__(self, left: SpeedController, right:SpeedController):
        self.left = left
        self.right = right

    def arcadeDrive(self, xspeed: float, zRotation: float):
        #some math to convert a rotation value to speed value per motor
        pass

    def tankDrive(self, leftSpeed: float, rightSpeed:float):
        self.left.set(leftSpeed)
        self.right.set(rightSpeed)
