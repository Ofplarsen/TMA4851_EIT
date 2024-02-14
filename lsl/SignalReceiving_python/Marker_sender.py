from pylsl import StreamInfo, StreamOutlet
import keyboard
import time

def send_marker():
    # Create a new StreamInfo for the marker stream
    info = StreamInfo('Markers', 'Markers', 1, 0, 'int32', 'myuidw43536')

    # Create a new StreamOutlet
    outlet = StreamOutlet(info)

    print("Press 's' to send a marker...")

    while True:
        if keyboard.is_pressed('s'):  # if key 's' is pressed 
            print('Marker sent!')
            outlet.push_sample([1])
            time.sleep(0.1)  # prevent bouncing effect of keyboard

if __name__ == "__main__":
    send_marker()
