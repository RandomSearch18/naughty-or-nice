"""Asks the user for some input and validates that they actually entered something"""
def text(prompt, default=None):
    raw_input = input(prompt)
    if default != None and raw_input == "":
        return default
    if not raw_input:
        print("Enter at least one character!")
        return text(prompt)
    return raw_input

"""Asks the user for their name. Returns their input in title case."""
def name():
    raw_input = input("Enter your name: ")
    if len(raw_input) < 1:
        print("Your name must be at least one letter!")
        return name()
    return raw_input.title()
