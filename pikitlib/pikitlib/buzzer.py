import RPi.GPIO as GPIO

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
