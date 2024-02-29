from flask import Flask, request, jsonify, render_template
import database_manager as dbm

app = Flask(__name__)

@app.route('/')
def index():
    conn = dbm.create_connection('library.db')
    books = dbm.select_all_books(conn)
    return render_template('index.html', books=books)

@app.route('/books', methods=['GET'])
def books():
    conn = dbm.create_connection('library.db')
    books = dbm.select_all_books(conn)
    if books is not None:
        books_list = [dict(zip(['id', 'title', 'author', 'isbn', 'published_date'], book)) for book in books]
    else:
        books_list = []  # Ensures an empty list is returned if there are no books
    return jsonify(books_list)

@app.route('/books/<int:book_id>', methods=['GET', 'PUT', 'DELETE'])
def book(book_id):
    conn = dbm.create_connection('library.db')
    if request.method == 'GET':
        book = dbm.select_book_by_id(conn, book_id)
        return jsonify(book)
    elif request.method == 'PUT':
        book_details = request.json
        book_details['id'] = book_id
        dbm.update_book(conn, book_details)
        return jsonify({"message": "Book updated successfully"})
    elif request.method == 'DELETE':
        dbm.delete_book(conn, book_id)
        return jsonify({"message": "Book deleted successfully"})

@app.route('/register', methods=['POST'])
def register():
    conn = dbm.create_connection('library.db')
    user_details = request.json
    dbm.add_user(conn, user_details['username'], user_details['password'], user_details.get('role', 'user'))
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    conn = dbm.create_connection('library.db')
    credentials = request.json
    user = dbm.login_user(conn, credentials['username'], credentials['password'])
    if user:
        return jsonify({"message": f"Welcome back, {credentials['username']}!"})
    else:
        return jsonify({"message": "Invalid login."}), 401

if __name__ == '__main__':
    app.run(debug=True)
