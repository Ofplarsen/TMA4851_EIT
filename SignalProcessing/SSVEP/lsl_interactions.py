import numpy as np
import time
info = ...
int_inlet = ...

def listen_for_start(int_inlet):
    start_indicator = [0]
    s = True
    while s:
        # get a single sample
        int_sample, int_timestamp = int_inlet.pull_sample()

        # process the single sample
        if int_sample is not None:
            print(f"Received integer sample {int_sample} at timestamp {int_timestamp}")
            if int_sample == start_indicator:
                print(f"Signal indicating start recording: {int_sample} ...")
                s = False
    # exit the loop
                
def listen_for_amp(flicker_inlet, amp_inlet, indicator: list):
    """Indicator being [1] for first call, [2] for second."""
    s = True
    amp = []
    while s:
        # get a single indicator sample
        amp_sample, int_timestamp = amp_inlet.pull_sample()
        # process the single sample
        if amp_sample is not None:
            amp.append(amp_sample) #omitting timestamp
        
        # get a single indicator sample
        int_sample, int_timestamp = flicker_inlet.pull_sample()
        # process the single sample
        if int_sample is not None:
            print(f"Received integer sample {int_sample} at timestamp {int_timestamp}")
            if int_sample == indicator:
                print(f"Signal indicating switch recording: {int_sample} ...")
                s = False
    return np.array(amp)


def send_index_data(backend_outlet, indices):
    backend_outlet.push_sample(indices)
    print('Sent indices to backend.')
