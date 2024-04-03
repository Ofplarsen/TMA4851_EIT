import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import time
from pylsl import StreamInlet, resolve_stream, resolve_byprop
from io_utils import read_xdf
#import filter
from lsl_interactions import listen_for_amp, listen_for_start, send_index_data
from pylsl import StreamInfo, StreamOutlet
import P300.signal_functions as sf
import P300.P300_selection_peakpick


if __name__ == "__main__":

    backend_info = StreamInfo('IndexData', 'Marker', 2, 100, 'int32', 'IndexData')
    backend_outlet = StreamOutlet(backend_info)

    flicker_info = resolve_stream('source_id', 'MentalChess')
    flicker_inlet = StreamInlet(flicker_info[0])

    while True:
        tid = listen_for_start(flicker_inlet)  # method defined by Hans
        # Listen for rows
        start = time.time()
        #X_row = listen_for_amp(flicker_inlet, amp_inlet, indicator=[1])[-3000:]  # Listen to signal from LSL, replaced with sleep here
        time.sleep(4.8)
        end = time.time()
        m = round((end - start)/0.8) # Determines how many cycles to listen for, 800ms per cycle

        # Listen for columns
        print("Between sleeps")
        start = end
        #X_col = listen_for_amp(flicker_inlet, amp_inlet, indicator=[2])[-3000:]  # Listen to signal from LSL, replaced with sleep here
        time.sleep(4.8)
        end = time.time()  
        n =  round((end - start)/0.8)

        # X_row and X_col are generated from available data files in evaluate_Y instead of being analyzed directly
        idxs = P300.P300_selection_peakpick.evaluate_Y(m, n)
        print('Estimated indices: ',  idxs)
        send_index_data(backend_outlet, idxs)



