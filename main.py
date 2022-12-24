import sys
import json
from util import (
    COLOR_BOLD,
    color_wrap,
    COLOR_RED,
    generate_id,
    print_error,
    print_success,
)
import inputs
from menu import create_menu

# Filename constants
FILE_CHILD_DATABASE = "children.json"
FILE_NAUGHTY_LIST = "naughty_list.txt"
FILE_NICE_LIST = "nice_list.txt"


def create_child(name: str, score: int, postcode: str, id: str):
    return {"name": name, "score": score, "postcode": postcode, "id": id}


def save_json():
    data = json.dumps(child_database)
    child_database_file = open(FILE_CHILD_DATABASE, "w", encoding="utf8")
    child_database_file.write(data)
    child_database_file.close()


def add_child_to_naughty_or_nice_list(
    child,
    naughty_file=open(FILE_NAUGHTY_LIST, "a"),
    nice_file=open(FILE_NICE_LIST, "a"),
):
    line = f"\"{child['name']}\" @ {child['postcode']}"
    is_nice = child["score"] >= 0
    file = nice_file if is_nice else naughty_file
    file.write(line + "\n")
    return file


def rewrite_naughty_and_nice_lists():
    naughty_list_file = open(FILE_NAUGHTY_LIST, "w", encoding="utf8")
    nice_list_file = open(FILE_NICE_LIST, "w", encoding="utf8")

    total_children = 0
    for child in child_database:
        add_child_to_naughty_or_nice_list(child, naughty_list_file, nice_list_file)
        total_children += 1

    print_success(f"Added {total_children} child(ren) to the naughty/nice lists")
    print()


def register_new_child():
    def ask_for_data():
        name = inputs.text("Name: ")
        postcode = inputs.postcode("Postcode: ", "AI")
        score = inputs.integer("Total score: ")

        id = generate_id()
        return create_child(name, score, postcode, id)

    print("Registering a new child")
    print("Please input their information's")
    child = ask_for_data()
    child_database.append(child)
    save_json()
    name = child["name"]
    print_success(f"Added a child called {name}")
    output_file = add_child_to_naughty_or_nice_list(child)
    print_success(f'Added "{name}" to {output_file.name}')
    print()


# Load the JSON database file:
try:
    child_database_file_read = open(FILE_CHILD_DATABASE, "r", encoding="utf8")
    child_database: list = json.load(child_database_file_read)
    child_database_file_read.close()
except FileNotFoundError:
    child_database = []
except json.decoder.JSONDecodeError as error:
    # If the file is empty then just re-create an empty json file
    # Otherwise, notify the user and exit the program
    child_database_file_read = open(FILE_CHILD_DATABASE, "r", encoding="utf8")
    file_is_empty = child_database_file_read.read(1) == ""
    if file_is_empty:
        child_database = []
    else:
        print(print_error("Child database is invalid!"))
        print(print_error(f"Error while parsing JSON: {error}"))
        sys.exit(10)

# Main menu
main_menu_title = color_wrap("Christmas Naughty or Nice".upper(), COLOR_BOLD)
add_option, show_menu = create_menu(main_menu_title)
add_option("Add a child", register_new_child)
add_option("Update naughty/nice lists", rewrite_naughty_and_nice_lists)
show_menu(loop=True, sep="\n")

# Program shutdown
print("Goodbye!")
save_json()
