import RPi.GPIO as GPIO
import time
import statistics

#Class requirements (from WPILIB):
# 


class Ultrasonic:
    def __init__(self):
        GPIO.setwarnings(False)
        self.trigger_pin = 27#=pingChannel
        self.echo_pin = 22#echoChannel  
        self.chirp_length = 0.00015
        self.detect_value = 10000 #This is the value at which
        #we report the signal having been received. This value
        #is from freenove.
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin,GPIO.OUT)
        GPIO.setup(self.echo_pin,GPIO.IN)
    #Sets up pins connected to the sensor pulse sender 
    # and receiver. On rio would be replaced with channels.

    def send_trigger_pulse(self):
        chirp_length = self.chirp_length
        GPIO.output(self.trigger_pin,True)
        time.sleep(chirp_length) 
        '''
        This is the duration of the 
        chirp (will be a little longer because its sound)
        We may want to decrease the duration; the wpilib
        Ultrasonic suggests 10e^-6 = 0.00001s as a chirp,
        but this is for the
        '''
        GPIO.output(self.trigger_pin,False)

    def wait_for_echo(self,value,timeout):
        count = timeout
        while GPIO.input(self.echo_pin) != value and count>0:
            count = count-1
        

    def getRangeMM(self):
        distance_cm = 0
        distance_cm=[0,0,0,0,0]
        for i in range(3):
            self.send_trigger_pulse()
            self.wait_for_echo(True,10000)
            start = time.time()
            self.wait_for_echo(False,10000)
            finish = time.time()
            pulse_len = finish-start
            distance_cm[i] = pulse_len/0.000058
        distance_cm=sorted(distance_cm)
        return int(10*(distance_cm[2]))
    
    def getRangeInches(self):
        return int(self.getRangeMM()/25.4)

U = Ultrasonic()
while True:
    print(U.getRangeInches())


'''
    
    
    def isRangeValid(self) -> bool:
        """Check if there is a valid range measurement. The ranges are
        accumulated in a counter that will increment on each edge of the
        echo (return) signal. If the count is not at least 2, then the range
        has not yet been measured, and is invalid.
        :returns: True if the range is valid
        """
        return self.counter.get() > 1
'''