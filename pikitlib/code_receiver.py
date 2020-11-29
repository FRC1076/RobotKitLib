import socket
import tqdm
import os
import logging

class codeReceiver():

    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.buffer_size = 4096
        self.speperator = "/"

        self.s = socket.socket()
        

    def setupConnection(self):
        self.s.bind((self.host, self.port))

        self.s.listen(5)
        print(f"[*] Listening as {self.host}:{self.port}")

        self.client_socket, address = self.s.accept() 

        print(f"[+] {address} is connected.")

        
    def receiveFile(self):
        received = self.client_socket.recv(self.buffer_size).decode()
        filename, filesize = received.split(self.speperator)

        self.filename = os.path.basename(filename)

        self.filesize = int(filesize)


        progress = tqdm.tqdm(range(self.filesize), f"Receiving {self.filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(self.filename, "wb") as f:
            for _ in progress:
                
                bytes_read = self.client_socket.recv(self.buffer_size)
                if not bytes_read:    
                    break
                
                f.write(bytes_read)

                progress.update(len(bytes_read))
