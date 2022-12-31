from pycountry import countries
import re
from typing import Callable, Union
from util import COLOR_YELLOW, color_wrap, print_error, print_gray
from postcodes import (
    assert_valid_iso_code,
    assert_valid_postcode,
    get_valid_postcode_types,
)


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


def ask_if(condition, prompt, default=None, helper: Callable[[str], str] = input):
    if not condition:
        return default

    return helper(prompt) or default


def yes_no(prompt: str, default="y") -> bool:
    separator = "/"
    options = ["y", "n"]

    formatted_options = [
        option.upper() if option == default else option.lower() for option in options
    ]
    hint = f"({separator.join(formatted_options)})"

    full_prompt = f"{prompt} {hint} "
    raw_input = input(full_prompt).lower().strip()
    if raw_input == "":
        return default == "y"

    if raw_input not in options:
        return yes_no(prompt, default)

    return raw_input == "y"


def text(prompt: str, default=None) -> str:
    """Asks the user for some input and validates that they actually entered something"""
    raw_input = input(prompt)
    if default != None and raw_input == "":
        return default
    if not raw_input:
        print_error("Enter at least one character!")
        return text(prompt)
    return raw_input


def postcode(
    country: str,
    base_prompt="Postcode: ",
    area_prompt="Area postcode: ",
    street_prompt="Street-level postcode: ",
):
    """Asks the user to input a valid postcode"""

    def get_valid_postcode(type: str, prompt) -> str:
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
            return get_valid_postcode(type, prompt)

    valid_postcode_types = get_valid_postcode_types(country)
    if valid_postcode_types == []:
        raise ValueError("Country {country} does not use postcodes!")

    if not valid_postcode_types:
        # Validation isn't supported for the country, so just treat it as a text input
        return text(base_prompt)

    if len(valid_postcode_types) == 1:
        # The country only uses one type of postcode, so just ask for a "postcode"
        valid_type = valid_postcode_types[0]
        return get_valid_postcode(valid_type, base_prompt)

    # The country uses both area and street-level postcodes,
    # so both need to be entered to get a full postcode.
    area_postcode = get_valid_postcode("area", area_prompt)
    street_postcode = get_valid_postcode("street", street_prompt)

    return " ".join([area_postcode, street_postcode])


def integer(prompt: str) -> int:
    raw_input = text(prompt).strip()

    if not is_number(raw_input):
        print_error("You must enter a number!")
        return integer(prompt)
    if not is_int(raw_input):
        print_error("You must enter an integer! (No decimal places)")
        return integer(prompt)

    return int(raw_input)


def house_number_maybe(prompt: str):
    raw_input = input(prompt).strip()
    if raw_input == "":
        return None

    has_digit = re.search("\\d", raw_input)
    if not has_digit:
        confirmed = yes_no(
            color_wrap(
                "Are you sure that this is a house number, not a house name?",
                COLOR_YELLOW,
            )
        )
        return raw_input if confirmed else house_number_maybe(prompt)

    return raw_input


def iso_country(prompt: str):
    raw_input = text(prompt)

    # If it's in the format of an ISO country code, treat it as one
    iso_code_format = re.match("^[A-Z]{2}$", raw_input.upper())
    if iso_code_format:
        raw_input = raw_input.upper()
        try:
            assert_valid_iso_code(raw_input)
            return raw_input
        except ValueError:
            print_error("That's not a valid ISO country code!")
            return iso_country(prompt)

    # Otherwise, treat it as a country name and try to resolve it to an ISO code
    try:
        results = countries.search_fuzzy(raw_input)
    except LookupError:
        print_error(f'Couldn\'t find any countries matching "{raw_input}".')
        return iso_country(prompt)

    country = results[0]
    unsure = len(results) > 1

    if unsure:
        confirmed = yes_no(
            color_wrap(f"Matched to {country.name}. Correct?", COLOR_YELLOW)
        )
        if confirmed:
            return country.alpha_2
        # If the user states that the selected country is incorrect,
        # show them the other matches and let them retry entering a country.
        print_gray("Other possible matches:")
        for country in results:
            print_gray(f" - {country.alpha_2}: {country.name}")
        return iso_country(prompt)

    print_gray(f"Selected country: {country.name} ({country.alpha_2})")
    return country.alpha_2


def address() -> dict[str, Union[str, None]]:
    country = iso_country("Country: ")  # TODO: Validate countries
    city = input("City: ") or None
    street = input("Street: ") or None
    place = ask_if(not street, "Place: ")
    house_number = house_number_maybe("House number: ")
    house_name = input("House name: ") or None

    use_detail = yes_no("Add sub-building detail?", default="n")
    unit = ask_if(use_detail, "Unit: ")
    floor = ask_if(use_detail, "Floor: ")
    chimney = ask_if(use_detail, "Chimney: ")
    full = ask_if(use_detail, "Description: ")

    return {
        "country": country,
        "city": city,
        "street": street,
        "place": place,
        "house_number": house_number,
        "house_name": house_name,
        "unit": unit,
        "floor": floor,
        "chimney": chimney,
        "full": full,
    }
