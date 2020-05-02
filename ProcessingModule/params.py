#!/usr/local/bin/python3
from os.path import expanduser

home = expanduser("~")

IN_PIPE_NAME = home + "/pipes/server2process"
OUT_PIPE_NAME = home + "/pipes/process2flow"