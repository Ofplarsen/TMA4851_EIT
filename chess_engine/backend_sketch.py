import requests
import json
from pylsl import StreamInlet, resolve_stream, resolve_byprop
import time

#this is the draft for backend part
class BackendClient:
    def __init__(self, base_url):
        self.base_url = base_url
        #int_streams = resolve_stream('source_id', 'MentalChess')  # change 'Int' to the actual type of your signal, also check name congruence
        #self.int_inlet = StreamInlet(int_streams[0])
        index_streams = resolve_stream('source_id', 'IndexData')
        self.index_inlet = StreamInlet(index_streams[0])

    def get_data_from_game(self):
        #temp
        base_url = "http://127.0.0.1:5000"
        url = f"{base_url}/choice_space"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            # Handle error
            print(f"Error: {response.status_code}")

    def send_data_to_game(self, data):
        #temp
        base_url = "http://127.0.0.1:5000"
        url = f"{base_url}/choices"
        data=dict(ids=data)
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
            print('Sent data to flickering unit and receiving: ',response.json())
            return response.json()
        else:
            # Handle error
            print(f"Error: {response.status_code}")

    def listen_for_index_from_sp_unit(self):

        """
        url = f"{self.base_url}/extracted_index"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            # Handle error
            print(f"Error: {response.status_code}")"""
        #self.index_inlet
        s = True
        while s:
        # get a single sample
            index_sample, int_timestamp = self.index_inlet.pull_sample()

            # process the single sample
            if index_sample is not None:
                print(f"Received integer sample {index_sample} at timestamp {int_timestamp}")
                if len(index_sample)==2: #dummy validation to filter out bugs
                    print(f"Signal resempling an index received: {index_sample} - ...")
                    s = False
                    return index_sample
                    # exit the loop
                


    def detect_lsl_finished_signal(self):
        finished_indicator_int = [2] #assumes this is finished signal
        print("Looking for a integer/finish signal")
        s = True
        print("listening for signal")

        while s:
            # get a single sample
            int_sample, int_timestamp = self.int_inlet.pull_sample()

            # process the single sample
            if int_sample is not None:
                print(f"Received integer sample {int_sample} at timestamp {int_timestamp}")
                if int_sample == finished_indicator_int:
                    print(f"Signal indicating finished with flickering: {int_sample} - proceed with API request to signal processing...")
                    s = False
                # exit the loop
            else:
                print("stops here")
                
            

        


#example usage
##client = BackendClient("http://127.0.0.1:5000")
#data_from_game = client.get_data_from_game()
#print("Data from component:", data_from_game)
#client.send_data_to_game({"choices": ['a2','a4']})


# main loop
if __name__ == '__main__':
    client = BackendClient("http://10.22.222.36:18080")
    status = True
    while status:
        list_of_indices = []
        #get choises from game engine
        print('\nRequesting data from game\n')
        data_from_game = client.get_data_from_game()

        #send choises to visual unit/flickering
        print('\nSending received data to flickering unit\n')
        client.send_data_to_flicker(data_from_game, list_of_indices=list_of_indices)
        is_final_flag = False
        #list_of_indices = []
        while not is_final_flag:
            
            received_index = client.listen_for_index_from_sp_unit()
            list_of_indices.append(received_index)
            #list_of_indices = [[0, 1],[0,1]]  #temporary before connection to sp
            print('\nSending indexing data to flickering unit\n')
            data_from_flicker = client.send_data_to_flicker(data_from_game, list_of_indices)
            ids = data_from_flicker['ids']
            is_final_flag = data_from_flicker['is_final']
        print('\nSending actual decicions back to game\n')
        status = client.send_data_to_game(ids)['status'] #gets the status from response json to decide if game is over
        
    print('Program loop was terminated as game was marked as finished (status became False)')
        #TODO:receive/listen for data to from signal processing
        #TODO:send what is received from signal p. to flickering unit
        #TODO: iteratively the above ... also wait for the end signal from flickering unit to know when finalized? then know the choises are on the way
            #listen for choises back from flickering unit        




        #receive start signal (lsl?)
            #client.detect_lsl_finished_signal()
            #print('\nSend POST to signal processing\n')