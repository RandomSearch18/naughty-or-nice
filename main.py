import json
import random


def generate_id(bits=64):
    return random.randint(0, 2**bits)


def create_child(name: str, score: int, postcode: str, id: str):
    return {
        "name": name,
        "score": score,
        "postcode": postcode,
        "id": id
    }


def save_json():
    json.dump(child_database, child_database_file)


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


child_database_filename = "children.json"
# Load the JSON database file:
# TODO: Create the file if it doesn't exist
child_database_file_read = open(child_database_filename, "r", encoding="utf8")
child_database: list = json.load(child_database_file_read)
child_database_file_read.close()
# Open the database file for writing:
child_database_file = open(child_database_filename, "w", encoding="utf8")

# TODO: Get menu system from Replit
register_new_child()

# Program shutdown
child_database_file.close()
