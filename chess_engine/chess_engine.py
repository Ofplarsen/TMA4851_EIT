import chess
import random
import json
from flask import Flask, request, jsonify



def board_and_moves(board):
    data = {"choices": [], "display": board.fen()}
    legal_moves = list(board.legal_moves)
    for piece in chess.PIECE_TYPES:
        # Get squares where current piece is located
        piece_squares = board.pieces(piece, chess.WHITE)
        for square in piece_squares:
            # Get legal moves for the piece on the square
            piece_moves = [move for move in legal_moves if move.from_square == square]
            if piece_moves:  # Only add to the list if there are legal moves for this piece
                piece_name = chess.piece_name(piece).upper()[0] + chess.square_name(square)
                data["choices"].append({
                    "name": piece_name,
                    "id": chess.square_name(square),
                    "choices": [{"name": chess.square_name(move.to_square), "id": chess.square_name(move.to_square), "choices": []} for move in piece_moves]
                })
    return data

# Converts input from blinker to "user move" format
def convert_to_string(data):
    return "".join(data['choices'])


def play_the_game(user_move, board):
    move = convert_to_string(convert_to_string(user_move) )       # Input from blinking
    board.push(chess.Move.from_uci(move))  # Make user move
    
    if board.is_game_over():                    # Check if game is over after user move
        print('Game over')
    
    board.push(random.choice(list(board.legal_moves)))# Make random move for computer
    
    if board.is_game_over():                    # Check if game is over after user move
        print('Game over')

#############################################################################
#############################################################################


app = Flask(__name__)


@app.route('/choice_space', methods=['GET'])
def send_game_data():
    """ data:output json format for interacting with backend"""

    print("Received GET request to /choice_space")
    #dummy data
    data = board_and_moves(board) 
    return jsonify(data), 200






@app.route('/choices', methods=['POST'])
def move_chosen():
    user_move = request.json  # Get JSON data from the request body
    
    print("Received data:", user_move)
    #TODO:save data received where it is appropriate
    # Return a response
    play_the_game(user_move, board)
    return jsonify({"message": "Data received successfully"}), 200






if __name__ == '__main__':
    board = chess.Board()
    app.run(debug=True)

