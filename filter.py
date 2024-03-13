import pandas as pd
import scipy
import numpy as np

'''
Implementation of filtering can be read on page 47 in the Bachelor Thesis
Notch filter:
    - frequency = 50 Hz
    - Quality factor = 0.25
Pass-band filter:
    - Bandpass = 1 - 15 Hz
    - Order = 3

TODO:
- Find a way to cut-off the Data to capture only periods before and after
outsized spikes, which indicate that the recording device is disrupted.
- Pipeline:
    - read xdf file to DataFrame X
    - Apply filters (Notch and Bandpass) to X
    - Cut off parts of X affected by recording disruptions and/or 
    endpoint distortions due to filtering
    - Assemble Y (fundamental frequencies)
    - Apply rolling CCA to X using Y
'''


def apply_filters(X, notch_freq, notch_Q, passband, bandpass_order):
    #X = X.loc[0:75, :]
    t = X.index
    cols = X.columns
    n = len(t)
    sample_freq = int(round(n / (t[-1] - t[0])))
    b, a = scipy.signal.iirnotch(notch_freq, notch_Q, sample_freq)
    X_arr = scipy.signal.lfilter(b, a, X.T)
    b, a = scipy.signal.butter(
        bandpass_order, passband, btype="bandpass", analog=False, output='ba',
        fs=sample_freq
    )
    X_arr = scipy.signal.lfilter(b, a, X).T
    X = pd.DataFrame(data=X_arr, columns=cols, index=t)
    return X  # X.loc[3.5:, :]


def trend_deviation(X, win):
    # Indicator that measures rolling deviation from trend
    median = X.rolling(win).median()
    sd = X.rolling(win).median()
    return (X - median)/sd
