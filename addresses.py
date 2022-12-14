"""Provides functions for working with addresses, e.g. geocoding."""

from typing import Any, Optional
from geopy.geocoders import Nominatim
from inputs import yes_no, address as address_input
from pycountry import countries

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


def geocode_postcode(postcode, country) -> Optional[Any]:
    return geolocator.geocode({"postalcode": postcode, "country": country})


def coordinates_from_address(address):
    result = geocode_address(address)

    if not result:
        raise LookupError()

    return [result.latitude, result.longitude]  # type:ignore


def add_coordinates_to_child(address, child):
    """Return codes:
    200 - Geocoding succeeded and coordinates have been added.
    301 - Added coordinates from postcode
    302 - Added coordinates from city
    """

    def ask_to_edit_address():
        if not yes_no("Do you want to edit the address?"):
            return False
        new_address = address_input()
        child["address"] = new_address
        return add_coordinates_to_child(new_address, child)

    def add_coordinates(location):
        print_gray("Found address match:")
        print_gray(location.address)
        child["coordinates"] = [location.latitude, location.longitude]

    result = geocode_address(address)

    if not result:
        print_gray("Looking up the following address:")
        if address["street"]:
            print_gray(f'  {address["street"]},')
        if address["city"]:
            print_gray(f'  {address["city"]},')
        print_gray(f'  Country: {address["country"]}')
        print_error("Address lookup failed! (No results)")

        edited_address = ask_to_edit_address()
        if edited_address:
            return edited_address

        if yes_no("Do you want to use the postcode to get coordinates?"):
            postcode_result = geocode_postcode(child["postcode"], address["country"])
            if postcode_result:
                add_coordinates(postcode_result)
                return 301
            print_error(f"Couldn't find the postcode {child['postcode']}!")

        if address["street"]:
            print(
                f"You can ignore the child's street and just use the city ({address['city']}) to get coordinates. This may be useful in poorly-mapped areas."
            )
            if yes_no("Get coordinates from the city?", default="n"):
                city_result = geolocator.geocode(
                    {"city": address["city"], "country": address["country"]}
                )
                if city_result:
                    add_coordinates(city_result)
                    return 302
                print_error(f"Couldn't find the city {address['city']}!")

        print_error("Still couldn't find the address!")
        print("You can register the child without an address, or edit the address.")
        edited_address = ask_to_edit_address()
        if edited_address:
            return edited_address

        return

    add_coordinates(result)
    return 200


def address_to_text(address, postcode=""):
    parts = []

    # SUB-BUILDING ADDRESS LINES
    if address["full"]:
        parts.append(address["full"])
    if address["chimney"]:
        parts.append(f'Chimney {address["chimney"]}')
    if address["floor"]:
        parts.append(f'Floor {address["floor"]}')
    if address["unit"]:
        parts.append(f'Unit {address["unit"]}')

    # STREET-LEVEL ADDRESS LINES
    # House names go on their own line, but house numbers go next to the road name
    if address["house_name"]:
        parts.append(address["house_name"])
        if address["street"]:
            parts.append(address["street"])
    elif address["house_number"]:
        # Only use the house number if there isn't a house name
        house_line = address["house_number"]
        if address["street"]:
            house_line += " " + address["street"]
        elif address["place"]:
            house_line += " " + address["place"]
        parts.append(house_line)

    # REGIONAL/NATIONAL ADDRESS LINES
    if address["city"]:
        parts.append(address["city"])
    if postcode:
        parts.append(postcode)

    try:
        country = countries.get(alpha_2=address["country"])
        parts.append(country.name.upper())
    except:
        # Just in case countries.get() fails for some reason
        parts.append(address["country"])

    return ",\n".join(parts)
