import socket
import tqdm
import os
import logging
import buffer




class codeReceiver():

    def __init__(self):
        pass
        

    def setupConnection(self):
        self.conn, self.addr = s.accept()
        print("Got a connection from ", self.addr)
        self.connbuf = buffer.Buffer(self.conn)

        
    def receiveFile(self):
        hasFile = True
        while True:
            hash_type = self.connbuf.get_utf8()
            if not hash_type:
                break
            print('hash type: ', hash_type)

            file_name = self.connbuf.get_utf8()
            if not file_name:
                hasFile = False
                break
            file_name = os.path.join('uploads',file_name)
            print('file name: ', file_name)

            file_size = int(self.connbuf.get_utf8())
            print('file size: ', file_size )

            with open(file_name, 'wb') as f:
                remaining = file_size
                while remaining:
                    chunk_size = 4096 if remaining >= 4096 else remaining
                    chunk = self.connbuf.get_bytes(chunk_size)
                    if not chunk: break
                    f.write(chunk)
                    remaining -= len(chunk)
                if remaining:
                    print('File incomplete.  Missing',remaining,'bytes.')
                else:
                    print('File received successfully.')
        print('Connection closed.')
        self.conn.close()
        return hasFile
        