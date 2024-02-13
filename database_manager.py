import database_manager as dbm

def display_admin_menu():
    print("""
          Welcome to the admin menu
          1 - Add new book
          2 - Update book Information
          3 - Delete book
          4 - View all books
          5 - Exit
    """)

def display_user_menu():
    print("""
          Welcome to the library
          1 - View all books
          2 - Search for a book
          3 - Exit
    """)

def register_user(conn):
    username = input("Enter new username: ")
    password = input("Enter new password: ")
    role = "user"  
    dbm.add_user(conn, username, password, role)

def login(conn):
    username = input("Username: ")
    password = input("Password: ")
    user = dbm.login_user(conn, username, password)
    return user

def admin_actions(conn):
  while True:
      display_admin_menu()
      choice = input("Enter your choice: ")
      if choice == '1':
          title = input("Enter the title of the book: ")
          author = input("Enter the author of the book: ")
          isbn = input("Enter the ISBN of the book: ")
          published_date = input("Enter the published date of the book (YYYY-MM-DD): ")
          book = (title, author, isbn, published_date)
          dbm.add_book(conn, book)
      elif choice == '2':
          book_id = int(input("Enter the ID of the book to update: "))
          title = input("Enter the new title of the book: ")
          author = input("Enter the new author of the book: ")
          isbn = input("Enter the new ISBN of the book: ")
          published_date = input("Enter the new published date of the book (YYYY-MM-DD): ")
          book = (title, author, isbn, published_date, book_id)
          dbm.update_book(conn, book)
      elif choice == '3':
          book_id = int(input("Enter the ID of the book to delete: "))
          dbm.delete_book(conn, book_id)
      elif choice == '4':
          dbm.select_all_books(conn)
  
      elif choice == '5': 
          break
      else:
          print("Invalid choice. Please try again.")

def user_actions(conn):
    while True:
        display_user_menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            dbm.select_all_books(conn)
        elif choice == '2':
            book_id = int(input("Enter the ID of the book to search: "))
            book = dbm.select_book_by_id(conn, book_id)
            print(book)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    database = "library.db"
    conn = dbm.create_connection(database)

    if conn is not None:
        dbm.create_table(conn) 
        dbm.create_users_table(conn) 
        if not dbm.does_user_exist(conn, "admin"):
          dbm.add_user(conn, "admin", "admin123", "admin")
        while True:
            print("1. Login\n2. Register\n3. Exit")
            choice = input("Choose an option: ")
            if choice == '1':
                user = login(conn)
                if user:
                    if user[3] == "admin": 
                        admin_actions(conn)
                    else:
                        user_actions(conn)
                else:
                    print("Invalid login.")
            elif choice == '2':
                register_user(conn)
            elif choice == '3':
                print("Exiting the system.")
                break

        conn.close()
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    main()
