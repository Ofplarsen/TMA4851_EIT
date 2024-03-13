import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyxdf
import time
from pylsl import StreamInlet, resolve_stream, resolve_byprop
from io_utils import read_xdf
import filter
from SSVEP.cca import cca_maxcorr_freq, get_Y
from lsl_interactions import listen_for_amp, listen_for_start, send_index_data
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
    #t = np.arange(0, 2, 1/sample_rate)
    #Y = get_Y(f_k_arr, t)

    backend_info = StreamInfo('IndexData', 'Marker', 2, 100, 'int32', 'IndexData')
    backend_outlet = StreamOutlet(backend_info)

    flicker_info = resolve_stream('source_id', 'MentalChess')
    flicker_inlet = StreamInlet(flicker_info[0])

    amp_info = resolve_stream('source_id', 'SignalProcessing')
    amp_inlet = StreamInlet(amp_info[0])

    


    while True:
        tid = listen_for_start(flicker_inlet)  # method defined by Hans
        X_row = listen_for_amp(flicker_inlet, amp_inlet, indicator=[1])[-3000:]  # to be defined by Hans
        X_col = listen_for_amp(flicker_inlet, amp_inlet, indicator=[2])[-3000:]
        t = np.arange(0, X_row.shape[0]*0.02, 0.02)

        print('Get y now...')
        Y = get_Y(f_k_arr, t)

        print(Y.shape, X_row.shape)
        X_row = filter.apply_filters(pd.DataFrame(data=X_row, index=t), 0.2, 0.25, (1, 15), 3)
        row_idx = cca_maxcorr_freq(pd.DataFrame(X_row), Y)  # already exists, but with different name
        t_x_col = np.arange(0, X_col.shape[0]*0.02, 0.02)
        Y_x_col = get_Y(f_k_arr, t_x_col)
        X_col = filter.apply_filters(pd.DataFrame(data=X_col, index=t_x_col), 0.2, 0.25, (1, 15), 3)
        col_idx = cca_maxcorr_freq(pd.DataFrame(X_col), Y_x_col)
        idxs = [row_idx, col_idx]
        print('estimated indices: ', idxs)
        send_index_data(backend_outlet, idxs)

        # TODO
        # Torbjørn:
        # 1. add argmax_freq
        # 2. mock_eeg_lsl.get_signal_matrix
        # 3. send_idx_data
        # Olav:
        # 1. listen_for_start(info_flicker)
        # 2. listen_for_amp(info_flicker, info_amp)
        # 3.



