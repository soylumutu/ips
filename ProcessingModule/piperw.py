#!/usr/local/bin/python3

import os
import select
import fcntl
from utils import decode_msg_size, create_msg

def get_message(fifo: int) -> str:
    """Get a message from the named pipe."""
    msg_size_bytes = os.read(fifo, 4)
    if msg_size_bytes == b'':
        return None
        
    msg_size = decode_msg_size(msg_size_bytes)
    msg_content = os.read(fifo, msg_size)#.decode("utf-8")
    return msg_content

class PipeReader:
    def __init__(self, pipename):        
        self.pipename = pipename

    def get_message(self):
        recv_msg = []
        if not os.path.exists(self.pipename):
            os.mkfifo(self.pipename)
        try:
            # Open the pipe in non-blocking mode for reading
            fifo = os.open(self.pipename, os.O_RDONLY | os.O_NONBLOCK)
            try:
                # Create a polling object to monitor the pipe for new data
                poll = select.poll()
                poll.register(fifo, select.POLLIN)
                try:
                    while True:
                        # Check if there's data to read. Timeout after x millisecs
                        if (fifo, select.POLLIN) in poll.poll(5000):
                            temp = get_message(fifo)
                            if temp:
                                recv_msg.append(temp)
                            else:
                                break
                        else:
                            break
                finally:
                    poll.unregister(fifo)
            finally:
                os.close(fifo)
        finally:
            os.remove(self.pipename)
            return recv_msg

class PipeWriter:
    def __init__(self, pipename:str):
        self.pipename = pipename

    def writemsg(self, message):
        if not os.path.exists(self.pipename):
            os.mkfifo(self.pipename)
            #print("Nobody listening!")
        """else:
            os.remove(self.pipename)
            os.mkfifo(self.pipename)"""

        fifo = os.open(self.pipename, os.O_WRONLY)
        try:
            msg = create_msg(message)
            os.write(fifo, msg)
        except Exception as e:
            print("Could not write to pipe(" + self.pipename + ")! Error: " + str(e))
        finally:
            os.close(fifo)  
