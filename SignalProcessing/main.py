import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyxdf
import time
from SignalProcessingRepo.SignalProcessing.io_utils import read_xdf
from SignalProcessingRepo.SignalProcessing import filter
from SignalProcessingRepo.SignalProcessing.SSVEP.cca import cca_maxcorr_freq
from SignalProcessingRepo.SignalProcessing.SSVEP.cca import get_Y
from pylsl import StreamInfo, StreamOutlet


if __name__ == "__main__":
    # info = StreamInfo('SingleIntSignal', 'Int', 1, 100, 'int32', 'myuid34235')
    # Both output and input from lsl needs a info object
    # type(setup_params) = Flicker_info
    # listen_for_start might return a timestamp
    # listen_for_amp is a stream that returns [timestamp, amp(timestamp)]
    # amp_data = [[t, amp(t)]]
    # each info-object needs an inlet or outlet object

    # seed parameters:
    f_k_arr = np.array([4, 5, 6, 7])
    sample_rate = 500
    t = np.linspace(0, 2, 1/sample_rate)
    Y = get_Y(f_k_arr, t)

    while True:
        t = listen_for_start(info_flicker)  # method defined by Hans
        X_row, X_col = listen_for_amp(info_flicker, info_amp)  # to be defined by Hans
        # X_row = (
        #
        # apply signal processing to row_amp and col_amp respectively to
        # first obtain the max-correlation reference frequency and then
        # find argmax = row_n
        row_idx = cca_maxcorr_freq(X_row, Y)  # already exists, but with different name
        col_idx = cca_maxcorr_freq(X_col, Y)
        idxs = [row_idx, col_idx]
        send_idx_data(info_backend, idxs)

        # TODO
        # Torbjørn:
        # 1. add argmax_freq
        # 2. mock_eeg_lsl.get_signal_matrix
        # 3. send_idx_data
        # Olav:
        # 1. listen_for_start(info_flicker)
        # 2. listen_for_amp(info_flicker, info_amp)
        # 3.



