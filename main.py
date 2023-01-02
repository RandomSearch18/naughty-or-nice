import sys
import json
from datetime import datetime
from addresses import add_coordinates_to_child
from util import (
    COLOR_BOLD,
    COLOR_GRAY,
    COLOR_ITALIC,
    color_wrap,
    generate_id,
    print_error,
    print_heading,
    print_success,
)
import inputs
from menu import create_menu

# Filename constants
FILE_CHILD_DATABASE = "children.json"
FILE_NAUGHTY_LIST = "naughty_list.txt"
FILE_NICE_LIST = "nice_list.txt"


def create_child(name: str, score: int, postcode: str, id: str, address):
    return {
        "name": name,
        "score": score,
        "postcode": postcode,
        "id": id,
        "address": address,
    }


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
    file.close()
    return file


def rewrite_naughty_and_nice_lists():
    naughty_list_file = open(FILE_NAUGHTY_LIST, "w", encoding="utf8")
    nice_list_file = open(FILE_NICE_LIST, "w", encoding="utf8")

    total_children = 0
    for child in child_database:
        add_child_to_naughty_or_nice_list(child, naughty_list_file, nice_list_file)
        total_children += 1

    print_success(f"Added {total_children} child(ren) to the naughty/nice lists")
    add_to_history(f"Updated the naughty/nice lists")


def register_new_child():
    def ask_for_data():
        name = inputs.text("Name: ")
        address = inputs.address()
        postcode = inputs.postcode(address["country"])  # type:ignore
        score = inputs.integer("Total score: ")

        id = generate_id()
        child = create_child(name, score, postcode, id, address)
        add_coordinates_to_child(address, child)
        return child

    print("Registering a new child")
    print("Please input their information's")
    child = ask_for_data()
    child_database.append(child)
    save_json()
    name = child["name"]
    print_success(f'New child registered: "{name}"')
    output_file = add_child_to_naughty_or_nice_list(child)
    print_success(f"Added the child to {output_file.name}")
    add_to_history(f"Registered a child ({name})")


def add_to_history(event: str):
    history.append({"time": datetime.now(), "event": event})


def print_history(max_lines=9):
    recent_events = history[-max_lines:]

    extra_lines = len(history) - max_lines
    if extra_lines > 0:
        print(color_wrap(f"+{extra_lines} older event(s)", COLOR_ITALIC))
        # Since the "..." takes up one line, we show one less item:
        recent_events.pop(0)

    for item in recent_events:
        time: datetime = item["time"]
        event: str = item["event"]

        time_string = color_wrap(f"[{time.strftime('%X')}]", COLOR_GRAY)
        print(time_string, event)


def view_history():
    print_history()
    add_to_history("Viewed the history")


def view_about():
    print_heading("Credits")
    print("Geocoding of child addresses provided by https://nominatim.org/")
    print(
        "Nominatim geocoding uses OpenStreetMap data: https://openstreetmap.org/copyright"
    )
    add_to_history("Viewed the credits")


# Keeps track of all the actions that the user has taken in this session
history = []


# Load the JSON database file:
try:
    database_file = open(FILE_CHILD_DATABASE, "r", encoding="utf8")
    child_database: list = json.load(database_file)
    database_file.close()
    add_to_history("Program launched")
except FileNotFoundError:
    child_database = []
    add_to_history("Program launched for the first time")
except json.decoder.JSONDecodeError as error:
    # If the file is empty then just re-create an empty json file
    # Otherwise, notify the user and exit the program
    database_file = open(FILE_CHILD_DATABASE, "r", encoding="utf8")
    file_is_empty = database_file.read(1) == ""
    if file_is_empty:
        child_database = []
        add_to_history("Program launched with an empty database file")
    else:
        print(print_error("Child database is invalid!"))
        print(print_error(f"Error while parsing JSON: {error}"))
        sys.exit(10)

# Main menu
program_mane = "Christmas Naughty or Nice"
add_option, show_menu = create_menu(color_wrap(program_mane.upper(), COLOR_BOLD))
add_option("Register a new child", register_new_child)
add_option("Update naughty/nice lists", rewrite_naughty_and_nice_lists)
add_option("View history", view_history)
add_option(f"About {program_mane}", view_about)
show_menu(loop=True, sep="\n")

# Program shutdown
print("Goodbye!")
save_json()
