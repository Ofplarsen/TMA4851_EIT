import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyxdf
import time
from SignalProcessingRepo.SignalProcessing.io_utils import read_xdf
from SignalProcessingRepo.SignalProcessing.SSVEP import io_utils
from SignalProcessingRepo.SignalProcessing import filter
from SignalProcessingRepo.SignalProcessing.SSVEP import testing
from SignalProcessingRepo.SignalProcessing.SSVEP.cca import rolling_cca_classification
from pylsl import StreamInfo, StreamOutlet


if __name__ == "__main__":
    # info = StreamInfo('SingleIntSignal', 'Int', 1, 100, 'int32', 'myuid34235')
    # Both output and input from lsl needs a info object
    # type(setup_params) = Flicker_info
    # listen_for_start might return a timestamp
    # listen_for_amp is a stream that returns [timestamp, amp(timestamp)]
    # amp_data = [[t, amp(t)]]
    # each info-object needs an inlet or outlet object

    while True:
        t = listen_for_start(info_flicker)  # method defined by Hans
        X_row, X_col = listen_for_amp(info_flicker, info_amp)  # to be defined by Hans
        # X_row = (
        #
        # apply signal processing to row_amp and col_amp respectively to
        # first obtain the max-correlation reference frequency and then
        # find argmax = row_n
        row_idx = argmax_freq(row_amp)  # already exists, but with different name
        col_idx = argmax_freq(col_amp)
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



