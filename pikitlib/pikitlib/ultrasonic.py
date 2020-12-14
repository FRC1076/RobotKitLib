import RPi.GPIO as GPIO
import time
import statistics

#Class requirements (from WPILIB):
# 


class Ultrasonic:
    def __init__(self, pingChannel = 27, echoChannel = 22):
        GPIO.setwarnings(False)

        self.pPin = pingChannel
        self.ePin = echoChannel  
        self.chirpLen = 0.00015

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pPin,GPIO.OUT)
        GPIO.setup(self.ePin,GPIO.IN)
    #Sets up pins connected to the sensor pulse sender 
    # and receiver. On rio would be replaced with channels.

    def sendPulse(self):
        chirpLen = self.chirpLen
        GPIO.output(self.pPin,True)
        time.sleep(chirpLen) 
        '''
        This is the duration of the 
        chirp (will be a little longer because it's sound)
        We may want to decrease the duration; the wpilib
        Ultrasonic suggests 10e^-6 = 0.00001s as a chirp,
        but this is for two possibly different models of 
        sensor.
        '''
        GPIO.output(self.trigger_pin,False)

    def waitForEcho(self,value,timeout):
        count = timeout
        while GPIO.input(self.ePin) != value and count>0:
            count = count-1
        
    def getRangeMM(self):
        distance_cm = 0
        distance_cm=[0,0,0,0,0]
        for i in range(3):
            self.sendPulse()
            self.waitForEcho(True,10000)
            start = time.time()
            self.waitForEcho(False,10000)
            finish = time.time()
            pulse_len = finish-start
            distance_cm[i] = pulse_len/0.000058
        distance_cm=sorted(distance_cm)
        return int(10*(distance_cm[2]))
    
    def getRangeInches(self):
        return int(self.getRangeMM()/25.4)


'''
    This commented out function is from wpilib; I think it counts the number of 
    echoes it gets (which is presumably greater than 1) and doesn't report a value until 
    it gets at least 2. We don't need to use it though and it seems like the current method
    of registering the signal immediately after the first wave is received works fine.
    I could be wrong about what this is doing though.
    
    def isRangeValid(self) -> bool:
        """Check if there is a valid range measurement. The ranges are
        accumulated in a counter that will increment on each edge of the
        echo (return) signal. If the count is not at least 2, then the range
        has not yet been measured, and is invalid.
        :returns: True if the range is valid
        """
        return self.counter.get() > 1
    
'''