import pyxdf
import pandas as pd
import numpy as np


root = "C:/Users/tbaad/Sync/Education/2024/EiT/SignalProcessing/BCISpellerData/"
channel_map = {
    "Pz": 11, "P3": 12, "P7": 13, "O1": 15,
    "Oz": 16, "O2": 17, "P8": 19, "P4": 20
}


def read_xdf(relative_path: str):
    data, header = pyxdf.load_xdf(root + relative_path)
    data = data[0]
    X_0 = data["time_series"]
    dict = {}
    for name, col_ind in channel_map.items():
        dict[name] = X_0[:, col_ind]
    sample_rate = float(data["info"]["nominal_srate"][0])
    print("sample rate:", sample_rate)
    n = X_0.shape[0]
    t = np.arange(1, n + 1) / sample_rate
    t -= t[0]
    X = pd.DataFrame(data=dict, index=t)
    return X
