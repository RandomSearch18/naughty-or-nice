import json

# TODO: Get menu system from Replit


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

        return create_child(name, score, postcode)

    print("Registering a new child")
    print("Please input their information's")
    child = ask_for_data()


child_database_file = open("children.json", "w")
child_database = json.load(child_database_file)

register_new_child()
