import sqlite3
import hashlib #hashlib library for hashing the passwords

def create_connection(db_file): #database connection
    """ creating connection to the SQLITE """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("SQLite connection is established.")
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn): #Function for creating a table if it doesnt exist
    """ creating the books table in the database """
    try: #Try and except is the best way for preventing errors or SQL injection. However it depends on the query too (you'll see this throughout the program)
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
             VALUES(:title, :author, :isbn, :published_date)''' #the ":" colons are for the dictionary in library_app.py
    try:
        with conn:
            conn.execute(sql, book)
    except sqlite3.Error as e:
        print(e)

def update_book(conn, book): # Same as add_book sql injection protection has been implemented and bug on dictionary has been resolved.
    """Updating a book using the ID in the books table with named placeholders."""
    sql = ''' UPDATE books
              SET title = :title,
                  author = :author,
                  isbn = :isbn,
                  published_date = :published_date
              WHERE id = :id'''
    try:
        with conn:
            conn.execute(sql, book)
    except sqlite3.Error as e:
        print(e)



def search_books_by_title(conn, title): #Search query function
  """ Search for books by title. """
  cur = conn.cursor()
  cur.execute("SELECT * FROM books WHERE title LIKE ?", ('%' + title + '%',)) #the like query is for similarity check

  rows = cur.fetchall() #fetchall gets all the data that was found 
  for row in rows:
      print(row)

def delete_book(conn, id): #Deleting a book from the library query
    """ delete a book from the books table by book id. """
    sql = 'DELETE FROM books WHERE id=?' #Deletes based on the ID that the admin has provided 
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

def select_all_books(conn): #Fetching all the books in the library (This is mainly for the API)
    """ querying all rows in the books table. """
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")

    rows = cur.fetchall()
    return rows


def view_books(conn): #Fetching all the books in the library (This is mainly for the CLI)
    """Print all books in the library."""
    books = select_all_books(conn)
    if books:
        print("ID | Title | Author | ISBN | Published Date | Stock Status")
        print("-" * 50)
        for book in books:
            print(f"{book[0]} | {book[1]} | {book[2]} | {book[3]} | {book[4]} | In stock") #Formatting the dictionary
    else:
        print("No books found in the library.")

def select_book_by_id(conn, id): #Getting a book based on the ID 
    """ getting a book by its ID . """
    cur = conn.cursor()
    cur.execute("SELECT * FROM books WHERE id=?", (id,))

    row = cur.fetchone()
    return row

def create_users_table(conn): #Creating a user query
  """ Creating user table in the database. """
  try:
      cursor = conn.cursor()
      cursor.execute(""" CREATE TABLE IF NOT EXISTS users (
                          id INTEGER PRIMARY KEY,
                          username TEXT UNIQUE NOT NULL,
                          password TEXT NOT NULL,
                          role TEXT NOT NULL
                        ); """) #Role, username, password has to be entered also the username is UNIQUE to prevent duplication
      print("Users table created successfully.")
  except sqlite3.Error as e:
      print(e)

def add_user(conn, username, password, role): #Adding a user to the database
  """ Add a new user into the users table. (default role will be user) """
  hashed_password = hashlib.sha256(password.encode()).hexdigest() #hasing the password for data protection
  sql = ''' INSERT INTO users(username, password, role)
            VALUES(?,?,?) '''
  cur = conn.cursor()
  cur.execute(sql, (username, hashed_password, role))
  conn.commit()
  return cur.lastrowid

def login_user(conn, username, password): #Login query function
  """ Validating user logins. """
  hashed_password = hashlib.sha256(password.encode()).hexdigest() #This will hash the password and in the query it will compare it 
  sql = 'SELECT * FROM users WHERE username=? AND password=?'
  cur = conn.cursor()
  cur.execute(sql, (username, hashed_password))
  user = cur.fetchone()
  return user
  
def does_user_exist(conn, username): #Checks if the user exists based on the username
  """ Check if a user already exists in the database. """
  cur = conn.cursor()
  cur.execute("SELECT * FROM users WHERE username=?", (username,))
  return cur.fetchone() is not None

def main():
    database = "library.db"

   
    conn = create_connection(database)

    if conn is not None:

        create_table(conn)


        book = ('Sample Book', 'Author Name', '1234567890', '01-01-2020') #Sample data. However, this is disabled for time being 
        add_book(conn, book)
        select_all_books(conn)

     
        conn.close()
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    main()
