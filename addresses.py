"""Provides functions for working with addresses, e.g. geocoding."""

from typing import Any, Optional
from geopy.geocoders import Nominatim
from inputs import yes_no, address as address_input

from util import print_error, print_gray, remove_nullish_values

geolocator = Nominatim(
    user_agent="Christmas Naughty or Nice: https://github.com/RandomSearch18/naughty-or-nice"
)


def geocode_address(address) -> Optional[Any]:
    house_label = address["house_number"] or address["house_name"] or None
    street_line = (
        f'{house_label} {address["street"]}' if house_label else address["street"]
    )

    results = geolocator.geocode(
        remove_nullish_values(
            {
                "country": address["country"],
                "city": address["city"],
                "street": street_line,
                # Postcodes aren't included because Nominatim's support for them is practically nonexistent
                # https://wiki.openstreetmap.org/wiki/Nominatim/FAQ#My_postcode_is_missing.2Fwrong_but_I.27ve_fixed_it_in_the_OSM_data._What_is_wrong.3F
            }
        )
    )  # type: ignore

    if results:
        return results

    # If the first search returned nothing, we try excluding the house name/number.
    # This means that we can at least find the correct road, if not the correct house
    return geolocator.geocode(
        remove_nullish_values(
            {
                "country": address["country"],
                "city": address["city"],
                "street": address["street"],
            }
        )
    )


def geocode_postcode(postcode) -> Optional[Any]:
    return geolocator.geocode({"postalcode": postcode})


def coordinates_from_address(address):
    result = geocode_address(address)

    if not result:
        raise LookupError()

    return [result.latitude, result.longitude]  # type:ignore


def add_coordinates_to_child(address, child):
    """Return codes:
    200 - Geocoding succeeded and coordinates have been added.
    301 - Added coordinates from postcode
    """

    def ask_to_edit_address():
        if not yes_no("Do you want to edit the address?"):
            return
        new_address = address_input()
        child["address"] = new_address
        return add_coordinates_to_child(new_address, child)

    def add_coordinates(location):
        child["coordinates"] = [location.latitude, location.longitude]

    result = geocode_address(address)

    if not result:
        print_gray("Looking up the following address:")
        print_gray(f'  {address["street"]},')
        print_gray(f'  {address["city"]},')
        print_gray(f'  Country: {address["country"]}')
        print_error("Address lookup failed! (No results)")

        ask_to_edit_address()

        if yes_no("Do you want to use the postcode to get coordinates?"):
            postcode_result = geocode_postcode(child["postcode"])
            if postcode_result:
                add_coordinates(postcode_result)
                return 301
            print_error(f"Couldn't look up the postcode {child['postcode']}!")

        if address["street"]:
            print(
                f"You can ignore the child's street and just use the city ({address['city']}) to get coordinates. This may be useful in poorly-mapped areas."
            )
            if yes_no("Get coordinates from the city?", default="n"):
                pass  # TODO

        print("Still couldn't look up the address!")
        print("You can register the child without an address, or edit the address.")
        ask_to_edit_address()

        return

    print_gray("Found address match:")
    print_gray(result.address)
    add_coordinates(result)
    return 200
