import sqlite3
import hashlib

def create_connection(db_file):
    """ creating connection to the SQLITE """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("SQLite connection is established.")
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn):
    """ creating the books table in the database """
    try:
        cursor = conn.cursor()
        cursor.execute(""" CREATE TABLE IF NOT EXISTS books (
                            id INTEGER PRIMARY KEY,
                            title TEXT NOT NULL,
                            author TEXT NOT NULL,
                            isbn TEXT NOT NULL,
                            published_date TEXT
                          ); """)
        print("Table created successfully.")
    except sqlite3.Error as e:
        print(e)

def add_book(conn, book): # SQL injection protection has been added in addition to the dictionary input issue
    """Add a new book to the books table using named parameters."""
    sql = '''INSERT INTO books(title, author, isbn, published_date)
             VALUES(:title, :author, :isbn, :published_date)'''
    try:
        with conn:
            conn.execute(sql, book)
    except sqlite3.Error as e:
        print(e)

def update_book(conn, book):
    """ Updating a book using the ID in books table. """
    sql = ''' UPDATE books
              SET title = ? ,
                  author = ? ,
                  isbn = ? ,
                  published_date = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, book)
    conn.commit()


def search_books_by_title(conn, title):
  """ Search for books by title. """
  cur = conn.cursor()
  cur.execute("SELECT * FROM books WHERE title LIKE ?", ('%' + title + '%',))

  rows = cur.fetchall()
  for row in rows:
      print(row)

def delete_book(conn, id):
    """ delete a book from the books table by book id. """
    sql = 'DELETE FROM books WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

def select_all_books(conn):
    """ querying all rows in the books table. """
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")

    rows = cur.fetchall()

    for row in rows:
        print(row)

def select_book_by_id(conn, id):
    """ getting a book by its ID . """
    cur = conn.cursor()
    cur.execute("SELECT * FROM books WHERE id=?", (id,))

    row = cur.fetchone()
    return row

def create_users_table(conn):
  """ Creating user table in the database. """
  try:
      cursor = conn.cursor()
      cursor.execute(""" CREATE TABLE IF NOT EXISTS users (
                          id INTEGER PRIMARY KEY,
                          username TEXT UNIQUE NOT NULL,
                          password TEXT NOT NULL,
                          role TEXT NOT NULL
                        ); """)
      print("Users table created successfully.")
  except sqlite3.Error as e:
      print(e)

def add_user(conn, username, password, role):
  """ Add a new user into the users table. (default role will be user) """
  hashed_password = hashlib.sha256(password.encode()).hexdigest()
  sql = ''' INSERT INTO users(username, password, role)
            VALUES(?,?,?) '''
  cur = conn.cursor()
  cur.execute(sql, (username, hashed_password, role))
  conn.commit()
  return cur.lastrowid

def login_user(conn, username, password):
  """ Validating user logins. """
  hashed_password = hashlib.sha256(password.encode()).hexdigest()
  sql = 'SELECT * FROM users WHERE username=? AND password=?'
  cur = conn.cursor()
  cur.execute(sql, (username, hashed_password))
  user = cur.fetchone()
  return user
  
def does_user_exist(conn, username):
  """ Check if a user already exists in the database. """
  cur = conn.cursor()
  cur.execute("SELECT * FROM users WHERE username=?", (username,))
  return cur.fetchone() is not None

def main():
    database = "library.db"

   
    conn = create_connection(database)

    if conn is not None:

        create_table(conn)


        book = ('Sample Book', 'Author Name', '1234567890', '01-01-2020')
        add_book(conn, book)
        select_all_books(conn)

     
        conn.close()
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    main()
