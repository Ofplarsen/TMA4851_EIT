from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/choice_space', methods=['GET'])
def send_game_data(data:dict):
    """ data:output json format for interacting with backend"""

    print("Received GET request to /choice_space")
    #dummy data
    #data = {"game_data": "Some data from the game"}
    return jsonify(data), 200


@app.route('/choices', methods=['POST'])
def move_chosen():
    data = request.json  # Get JSON data from the request body
    
    print("Received data:", data)
    #TODO:save data received where it is appropriate
    # Return a response
    return jsonify({"message": "Data received successfully"}), 200



if __name__ == '__main__':
    app.run(debug=True)




















