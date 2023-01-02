import json
import sys
from constants import FILE_CHILD_DATABASE
from history import add_to_history
from util import print_error


def get_child(id: str):
    # Linear search FTW
    for child in child_database:
        if child["id"] == id:
            return child

    raise LookupError(f"Couldn't find a child with ID {id}")


child_database: list = []

try:
    database_file = open(FILE_CHILD_DATABASE, "r", encoding="utf8")
    child_database = json.load(database_file)
    database_file.close()
    add_to_history("Program launched")
except FileNotFoundError:
    add_to_history("Program launched for the first time")
except json.decoder.JSONDecodeError as error:
    # If the file is empty then just re-create an empty json file
    # Otherwise, notify the user and exit the program
    database_file = open(FILE_CHILD_DATABASE, "r", encoding="utf8")
    file_is_empty = database_file.read(1) == ""
    if file_is_empty:
        add_to_history("Program launched with an empty database file")
    else:
        print(print_error("Child database is invalid!"))
        print(print_error(f"Error while parsing JSON: {error}"))
        sys.exit(10)
