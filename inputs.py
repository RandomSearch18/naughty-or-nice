def text(prompt, default=None):
    """Asks the user for some input and validates that they actually entered something"""
    raw_input = input(prompt)
    if default != None and raw_input == "":
        return default
    if not raw_input:
        print("Enter at least one character!")
        return text(prompt)
    return raw_input


def postcode(prompt):
    """Asks the user to input a postcode"""
