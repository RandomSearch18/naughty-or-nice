import json
import random
from menu import create_menu


def generate_id(bits=64):
    return random.randint(0, 2**bits)


def create_child(name: str, score: int, postcode: str, id: str):
    return {"name": name, "score": score, "postcode": postcode, "id": id}


def save_json():
    data = json.dumps(child_database)
    child_database_file = open(child_database_filename, "w", encoding="utf8")
    child_database_file.write(data)
    child_database_file.close()


def register_new_child():
    def ask_for_data():
        # TODO: Use input helpers from Replit
        name = input("Name: ")
        postcode = input("Postcode: ")
        score = int(input("Total score: "))

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
# TODO: Create the file if it doesn't exist
child_database_file_read = open(child_database_filename, "r", encoding="utf8")
child_database: list = json.load(child_database_file_read)
child_database_file_read.close()


print("Welcome to the Christmas Naughty or Nice tool!")
print()

# Main menu
add_option, show_menu = create_menu("Christmas Naughty or Nice")
add_option("Add a child", register_new_child)
show_menu()

# Program shutdown
print("Goodbye!")
