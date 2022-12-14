import json
import random
from menu import create_menu, color_wrap, COLOR_RED
import sys
import inputs


def generate_id(bits=64):
    random_int = random.randint(0, 2**bits)
    return hex(random_int)


def create_child(name: str, score: int, postcode: str, id: str):
    return {"name": name, "score": score, "postcode": postcode, "id": id}


def save_json():
    data = json.dumps(child_database)
    child_database_file = open(child_database_filename, "w", encoding="utf8")
    child_database_file.write(data)
    child_database_file.close()


def write_naughty_and_nice_lists():
    naughty_list_file = open("naughty_list.txt", "w", encoding="utf8")
    nice_list_file = open("nice_list.txt", "w", encoding="utf8")

    for child in child_database:
        pass


def register_new_child():
    def ask_for_data():
        name = inputs.text("Name: ")
        postcode = inputs.text("Postcode: ")  # TODO: Use postcode input helper
        score = inputs.integer("Total score: ")

        id = generate_id()
        return create_child(name, score, postcode, id)

    print("Registering a new child")
    print("Please input their information's")
    child = ask_for_data()
    child_database.append(child)
    save_json()
    print(f"Added a child called {child['name']}")
    print()


child_database_filename = "children.json"
# Load the JSON database file:
try:
    child_database_file_read = open(child_database_filename, "r", encoding="utf8")
    child_database: list = json.load(child_database_file_read)
    child_database_file_read.close()
except FileNotFoundError:
    child_database = []
except json.decoder.JSONDecodeError as error:
    # If the file is empty then just re-create an empty json file
    # Otherwise, notify the user and exit the program
    child_database_file_read = open(child_database_filename, "r", encoding="utf8")
    file_is_empty = child_database_file_read.read(1) == ""
    if file_is_empty:
        child_database = []
    else:
        print(color_wrap("Child database is invalid!", COLOR_RED))
        print(color_wrap(f"Error while parsing JSON: {error}", COLOR_RED))
        sys.exit(10)

print("Welcome to the Christmas Naughty or Nice tool!")
print()

# Main menu
add_option, show_menu = create_menu("Christmas Naughty or Nice")
add_option("Add a child", register_new_child)
show_menu()

# Program shutdown
print("Goodbye!")
save_json()
