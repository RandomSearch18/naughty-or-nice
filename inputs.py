from postcodes import assert_valid_postcode, get_valid_postcode_types


def is_int(string: str):
    try:
        int(string)
        return True
    except:
        return False


def is_float(string: str):
    try:
        float(string)
        return True
    except:
        return False


def is_number(string: str):
    return is_int(string) or is_float(string)


def text(prompt: str, default=None) -> str:
    """Asks the user for some input and validates that they actually entered something"""
    raw_input = input(prompt)
    if default != None and raw_input == "":
        return default
    if not raw_input:
        print("Enter at least one character!")
        return text(prompt)
    return raw_input


def postcode(prompt: str, country: str):
    """Asks the user to input a valid postcode"""
    use_validation = True

    valid_postcode_types = get_valid_postcode_types(country)
    if valid_postcode_types == None:
        use_validation = False
    if valid_postcode_types == []:
        raise ValueError("Country {country} does not use postcodes!")

    if use_validation and "street" in valid_postcode_types:
        pass

    # raw_input = input(prompt).strip().upper()
    # assert_valid_postcode(country, raw_input)
    return "TEST POSTCODE"


def integer(prompt: str) -> int:
    raw_input = text(prompt).strip()

    if not is_number(raw_input):
        print("You must enter a number!")
        return integer(prompt)
    if not is_int(raw_input):
        print("You must enter an integer! (No decimal places)")
        return integer(prompt)

    return int(raw_input)
