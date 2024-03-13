import numpy as np
import time
info = ...
int_inlet = ...
import threading

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
                
def listen_for_indicator(flicker_inlet, indicator):
    """Thread function to listen for indicator signal."""
    while True:
        int_sample, _ = flicker_inlet.pull_sample()
        if int_sample == indicator:
            print(f"Received integer sample {int_sample} indicating switch recording")
            break

def listen_for_amp(flicker_inlet, amp_inlet, indicator):
    amp = []
    i = 0
    j = 0
    indicator_thread = threading.Thread(target=listen_for_indicator, args=(flicker_inlet, indicator))
    indicator_thread.start()
    while indicator_thread.is_alive():
        j +=1
        # get a single indicator sample
        amp_sample, amp_timestamp = amp_inlet.pull_sample()
        # process the single sample
        #print('iteration', j)
        if amp_sample is not None:
            amp.append(amp_sample) #omitting timestamp

    indicator_thread.join()
    print(f'Returning eeg sequence for indicator signal: {indicator}\n')
    print('len of the array', len(amp))
    return np.array(amp)
"""
def listen_for_amp(flicker_inlet, amp_inlet, indicator: list):
    #Indicator being [1] for first call, [2] for second.
    s = True
    amp = []
    i = 0
    j = 0
    while s:
        j +=1
        # get a single indicator sample
        amp_sample, int_timestamp = amp_inlet.pull_sample()
        # process the single sample
        print('iteration', j)
        if amp_sample is not None:
            i +=1
            print(i)
            amp.append(amp_sample) #omitting timestamp
        
        # get a single indicator sample
        print('before getting indeicator')
        int_sample, int_timestamp = flicker_inlet.pull_sample()
        print('after getting indeicator')

        # process the single sample
        if int_sample is not None:
            print(f"Received integer sample {int_sample} at timestamp {int_timestamp}")
            if int_sample == indicator:
                print(f"Signal indicating switch recording: {int_sample} ...")
                s = False
        print('reached end')
    print(i)
    print(amp)
    return np.array(amp)
"""

def send_index_data(backend_outlet, indices):
    backend_outlet.push_sample(indices)
    print('Sent indices to backend.')
