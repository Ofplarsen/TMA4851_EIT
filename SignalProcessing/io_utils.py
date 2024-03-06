import pandas as pd
import numpy as np
import pyxdf
import matplotlib.pyplot as plt
import time


root = "C:/Users/tbaad/Sync/Education/2024/EiT/SignalProcessing/Data/"


channel_map = {
    "Pz": 11, "P3": 12, "P7": 13, "O1": 15,
    "Oz": 16, "O2": 17, "P8": 19, "P4": 20
}


def read_xdf(filename):
    """


    returns x0, X
    """
    time_0 = time.time()
    streams, fileheader = pyxdf.load_xdf(root + filename)
    for stream in streams:
        if len(stream['time_series']) > 0:
            if stream['info']['name'][0] == 'FlickerStream':
                stream_1 = stream
            if stream['info']['name'][0] == 'LiveAmpSN-056309-0533':
                stream_2 = stream

    if stream_1 is None or stream_2 is None:
        print("Error: Two streams not found in the file.")
        exit()

    # Extract data from the streams

    data_1 = np.array(stream_1['time_series'])
    data_2 = np.array(stream_2['time_series'])
    timestamps_1 = np.round(np.array(stream_1['time_stamps']), 2)
    timestamps_2 = np.round(np.array(stream_2['time_stamps']), 2)

    # For each rounded timestamp that exists both in stream 1 and stream 2:
    #   -   Place the element from stream 1 corresponding to that timestamp
    #       into the array "data_1"
    # Olav method: {

    x0 = pd.Series(data=data_1[:, 0], index=timestamps_1)
    X = pd.DataFrame(data=data_2, index=timestamps_2)
    x0_1 = pd.Series(data=-1 * np.ones(len(timestamps_2)), index=timestamps_2)
    timestamps_3 = x0.index.intersection(X.index)
    x0_1.loc[timestamps_3] = x0.loc[timestamps_3]
    time_1 = time.time()
    print("time elapsed:", time_1 - time_0)
    # }
    x0 = x0_1
    return x0, X

