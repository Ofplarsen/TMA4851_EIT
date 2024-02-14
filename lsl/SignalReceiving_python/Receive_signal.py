from pylsl import StreamInlet, resolve_stream, resolve_byprop
import matplotlib.pyplot as plt
import time

def receive_signal_and_marker():
    print("Looking for an EEG stream...")
    eeg_streams = resolve_stream('type', 'EEG')

    print("Looking for a Marker stream...")
    marker_streams = resolve_byprop('type', 'Markers')

    if len(marker_streams) == 0:
        raise RuntimeError('Could not find marker stream')

    # Create new inlets to read from the streams
    eeg_inlet = StreamInlet(eeg_streams[0])
    marker_inlet = StreamInlet(marker_streams[0])

    # Initialize a variable to keep track of when to start recording
    record_time = None

    # Initialize a list to store the samples
    samples = []

    while True:
        # Get a new sample
        eeg_sample, eeg_timestamp = eeg_inlet.pull_sample(0)
        if eeg_sample is not None:
            print(f"Received EEG sample at timestamp {eeg_timestamp}: {eeg_sample}")

            # If we're in the recording window, save the sample
            if record_time is not None and time.time() - record_time < 3:
                samples.append(eeg_sample)
            elif record_time is not None and time.time() - record_time >= 3:
                # If the recording window has ended, plot the samples
                plt.plot(samples)
                plt.show()

                # Reset the recording window and samples
                record_time = None
                samples = []

        # Get a new marker
        marker, marker_timestamp = marker_inlet.pull_sample(0)
        if marker is not None:
            print(f"Received marker: {marker[0]} at timestamp: {marker_timestamp}")

            # Start the recording window
            record_time = time.time()

if __name__ == "__main__":
    receive_signal_and_marker()
