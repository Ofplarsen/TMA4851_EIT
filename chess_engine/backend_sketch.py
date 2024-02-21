import requests
import json

#this is the draft for backend part
class BackendClient:
    def __init__(self, base_url):
        self.base_url = base_url

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
            return response.json()
        else:
            # Handle error
            print(f"Error: {response.status_code}")

    def send_data_to_flicker(self, data):
        url = f"{self.base_url}/display_data"
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            # Handle error
            print(f"Error: {response.status_code}")


#example usage
client = BackendClient("http://127.0.0.1:5000")
data_from_game = client.get_data_from_game()
print("Data from component:", data_from_game)
client.send_data_to_game({"choices": ['a2','a4']})
# main loop
if __name__ == '__main__':
    client = BackendClient("http://127.0.0.1:5000")
    status = True
    while status:
        #get choises from game engine
        data_from_game = client.get_data_from_game()

        #send choises to visual unit/flickering
        client.send_data_to_flicker(data_from_game)
        #TODO: receive start signal (lsl?)
        #TODO:receive/listen for data to from signal processing
        #TODO:send what is received from signal p. to flickering unit
        #TODO: iteratively the above ... also wait for the end signal from flickering unit to know when finalized? then know the choises are on the way
            #listen for choises back from flickering unit
