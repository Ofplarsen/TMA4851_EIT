import numpy as np
import matplotlib.pyplot as plt
import pyxdf

def main():
    # Load the XDF file
    filename = 'test_data/sub-P001/ses-S001/eeg/p300_3000ms_between_each.xdf'
    streams, fileheader = pyxdf.load_xdf(filename)

    # Extract the streams
    stream_1 = None
    stream_2 = None
    for stream in streams:
        if len(stream['time_series']) > 0:
            if stream_1 is None:
                stream_1 = stream
            else:
                stream_2 = stream

    if stream_1 is None or stream_2 is None:
        print("Error: Two streams not found in the file.")
        return

    # Extract data from the streams
    data_1 = np.array(stream_1['time_series'])
    data_2 = np.array(stream_2['time_series'])
    timestamps_1 = np.array(stream_1['time_stamps'])
    timestamps_2 = np.array(stream_2['time_stamps'])

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(timestamps_1, data_1)
    plt.title('Stream 1')
    plt.xlabel('Time')
    plt.ylabel('Data')

    plt.subplot(2, 1, 2)
    plt.plot(timestamps_2, data_2)
    plt.title('Stream 2')
    plt.xlabel('Time')
    plt.ylabel('Data')
    plt.xticks(timestamps_2, rotation=45)  # Adjust rotation as needed
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()

