import numpy as np
import matplotlib.pyplot as plt
import pyxdf
from scipy.interpolate import interp1d
from scipy.signal import find_peaks


channels = ['Fp1', 'Fz', 'F3', 'F7', 'F9', 'FC5', 'FC1', 'C3', 'T7', 'CP5', 'CP1', 'Pz', 'P3', 'P7'
            , 'P9', 'O1', 'Oz', 'O2', 'P10', 'P8', 'P4', 'CP2', 'CP6', 'T8', 'C4', 'Cz'
            , 'FC2', 'FC6', 'F10', 'F8', 'F4', 'Fp2','AUX_1', 'ACC_X', 'ACC_Y', 'ACC_Z']


def get_peaks(data, timestamps, threshold=0.5):
    peaks, _ = find_peaks(data, height=threshold)
    return timestamps[peaks]


def main():
    # Load the XDF file
    filename = 'test_data/sub-w_sensor/ses-S001/eeg/sub-w_sensor_ses-S001_task-Default_run-001_eeg.xdf'
    streams, fileheader = pyxdf.load_xdf(filename)

    for stream in streams:
        if len(stream['time_series']) > 0:
            if stream['info']['name'][0] == 'FlickerStream':
                stream_1 = stream
            if stream['info']['name'][0] == 'LiveAmpSN-056309-0533':
                stream_2 = stream

    if stream_1 is None or stream_2 is None:
        print("Error: Two streams not found in the file.")
        exit()

    # Extract data from the streams

    data_1_ = np.array(stream_1['time_series'])
    data_2 = np.array(stream_2['time_series'])
    timestamps_1 = np.array(stream_1['time_stamps'])
    timestamps_2 = np.array(stream_2['time_stamps'])
    t = timestamps_2

    # For each rounded timestamp that exists both in stream 1 and stream 2:
    #   -   Place the element from stream 1 corresponding to that timestamp
    #       into the array "data_1"
    data_1 = -1 * np.ones(len(timestamps_2))
    for f, i in enumerate(timestamps_1):
        for p, y in enumerate(timestamps_2):
            l = round(i,2)
            å = round(y,2)
            if round(i,2) == round(y,2):
                data_1[p] = data_1_[f]


    #print(get_peaks(data_1, timestamps_2))
    #print(get_peaks(data_2.T[-4], timestamps_2))
    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(timestamps_2, data_1)
    plt.title('Stream 1 Interpolated')
    plt.xlabel('Time')
    plt.ylabel('Data')

    plt.subplot(2, 1, 2)
    plt.plot(timestamps_2, data_2.T[-4])
    plt.title('Stream 2')
    plt.xlabel('Time')
    plt.ylabel('Data')
    plt.xticks(rotation=45)  # Adjust rotation as needed
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()

