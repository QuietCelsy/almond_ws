#!/usr/bin/python3
import socket
import sys

from teleop import Teleop

class server():
    def __init__(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.s:
            self.host= "192.168.43.149"
            self.port = 3003
            self.s.bind((self.host, self.port))
            self.s.listen(5)
            self.conn, self.addr = self.s.accept()
            self.mode = ''
            
        
    def switch(self):
        with self.conn:
            self.s.send('client connected'.encode())
            teleop = Teleop(Teleop)
            if self.s.recv(1024).decode == 'manual':
                if self.mode == 'auto':
                    teleop.killswitch()
                else:
                    pass
                self.mode = 'manual'
                teleop.start(self.s.recv(1024).decode)
            # if self.s.recv(1024).decode == 'auto':
            #     if self.mode == 'manual':
            #         automode.killswitch()
            #     else:
            #         pass
            #     self.mode = 'auto'
            #     blablabla
                