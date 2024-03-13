import chess
import random
from flask import Flask, request, jsonify

#############################################################################
#############################################################################

board = chess.Board()
app = Flask(__name__)


class ChessEngine:
    def __init__(self) -> None:
        self.board = chess.Board()

    def get_game_data(self):
        board = self.board

        legal_moves = list(board.legal_moves)
        disp = str(board)
        disp = disp.replace(' ', '')
        data = {"choices": [], "display": disp, "status": not board.is_game_over()}
        if not data['status']: #drops if no choises to send
            return data
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
    def convert_to_string(self, data):
        print('data["ids"]: ', data['ids'], type(data['ids']))
        return "".join(data['ids'])


    """def play_the_game(user_move, board):
        move = convert_to_string(convert_to_string(user_move) )       # Input from blinking
        board.push(chess.Move.from_uci(move))  # Make user move
        
        if board.is_game_over():                    # Check if game is over after user move
            print('Game over')
        
        board.push(random.choice(list(board.legal_moves)))# Make random move for computer
        
        if board.is_game_over():                    # Check if game is over after user move
            print('Game over')"""

    def do_move(self, user_move):
        board = self.board
        print("User move received from Backend:\n", user_move)
        if board.is_game_over():
            print('The game received a move, but the game is finished')
            return False
        
        move = self.convert_to_string(user_move)  # Input from blinking
        move_uci = chess.Move.from_uci(move)
        if not move_uci in board.legal_moves:
            print('The move from backend was not legal: ', move_uci)
            print('proceeds with random')
            move_uci = random.choice(list(board.legal_moves))

        print("Board before user move:\n", board)
        
        board.push(move_uci)  # Make user move
        print("Board after user move:\n", board)
        
        if board.is_game_over():  # Check if game is over after user move
            print('Game over')
            return False
        else:
            computer_move = random.choice(list(board.legal_moves))
            print("Computer move:\n", computer_move)
            board.push(computer_move)  # Make random move for computer
            print("Board after computer move:\n", board)
        
            if board.is_game_over():  # Check if game is over after computer move
                print('Game over')
                return False

        self.board = board
        return True

chess_engine = ChessEngine()

#############################################################################
@app.route('/choice_space', methods=['GET'])
def send_game_data(engine=chess_engine):
    """ data:output json format for interacting with backend"""

    print("Received GET request to /choice_space")
    #dummy data
    data = engine.get_game_data() 
    print('This is the data to be sent', data)
    return jsonify(data), 200


@app.route('/choices', methods=['POST'])
def move_chosen(engine=chess_engine):
    user_move = request.json  # Get JSON data from the request body
    
    print("Received data:", user_move)
    #TODO:save data received where it is appropriate
    # Return a response
    status = engine.do_move(user_move)
    return jsonify({"message": "Data received successfully", "status":status}), 200
#############################################################################
#board = chess.Board()
#app = Flask(__name__)








if __name__ == '__main__':
    

    app.run(debug=True)

