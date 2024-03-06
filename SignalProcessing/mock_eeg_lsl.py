import pandas as pd
import numpy as np
import time
from pylsl import StreamInfo, StreamOutlet
from SignalProcessingRepo.SignalProcessing.SSVEP.testing import create_X_mat
from SignalProcessingRepo.SignalProcessing.SSVEP.cca import get_Y


def send_single_eeg_signal():
    # Create a new StreamInfo for the signal stream
    info = StreamInfo('MockEEG', 'Float', 1, 100, 'float32', 'SignalProcessing')

    # Create a new StreamOutlet
    outlet = StreamOutlet(info)

    f_k_arr = np.array([4, 5, 6, 7])
    sample_rate = 500
    t = np.linspace(0, 2, 1/sample_rate)
    Y = get_Y(f_k_arr, t)

    while True:
        # Generate a random single integer sample
        # create_X_mat returns a signal for each channel that carries an underlying
        # reference signal and noise.
        # initially set dimension of signal_arr to (100,)
        X_mat: pd.DataFrame = create_X_mat(
            f_k_arr, sample_rate, noise_params=((1, 40), (1, 80)),
            white_noise_sd=1, n_channels=32, t_max=2
        )
        for t, channel_amps in X_mat.iterrows():
            sample = list(channel_amps)
            # Send the sample
            outlet.push_sample(sample)

        # Wait for a short period of time before sending the next sample
        time.sleep(0.5)  # Adjust this value as needed


if __name__ == "__main__":
    send_single_eeg_signal()
