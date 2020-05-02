import socket
import time
#import pickle

from piperw import PipeWriter

class TCPServer:
    def __init__(self, headersize:int, server_port:int, pipename:str, listen_limit = 5):
        self.headersize = headersize
        self.server_port = server_port
        self.listen_limit = listen_limit
        self.socket = 0
        self.recv_obj = None
        self.pipewriter = PipeWriter(pipename)

    def startServer(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('', self.server_port))
        self.socket.listen(self.listen_limit)
        print("Listening at port: " + str(self.server_port) + "\n")

    def accept_recv(self):
        while True:
            clientsocket, address = self.socket.accept()
            print(f"Connection from {address} has been established.")
            
            full_msg = b''
            new_msg = True
            while True:
                msg = clientsocket.recv(4096)
                if len(msg) == 0:
                    break
                if new_msg:
                    msglen = int(msg[:self.headersize])
                    new_msg = False

                full_msg += msg

                if len(full_msg)-self.headersize == msglen:
                    print("Message received!")
                    self.pipewriter.writemsg(full_msg[self.headersize:])
                    new_msg = True
                    full_msg = b""
