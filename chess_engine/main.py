from flask import Flask, jsonify
import chess

app = Flask(__name__)

# Sample data
books = [
    {"id": 1, "title": "Python Programming", "author": "Guido van Rossum"},
    {"id": 2, "title": "Flask Web Development", "author": "Miguel Grinberg"},
    {"id": 3, "title": "Django for Beginners", "author": "William S. Vincent"},
    {"id": 4, "title": "Python Programming", "author": "Guido van Rossum"},
    {"id": 5, "title": "Flask Web Development", "author": "Miguel Grinberg"},
    {"id": 6, "title": "Django for Beginners", "author": "William S. Vincent"}
]
'''
current_board = [
    print(chess.BaseBoard())

]

@app.route('/currentboard', methods=['GET'])
def get_books():
    return jsonify(current_board)
'''

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)

if __name__ == '__main__':
    app.run(debug=True)

