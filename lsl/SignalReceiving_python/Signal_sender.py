'''
Sends random singal in 32 channels
'''

from pylsl import StreamInfo, StreamOutlet
import numpy as np
import time

def send_random_signal():
    # Create a new StreamInfo for the signal stream
    info = StreamInfo('RandomSignal', 'EEG', 32, 100, 'float32', 'myuid34234')

    # Create a new StreamOutlet
    outlet = StreamOutlet(info)

    while True:
        # Generate a random sample with 32 values
        sample = np.random.random(32)

        # Send the sample
        outlet.push_sample(sample)

        # Wait for a short period of time before sending the next sample
        time.sleep(0.01)  # Adjust this value as needed

if __name__ == "__main__":
    send_random_signal()