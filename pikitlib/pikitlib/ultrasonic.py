import RPi.GPIO as GPIO
import time
import statistics
import pikitlib
import threading

class Ultrasonic:
    def __init__(self, pingChannel = 27, echoChannel = 22):
        GPIO.setwarnings(False)

        self.pPin = pingChannel
        self.ePin = echoChannel  
        self.chirpLen = 0.00015

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pPin,GPIO.OUT)
        GPIO.setup(self.ePin,GPIO.IN)

        self.range = None
        self.stop_threads = False
        self.t = threading.Thread(target=updateRange, args =(lambda : self.stop_threads, ))


    def updateRange(self, stop):
        t = pikitlib.Timer() 
        t.start()
        while not stop():
            if t.get() > 0.2:
                v = self.getRangeInches()
                self.range = v
                t.reset()

    def get(self):
        return self.range

        
    def quit(self):
        self.stop_threads = True

    def sendPulse(self):
        chirpLen = self.chirpLen
        GPIO.output(self.pPin,True)
        time.sleep(chirpLen) 
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
