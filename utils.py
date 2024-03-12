def validate_date(date_text): 
  """Validation for date format (YYYY-MM-DD).""" #These """ will act as commenting and documentation also
  from datetime import datetime
  try:
      datetime.strptime(date_text, '%Y-%m-%d')
      return True
  except ValueError:
      return False

def input_with_validation(prompt, validation_function):
  """Repeat till input is valid."""
  while True:
      user_input = input(prompt)
      if validation_function(user_input):
          return user_input
      else:
          print("Invalid input, please try again.")

def validate_isbn(isbn):
  """Validating the ISBN format."""
  return len(isbn) in [10, 13]

def format_book_info(book_info):
  """Formating and returning book information in a readable format."""
  return f"ID: {book_info[0]}, Title: {book_info[1]}, Author: {book_info[2]}, ISBN: {book_info[3]}, Published Date: {book_info[4]}"

def validate_positive_integer(number):
  """Ensuring input is a valid integer"""
  try:
      value = int(number)
      return value > 0
  except ValueError:
      return False