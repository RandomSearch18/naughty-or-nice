"""Utility functions for parsing postcodes, and working with two-digit country codes."""

# Possibly-useful websites:
# https://github.com/melwynfurtado/postcode-validator
# https://github.com/FenixEdu/PostCodeTools
# https://pypi.org/project/pgeocode/

from pycountry import countries
import re


def rule(regex: str):
    return rule_raw_regex(f"^{regex}$", regex)


def rule_raw_regex(regex: str, raw_regex=None):
    return {"area": {"type": "regex", "regex": regex, "raw_regex": raw_regex or regex}}


def rule_single(code: str):
    return {"area": {"type": "single", "code": code}}


def rule_country_code():
    return {"area": {"type": "country_code"}}


def rule_prefix(base_rule, prefix, prefix_length, sep):
    return {
        "area": {
            "type": "prefixed",
            "prefix_length": prefix_length,
            "prefix": prefix["area"],
            "main": base_rule["area"],
            "sep": sep,
        }
    }


def rule_country_code_prefix(rule, sep=""):
    return {
        "area": {
            "type": "prefixed",
            "prefix_length": 2,
            "prefix": rule_country_code()["area"],
            "main": rule["area"],
            "sep": sep,
        }
    }


def rule_numbers(count: int):
    # Regex would look like \d{3}
    return rule(f"\\d{{{count}}}")


def rule_split(*parts, join=" "):
    regex_parts = [part["area"]["raw_regex"] for part in parts]
    full_regex = join.join(regex_parts)
    return rule(full_regex)


def add_street_rule(rule, street_rule):
    if isinstance(rule, list):
        # Extract the street rule from each rule in the list
        rule = [rule["area"] for rule in rule]
    elif not rule:
        pass  # Don't try to normalise rules that are are None
    else:
        rule = rule["area"]

    if isinstance(street_rule, list):
        street_rule = [rule["area"] for rule in street_rule]
    elif not street_rule:
        pass
    else:
        street_rule = street_rule["area"]

    full_rule = {"street": street_rule, "area": rule and rule}
    return full_rule


def allow_none(rule):
    rule["allow_none"] = True
    return rule


postcode_rules = {
    "AF": rule_numbers(4),
    "AX": [rule_numbers(5), rule_country_code_prefix(rule_numbers(5), sep="-")],
    "AL": rule_numbers(4),
    "DZ": rule_numbers(5),
    "AS": [rule_numbers(5), rule_split(rule_numbers(5), rule_numbers(4), join="-")],
    "AD": rule_country_code_prefix(rule_numbers(3)),
    "AO": None,
    "AI": rule_single("AI-2640"),
    "AG": None,
    # Doesn't check for valid provinces:
    "AR": add_street_rule(
        rule_numbers(4), [rule_numbers(4), rule("[A-Z]\\d{4}[a-zA-Z]{3}")]
    ),
    "AM": rule_numbers(4),
    "AW": None,
    "AU": rule_numbers(4),
    "AT": rule_numbers(4),
    "AZ": rule_country_code_prefix(rule_numbers(4), sep=" "),
    "BS": None,
    # Valid range is 101..1216:
    "BH": [rule_numbers(3), rule_numbers(4)],
    "BD": rule_numbers(4),
    "BB": rule_country_code_prefix(rule_numbers(5), sep=""),
    "BY": rule_numbers(6),
    "BE": rule_numbers(4),
    "BZ": None,
    "BJ": None,
    "BM": add_street_rule(None, [rule("[A-Z]{2} [0-9]{2}"), rule("[A-Z]{2} [A-Z]{2}")]),
    "BT": rule_numbers(5),
    "BO": None,
    "BQ": None,
    "BA": rule_numbers(5),
    "BW": None,
    "BR": rule_single("BIQQ 1ZZ"),
    "IO": rule_single("BBND 1ZZ"),
    "VG": rule_country_code_prefix(rule_numbers(4)),
    "KH": rule_single("120000"),
    "CM": None,
    # The letters D, F, I, O, Q, and U are not used to avoid confusion with other letters or numbers.
    "CA": rule("[A-Z][0-9][A-Z] [0-9][A-Z][0-9]"),
    "CV": rule_numbers(4),
    "KY": rule_prefix(
        prefix=rule_country_code_prefix(rule_numbers(1)),
        prefix_length=3,
        sep="",
        base_rule=rule_numbers(4),
    ),
    "CF": None,
    "TD": None,
    "CL": [rule_numbers(7), rule_split(rule_numbers(3), rule_numbers(4), join="-")],
    # Macau and Hong Kong don't have postcodes
    "CN": allow_none(rule_numbers(6)),
    "CX": rule_numbers(4),
    "CC": rule_numbers(4),
    "CO": rule_numbers(6),
    "KM": None,
    "CG": None,
    "CD": None,
    "CK": None,
    "CR": add_street_rule(
        rule_numbers(5), rule_split(rule_numbers(5), rule_numbers(4), join="-")
    ),
    "CI": None,
    "HR": rule_numbers(5),
    # The letters CP ("codigo postal") are frequently used before the postal code.
    "CU": rule_numbers(5),
    "CW": None,
    "CY": rule_numbers(4),
    "CZ": rule_split(rule_numbers(3), rule_numbers(2), join=" "),
}


def normalise_postcode_rule(rule):
    if rule == None:
        return {
            "area": [],
            "street": [],
        }

    # If the rule is directly an list, move the list of formats to the `area` key
    if isinstance(rule, list):
        rule = {
            "area": [rule["area"] for rule in rule],
            "street": [],
        }

    # If either the `area` or `street` keys are missing, make them an empty array
    # This also handles either key being `None`
    if "area" not in rule or not rule["area"]:
        rule["area"] = []
    if "street" not in rule or not rule["street"]:
        rule["street"] = []

    # If rule["area"] or rule["street"] isn't a list, make it a single-item list
    for postcode_type in rule:
        format = rule[postcode_type]
        if not isinstance(format, list):
            rule[postcode_type] = [format]

    return rule


normalised_rules = {}
for country in postcode_rules:
    rule = postcode_rules[country]
    normalised_rules[country] = normalise_postcode_rule(rule)


def assert_valid_iso_code(code: str):
    if not code:
        raise ValueError("Provided country code is an empty string!")

    if not re.search("^[A-Z]{2}$", code):
        raise ValueError(
            f'ISO 3166-1 alpha-2 country codes can only contain two uppercase letters, but "{code}" was provided.'
        )

    if not countries.get(alpha_2=code):
        raise ValueError(f"Not an officially-assigned country code: {code}")


def get_valid_postcode_types(country: str):
    assert_valid_iso_code(country)

    if country not in normalised_rules:
        # Postcode rules/info are not (yet) available for this country
        return None

    ruleset = normalised_rules[country]
    valid_types = []

    if ruleset["area"]:
        valid_types.append("area")
    if ruleset["street"]:
        valid_types.append("street")

    return valid_types


def assert_postcode_matches_rule(postcode, rule):
    rule_type = rule["type"]

    # Single-value rules
    if rule_type == "single":
        required_code = rule["code"]
        if postcode == required_code:
            return
        raise ValueError(
            f"The country only has a single postcode ({required_code}), but something else was provided: {postcode}"
        )

    # Regex rules
    if rule_type == "regex":
        expression = rule["regex"]
        if re.search(expression, postcode):
            return
        raise ValueError(
            f"That postcode doesn't match the expected format. Regexp: {rule['raw_regex']}"
        )

    raise NotImplementedError(rule_type)


def check_rules(postcode, rules):
    """Takes a postcode and list of rules to validate it against.
    If it doesn't match any of the rules, returns the error from each rule in a list."""
    errors = []
    for rule in rules:
        try:
            assert_postcode_matches_rule(postcode, rule)
            return  # Success
        except ValueError as error:
            error = error.args[0]
            errors.append(error)
    return errors


# https://en.wikipedia.org/wiki/List_of_postal_codes
def assert_valid_postcode(country: str, postcode: str, type: str = "area"):
    """
    Return codes:
    200 - Valid postcode!
    401 - Country does not use postcodes at all (area and street rules are empty lists)
    402 - Country does not have postcodes in the specified area (rule is an empty list)
    501 - Country not supported (no available postcode rules)
    502 - Postcode rule not supported (rule type didn't match any if statements)
    """
    if not postcode:
        raise ValueError("Provided postcode is empty!")

    assert_valid_iso_code(country)

    rules = normalised_rules
    if not rules[country]:
        return 501

    country_rule = rules[country]
    if not country_rule["area"] and not country_rule["street"]:
        return 401
    if not country_rule[type]:
        return 402

    rules = country_rule[type]

    try:
        errors = check_rules(postcode, rules)
    except NotImplementedError:
        return 502

    postcode_is_valid = not isinstance(errors, list)
    if not postcode_is_valid:
        if not errors:
            raise ValueError("Invalid postcode! Failed to get details of the error.")
        if len(errors) == 1:
            raise ValueError(errors[0])

        message = f"Postcode doesn't match any of the {len(errors)} formats:"
        for error in errors:
            message += f"\n - {error}"
        raise ValueError(message)

    return 200
