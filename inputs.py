from util import print_error
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

    def get_valid_postcode(type: str) -> str:
        raw_input = input(prompt).strip().upper()
        try:
            result = assert_valid_postcode(country, raw_input, type)
            if result == 200:
                pass  # Validation was performed successfully

            elif result == 501:
                print(f"Warning: Postcode validation for {country} is not available.")

            elif result == 502:
                print(
                    f"Warning: Skipped validation because one of the postcode rules for {country} were not understood."
                )

            else:
                print_error(f"Skipped postcode validation due to an error ({result})")

            return raw_input
        except ValueError as error:
            message = "\n".join(error.args)
            print_error(message)
            return get_valid_postcode(type)

    # `None` if postcode validation isn't supported for the country:
    valid_postcode_types = get_valid_postcode_types(country)
    if valid_postcode_types == []:
        raise ValueError("Country {country} does not use postcodes!")

    if valid_postcode_types and "area" not in valid_postcode_types:
        print("Warning: Only area-level postcodes are currently supported.")
        valid_postcode_types = None

    output_postcode = get_valid_postcode("area")

    return output_postcode


def integer(prompt: str) -> int:
    raw_input = text(prompt).strip()

    if not is_number(raw_input):
        print("You must enter a number!")
        return integer(prompt)
    if not is_int(raw_input):
        print("You must enter an integer! (No decimal places)")
        return integer(prompt)

    return int(raw_input)
