import socket

class Ultrasonic:
    def __init__(self, pingChannel = 27, echoChannel = 22):

        self.pPin = pingChannel
        self.ePin = echoChannel  
        self.chirpLen = 0.00015

  
    def getRangeInches(self):
        s = socket.socket()
        host = 'localhost'
        port = 1235
        s.bind((host,port))
        s.listen(5)
        sc, addr = s.accept()
        print("received info")
        message = socketclient.recv(1024)
        message = message.decode("utf-8")
        return message
        
