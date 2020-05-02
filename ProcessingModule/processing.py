from piperw import PipeReader, PipeWriter
from params import IN_PIPE_NAME, OUT_PIPE_NAME
from time import sleep
import pickle

pr = PipeReader(IN_PIPE_NAME)
while True:
    msg = pr.get_message()
    if not msg:
        sleep(0.5)
        print("empty")
        continue

    for item in msg:
        recv_obj = pickle.loads(item)
        print(recv_obj)
