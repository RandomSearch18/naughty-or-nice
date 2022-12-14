"""Utility functions for parsing postcodes, and working with two-digit country codes."""

# Possibly-useful websites:
# https://github.com/melwynfurtado/postcode-validator
# https://github.com/FenixEdu/PostCodeTools
# https://pypi.org/project/pgeocode/

import re

# A list of all currently-valid ISO 3166-1 alpha-2 country codes. Doesn't include transitional codes.
# Source: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Decoding_table
VALID_ISO_CODES = [
    "AD",
    "AE",
    "AF",
    "AG",
    "AL",
    "AM",
    "AO",
    "AQ",
    "AR",
    "AS",
    "AT",
    "AU",
    "AW",
    "AX",
    "AZ",
    "BA",
    "BB",
    "BD",
    "BE",
    "BF",
    "BG",
    "BH",
    "BI",
    "BJ",
    "BL",
    "BM",
    "BN",
    "BO",
    "BR",
    "BS",
    "BT",
    "BV",
    "BW",
    "BY",
    "BZ",
    "CA",
    "CC",
    "CD",
    "CF",
    "CG",
    "CH",
    "CI",
    "CK",
    "CL",
    "CM",
    "CN",
    "CO",
    "CR",
    "CU",
    "CV",
    "CW",
    "CX",
    "CY",
    "CZ",
    "DE",
    "DJ",
    "DK",
    "DM",
    "DO",
    "DZ",
    "EC",
    "EE",
    "EG",
    "EH",
    "ER",
    "ES",
    "ET",
    "FI",
    "FJ",
    "FK",
    "FM",
    "FO",
    "FR",
    "GA",
    "GB",
    "GD",
    "GF",
    "GG",
    "GH",
    "GI",
    "GL",
    "GM",
    "GN",
    "GP",
    "GQ",
    "GR",
    "GS",
    "GT",
    "GU",
    "GW",
    "GY",
    "HK",
    "HM",
    "HN",
    "HR",
    "HT",
    "HU",
    "ID",
    "IE",
    "IL",
    "IM",
    "IN",
    "IO",
    "IQ",
    "IR",
    "IS",
    "IT",
    "JE",
    "JM",
    "JO",
    "JP",
    "KE",
    "KG",
    "KH",
    "KI",
    "KM",
    "KN",
    "KP",
    "KR",
    "KW",
    "KY",
    "KZ",
    "LA",
    "LB",
    "LC",
    "LI",
    "LK",
    "LR",
    "LS",
    "LU",
    "LV",
    "LY",
    "MA",
    "MC",
    "MD",
    "MF",
    "MG",
    "MH",
    "MK",
    "ML",
    "MM",
    "MN",
    "MO",
    "MP",
    "MQ",
    "MR",
    "MS",
    "MT",
    "MU",
    "MV",
    "MW",
    "MX",
    "MY",
    "MZ",
    "NA",
    "NC",
    "NE",
    "NF",
    "NG",
    "NI",
    "NL",
    "NO",
    "NP",
    "NR",
    "NU",
    "NZ",
    "OM",
    "PA",
    "PE",
    "PF",
    "PG",
    "PH",
    "PK",
    "PL",
    "PM",
    "PN",
    "PR",
    "PS",
    "PT",
    "PW",
    "PY",
    "QA",
    "RE",
    "RO",
    "RS",
    "RW",
    "SA",
    "SB",
    "SC",
    "SD",
    "SE",
    "SG",
    "SH",
    "SI",
    "SJ",
    "SL",
    "SM",
    "SN",
    "SO",
    "SR",
    "SS",
    "ST",
    "SV",
    "SX",
    "SY",
    "SZ",
    "TC",
    "TD",
    "TF",
    "TG",
    "TH",
    "TJ",
    "TK",
    "TL",
    "TM",
    "TN",
    "TO",
    "TR",
    "TT",
    "TV",
    "TW",
    "TZ",
    "UA",
    "UG",
    "UM",
    "US",
    "UY",
    "UZ",
    "VA",
    "VC",
    "VE",
    "VG",
    "VI",
    "VN",
    "VU",
    "WF",
    "WS",
    "YE",
    "YT",
    "ZA",
    "ZM",
    "ZW",
    "AI",
    "BQ",
    "GE",
    "LT",
    "ME",
    "RU",
    "SK",
]


def rule(regex: str):
    return {"area": {"type": "regex", "regex": f"^{regex}$", "raw_regex": regex}}


def rule_single(code: str):
    return {"area": {"type": "single", "code": code}}


def rule_country_code():
    return {"area": {"type": "country_code"}}


def rule_country_code_prefix(rule, sep=""):
    return {
        "area": {
            "type": "prefixed",
            "prefix_length": 2,
            "prefix": rule_country_code()["area"],
            "main": rule,
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
    full_rule = {"street": street_rule["area"], "area": rule and rule["area"]}
    return full_rule


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
    "AR": add_street_rule(rule_numbers(4), rule("^\\d{4}|[A-Z]\\d{4}[a-zA-Z]{3}$")),
    "AM": rule_numbers(4),
    "AW": None,
    "AU": rule_numbers(4),
    "AT": rule_numbers(4),
    "AZ": rule_country_code_prefix(rule_numbers(4), sep=" "),
    "BS": None,
    # Valid range is 101..1216:
    "BH": [rule_numbers(3), rule_numbers(4)],
    "BD": rule_numbers(4),
    "BZ": None,
    "BJ": None,
    # Bermuda is weird:
    "BM": add_street_rule(None, rule("\\d{4}|[A-Z]\\d{4}[a-zA-Z]{3}")),
    "BT": rule_numbers(5),
    "BO": None,
    "BQ": None,
    "BA": rule_numbers(5),
    "BW": None,
    "BR": rule_single("BIQQ 1ZZ"),
    "IO": rule_single("BBND 1ZZ"),
    "VG": rule_country_code_prefix(rule_numbers(4)),
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
            f"ISO 3166-1 alpha-2 country codes can only contain two uppercase letters: {code}"
        )

    if code not in VALID_ISO_CODES:
        raise ValueError(f"Not an officially-assigned country code: {code}")


# https://en.wikipedia.org/wiki/List_of_postal_codes
def assert_valid_postcode(country: str, postcode: str):
    if not postcode:
        raise ValueError("Provided postcode is empty!")

    assert_valid_iso_code(country)
