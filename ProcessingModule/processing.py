from piperw import PipeReader, PipeWriter
from params import IN_PIPE_NAME, OUT_PIPE_NAME
from time import sleep
import pickle
import pandas as pd
from datetime import datetime

def str2dt(hour:str, minute:str, secs:str):
    return datetime.strptime(hour + ":" + minute + ":" + secs, '%H:%M:%S')

def obj2df(df:pd.DataFrame, obj):
    for item in obj:
        index_list = None 
        l2check = ["source_ip", "source_port", "destination_ip", "destination_port", "protocol"]
        for i in range(len(l2check)):
            if i == 0:
                index_list = df.index[df['source_ip'] == item[0]].tolist()
            else:
                temp = []
                for j in index_list:
                    if df.loc[j, l2check[i]] == item[i]:
                        temp.append(j)
                    
                index_list = temp
                
            if not index_list:
                break
        if index_list:
            df.loc[index_list[0], 'count'] += 1
            df.loc[index_list[0], 'last_time'] = str2dt(item[12], item[13], item[14])
        else:
            df = df.append(pd.Series([item[0], item[1], item[2], item[3], item[4], 1, str2dt(item[12], item[13], item[14]), str2dt(item[12], item[13], item[14])],index=df.columns ), ignore_index=True)
    return df


if __name__ == "__main__":
    flows = pd.DataFrame(columns = ["source_ip", "source_port", "destination_ip", "destination_port", "protocol", "count", "start_time", "last_time"])
    pr = PipeReader(IN_PIPE_NAME)
    while True:
        msg = pr.get_message()
        if not msg:
            sleep(0.5)
            print("empty")
            continue

        for item in msg:
            recv_obj = pickle.loads(item)
            mal_flow = recv_obj["mal_flow"]
            flows = obj2df(flows, mal_flow)
            del recv_obj, mal_flow

        del msg

        
