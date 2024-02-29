import database_manager as dbm

def display_menu(options): #Displaying the options from the dictionaries
    print("\n".join([f"{key} - {value['text']}" for key, value in options.items()]))

def get_user_input(prompt, cast_to=str, validation=None): #Getting the user input 
    while True:
        user_input = input(prompt)
        try:
            value = cast_to(user_input)
            if validation and not validation(value):
                raise ValueError
            return value
        except ValueError:
            print("Invalid input, please try again.")

def add_book(conn):
    """ Add book menu inputs """
    book_details = { # Made it more robust by making it dictionary based (Javascript experience)
        'title': input("Enter the title of the book: "),
        'author': input("Enter the author of the book: "),
        'isbn': input("Enter the ISBN of the book: "),
        'published_date': input("Enter the published date of the book (YYYY-MM-DD): ")
    }
    dbm.add_book(conn, book_details)

def update_book(conn):
    """ update  book menu inputs """
    book_id = get_user_input("Enter the ID of the book to update: ", int)
    book_details = { # Made it more robust by making it dictionary based (Javascript experience)
        'title': input("Enter the new title of the book: "),
        'author': input("Enter the new author of the book: "),
        'isbn': input("Enter the new ISBN of the book: "),
        'published_date': input("Enter the new published date of the book (DD-MM-YEAR): "),
        'id': book_id
    }
    dbm.update_book(conn, book_details)

def delete_book(conn):
    """ delete book menu inputs """
    book_id = get_user_input("Enter the ID of the book to delete: ", int)
    dbm.delete_book(conn, book_id)

def view_books(conn):
    """ Getting all the books with the query """
    dbm.view_books(conn)

def search_books(conn):
    """ Search book input """
    title = input("Enter the title of the book to search: ")
    dbm.search_books_by_title(conn, title)

def admin_actions(conn): #Admin panel functionalities
    """ Admin panel inputs """
    admin_options = {  # Made it more robust by making it dictionary based
        '1': {'text': 'Add new book', 'action': lambda: add_book(conn)},
        '2': {'text': 'Update book Information', 'action': lambda: update_book(conn)},
        '3': {'text': 'Delete book', 'action': lambda: delete_book(conn)},
        '4': {'text': 'View all books', 'action': lambda: view_books(conn)},
        '5': {'text': 'Search books by title', 'action': lambda: search_books(conn)},
        '6': {'text': 'Exit', 'action': None}
    }

    while True: 
        """ Admin menu """
        print("\nWelcome to the admin menu")
        display_menu(admin_options)
        choice = input("Enter your choice: ")
        if choice in admin_options:
            if choice == '6':
                break
            admin_options[choice]['action']()
        else:
            print("Invalid choice. Please try again.")

def user_actions(conn): # User panel abilities. 
    """ User panel actions abilities """
    user_options = {
        '1': {'text': 'View all books', 'action': lambda: view_books(conn)},
        '2': {'text': 'Search for a book', 'action': lambda: search_books(conn)},
        '3': {'text': 'Exit', 'action': None}
    }

    while True:
        print("\nWelcome to the library")
        display_menu(user_options)
        choice = input("Enter your choice: ")
        if choice in user_options:
            if choice == '3':
                break
            user_options[choice]['action']()
        else:
            print("Invalid choice. Please try again.")

def register_user(conn):
    """ User registeration panel """
    username = input("Enter new username: ")
    password = input("Enter new password: ")
    role = "user"
    dbm.add_user(conn, username, password, role)
    print("Registration successful.")

def login(conn):
    """User login panel """
    username = input("Username: ")
    password = input("Password: ")
    user = dbm.login_user(conn, username, password)
    if user:
        print(f"Welcome back, {username}!")
    else:
        print("Invalid login.")
    return user

def main_menu(conn):
    """ Main menu of the application """
    options = {
        '1': {'text': 'Login', 'action': lambda: login(conn)},
        '2': {'text': 'Register', 'action': lambda: register_user(conn)},
        '3': {'text': 'Exit', 'action': None}
    }

    while True: # """ for the string could be used but this is much cleaner I believe.
        print("\nWelcome to the library system\n1. Login\n2. Register\n3. Exit")
        choice = input("Choose an option: ")
        if choice in options:
            if choice == '3':
                print("Exiting the system.")
                break
            user = options[choice]['action']()
            if user and user[3] == "admin":
                admin_actions(conn)
            elif user:
                user_actions(conn)
        else:
            print("Invalid choice. Please try again.")

def main():
    """ Database connections """
    database = "library.db"
    conn = dbm.create_connection(database)
    if conn is not None:
        dbm.create_table(conn)  
        dbm.create_users_table(conn)  
        if not dbm.does_user_exist(conn, "admin"):
            dbm.add_user(conn, "admin", "admin123", "admin") # If admin doesnt exist in the database this will be the default one just in case. A functionality could be added to change user roles in the admin panel.
        main_menu(conn)
        conn.close()
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    main()
