import socket

class Ultrasonic:
    def __init__(self, pingChannel = 27, echoChannel = 22):

        self.pPin = pingChannel
        self.ePin = echoChannel  
        self.chirpLen = 0.00015
        self.s = socket.socket()
        

    def connect():
        host = 'localhost'
        port = 1235
        self.s.bind((host,port))
        self.s.listen(5)
        sc, addr = self.s.accept()

    def getRangeInches(self):
        
        
        
        print("received info")
        message = socketclient.recv(1024)
        message = message.decode("utf-8")
        return message
        
