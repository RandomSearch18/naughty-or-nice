import sys
import json
from addresses import add_coordinates_to_child
from constants import (
    FILE_CHILD_DATABASE,
    FILE_NAUGHTY_LIST,
    FILE_NICE_LIST,
    PROGRAM_NAME,
)
from history import add_to_history, print_history
from letters import personalised_letters
from util import (
    COLOR_BOLD,
    color_wrap,
    generate_id,
    print_error,
    print_heading,
    print_success,
)
import inputs
from menu import create_menu
from child_database import child_database


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


def add_child_to_naughty_or_nice_list(child):
    naughty_file = open(FILE_NAUGHTY_LIST, "a")
    nice_file = open(FILE_NICE_LIST, "a")

    line = f"\"{child['name']}\" @ {child['postcode']}"
    is_nice = child["score"] >= 0
    file = nice_file if is_nice else naughty_file
    file.write(line + "\n")
    file.close()
    return file


def rewrite_naughty_and_nice_lists():
    # Clear both of the files
    for filename in [FILE_NICE_LIST, FILE_NAUGHTY_LIST]:
        open(filename, "w", encoding="utf8").close()

    total_children = 0
    for child in child_database:
        add_child_to_naughty_or_nice_list(child)
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


# Main menu
add_option, show_menu = create_menu(color_wrap(PROGRAM_NAME.upper(), COLOR_BOLD))
add_option("Register a new child", register_new_child)
add_option("Update naughty/nice lists", rewrite_naughty_and_nice_lists)
add_option("Write personalised letters", personalised_letters)
add_option("View history", view_history)
add_option(f"About {PROGRAM_NAME}", view_about)
show_menu(loop=True, sep="\n")

# Program shutdown
print("Goodbye!")
save_json()
