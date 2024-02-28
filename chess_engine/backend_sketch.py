import requests
import json
from pylsl import StreamInlet, resolve_stream, resolve_byprop
import time

#this is the draft for backend part
class BackendClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.int_streams = resolve_stream('source_id', 'MentalChess')  # change 'Int' to the actual type of your signal, also check name congruence


    def get_data_from_game(self):
        url = f"{self.base_url}/choice_space"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            # Handle error
            print(f"Error: {response.status_code}")

    def send_data_to_game(self, data):
        url = f"{self.base_url}/choices"
        response = requests.post(url, json=data)
        if response.status_code == 200:
            #print('Data sent successfully to game. Response: ', response.json())
            return response.json()
        else:
            # Handle error
            print(f"Error: {response.status_code}")

    def send_state_to_flicker(self, data):
        url = f"{self.base_url}/display_data"
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print('Sent game state to flickering unit: ',response.json())
            return response.json()
        else:
            # Handle error
            print(f"Error: {response.status_code}")

    def send_data_to_flicker(self, data_from_game, list_of_indices):
        """Sending index data from signal processing data to the flickering unit. Returning a status if we can expect further iterations or not (before getting a choice returned)."""
        url = f"{self.base_url}/index_data"
        data = dict(state=data_from_game, indices=list_of_indices)
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print('Sent index to flickering unit: ',response.json())
            return response.json().is_final
        else:
            # Handle error
            print(f"Error: {response.status_code}")

    def get_index_from_sp_unit(self):
        url = f"{self.base_url}/extracted_index"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            # Handle error
            print(f"Error: {response.status_code}")


    def detect_lsl_finished_signal(self):
        finished_indicator_int = [2] #assumes this is finished signal
        print("Looking for a integer/finish signal")
        s = True
        print("listening for signal")

        while s:
            if len(self.int_streams) > 0:
                #print('Inside if (signal found?)')
                # create a new inlet to read from the stream
                int_inlet = StreamInlet(self.int_streams[0])

                # get a single sample
                int_sample, int_timestamp = int_inlet.pull_sample()

                # process the single sample
                if int_sample is not None:
                    print(f"Received integer sample {int_sample} at timestamp {int_timestamp}")
                    if int_sample == finished_indicator_int:
                        print(f"Signal indicating finished with flickering: {int_sample} - proceed with API request to signal processing...")
                        s = False
                # exit the loop
                
            else:
                print("Signal not found. Retrying in 1 second...")
                time.sleep(0.5)  # wait for 1 second before retrying

        


#example usage
##client = BackendClient("http://127.0.0.1:5000")
#data_from_game = client.get_data_from_game()
#print("Data from component:", data_from_game)
#client.send_data_to_game({"choices": ['a2','a4']})


# main loop
if __name__ == '__main__':
    client = BackendClient("http://127.0.0.1:5000")
    status = True
    while status:
        list_of_indices = []
        #get choises from game engine
        print('\Requesting data from game\n')
        data_from_game = client.get_data_from_game()

        #send choises to visual unit/flickering
        print('\nSending received data to flickering unit\n')
        client.send_data_to_flicker(data_from_game, list_of_indices=list_of_indices)
        is_final_flag = False
        #list_of_indices = []
        while not is_final_flag:
            #receive start signal (lsl?)
            client.detect_lsl_finished_signal()
            print('\nSend POST to signal processing\n')
            received_index = client.get_index_from_sp_unit()
            list_of_indices.append(received_index)
            print('\nSending indexing data to flickering unit\n')
            choices, is_final_flag = client.send_index_to_flicker(data_from_game, list_of_indices)
        print('\nSending actual decicions back to game\n')
        client.send_data_to_game(choices)
        

        #TODO:receive/listen for data to from signal processing
        #TODO:send what is received from signal p. to flickering unit
        #TODO: iteratively the above ... also wait for the end signal from flickering unit to know when finalized? then know the choises are on the way
            #listen for choises back from flickering unit

        #temporary:
        status=False