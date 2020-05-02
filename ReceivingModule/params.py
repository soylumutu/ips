#!/usr/local/bin/python3
from os.path import expanduser

home = expanduser("~")
PIPE_NAME = home + "/pipes/server2process"
HEADERSIZE = 32
SERVER_PORT = 50008