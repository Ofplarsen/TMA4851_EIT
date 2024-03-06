import pandas as pd
import numpy as np
import time
from pylsl import StreamInfo, StreamOutlet


def send_single_eeg_signal():
    # Create a new StreamInfo for the signal stream
    info = StreamInfo('MockEEG', 'Float', 1, 100, 'float32', 'SignalProcessing')

    # Create a new StreamOutlet
    outlet = StreamOutlet(info)

    while True:
        # Generate a random single integer sample
        # get_signal_arr returns a signal that carries an underlying reference signal
        # and noise
        # initially set dimension of signal_arr to (100,)
        signal_arr: np.ndarray = get_signal_matrix()
        for signal in signal_arr:
            sample = signal
            # Send the sample
            outlet.push_sample([sample])

        # Wait for a short period of time before sending the next sample
        time.sleep(0.5)  # Adjust this value as needed


if __name__ == "__main__":
    send_single_eeg_signal()
