import sys
try:
    import RPi.GPIO as GPIO
except Exception as e:
    print("You are either not using a raspberry pi or dont have RPi.GPIO installed")
    print("Quiting...")
    #sys.exit()


class IllegalBuzzer():
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
