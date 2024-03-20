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
import P300_selection_peakpick


if __name__ == "__main__":
    # info = StreamInfo('SingleIntSignal', 'Int', 1, 100, 'int32', 'myuid34235')
    # Both output and input from lsl needs a info object
    # type(setup_params) = Flicker_info
    # listen_for_start might return a timestamp
    # listen_for_amp is a stream that returns [timestamp, amp(timestamp)]
    # amp_data = [[t, amp(t)]]
    # each info-object needs an inlet or outlet object

    # seed parameters:
    #f_k_arr = np.array([4, 5, 6, 7])
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
        start = time.time()
        X_row = listen_for_amp(flicker_inlet, amp_inlet, indicator=[1])[-3000:]  # to be defined by Hans
        end = time.time()

        n = round((end - start)/0.8) #800ms per cycle

        X_col = listen_for_amp(flicker_inlet, amp_inlet, indicator=[2])[-3000:]

        # X_row and X_col are generated from available data files in evaluate_Y instead of being analyzed directly
        idxs = P300_selection_peakpick.evaluate_Y(n)
        print('estimated indices: ',  idxs)
        send_index_data(backend_outlet, idxs)



