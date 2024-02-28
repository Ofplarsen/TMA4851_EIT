from pylsl import StreamInfo, StreamOutlet
import numpy as np
import time

def send_single_int_signal():
    # Create a new StreamInfo for the signal stream
    info = StreamInfo('SingleIntSignal', 'Int', 1, 100, 'int32', 'myuid34235')

    # Create a new StreamOutlet
    outlet = StreamOutlet(info)

    while True:
        # Generate a random single integer sample
        sample = np.random.randint(0, 10)  # Modify the range as needed

        # Send the sample
        outlet.push_sample([sample])

        # Wait for a short period of time before sending the next sample
        time.sleep(0.5)  # Adjust this value as needed

if __name__ == "__main__":
    send_single_int_signal()
