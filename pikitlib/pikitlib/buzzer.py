import sys
import logging
try:
    import RPi.GPIO as GPIO
except Exception as e:
    logging.error("You are either not using a raspberry pi or dont have RPi.GPIO installed")
    logging.error("If you are deploying code, you can safely ignore this message")
    #sys.exit()


class IllegalBuzzer():
    """
    1: On 0: Off
    """
    def __init__(self, pin):
        print("Never use this outside testing")
        GPIO.setwarnings(False)
        self.buzzer_pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.buzzer_pin,GPIO.OUT)

    def set(self, value):
        if value == 0:
            GPIO.output(self.buzzer_pin,False)
        else:
            GPIO.output(self.buzzer_pin,True)
