''' Custom exception for the Movies_CRUD program '''

class NotFoundError(Exception):         # Define a custom exception type for records that was not found in the database
    ''' A custom exception type for records that was not found in the database '''
    def __init__(self, value):
        self.value = value

class RatingError(Exception):           # Define a custom exception type for ratings that was over 5.0      
    ''' A custom exception type for ratings that was over 10.0 '''
    def __init__(self, value):
        self.value = value

class MatchedValueError(Exception):     # Define a custom exception type for entry that was not updated and therefore remained unchanged 
    ''' A custom exception type for entry that was not updated and therefore remained unchanged '''
    def __init__(self, value):
        self.value = value

class GenresLimitError(Exception):      # Define a custom exception type for exceeding the limit of allowed selected genres
    ''' A custom exception type for exceeding the limit of allowed selected genres'''
    def __init__(self, value):          # (Genres limit: 5 genres per movie)
        self.value = value

class IDChangeError(Exception):         # Define a custom exception type that prevents users from changing the ID
    ''' A custom exception type that prevents users from changing the ID '''
    def __init__(self, value):         
        self.value = value

class IncompleteEntryError(Exception):  # Define a custom exception type that handles incomplete user entry
    ''' A custom exception type that handles incomplete user entry '''
    def __init__(self, value):         
        self.value = value

class NoSelectedItemError(Exception):   # Define a custom exception type that is raised when no record is selected
    ''' A custom exception type that is raised when no record is selected '''
    def __init__(self, value):         
        self.value = value
