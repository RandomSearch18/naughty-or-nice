
{
    "AF": {
        "area": [{"type": "regex", "regex": "^\\d{4}$", "raw_regex": "\\d{4}"}],
        "street": [],
    },
    "AX": {
        "area": [
            {"type": "regex", "regex": "^\\d{5}$", "raw_regex": "\\d{5}"},
            {
                "type": "prefixed",
                "prefix_length": 2,
                "prefix": {"type": "country_code"},
                "main": {"type": "regex", "regex": "^\\d{5}$", "raw_regex": "\\d{5}"},
                "sep": "-",
            },
        ],
        "street": [],
    },
    "AL": {
        "area": [{"type": "regex", "regex": "^\\d{4}$", "raw_regex": "\\d{4}"}],
        "street": [],
    },
    "DZ": {
        "area": [{"type": "regex", "regex": "^\\d{5}$", "raw_regex": "\\d{5}"}],
        "street": [],
    },
    "AS": {
        "area": [
            {"type": "regex", "regex": "^\\d{5}$", "raw_regex": "\\d{5}"},
            {"type": "regex", "regex": "^\\d{5}-\\d{4}$", "raw_regex": "\\d{5}-\\d{4}"},
        ],
        "street": [],
    },
    "AD": {
        "area": [
            {
                "type": "prefixed",
                "prefix_length": 2,
                "prefix": {"type": "country_code"},
                "main": {"type": "regex", "regex": "^\\d{3}$", "raw_regex": "\\d{3}"},
                "sep": "",
            }
        ],
        "street": [],
    },
    "AO": {"area": [], "street": []},
    "AI": {"area": [{"type": "single", "code": "AI-2640"}], "street": []},
    "AG": {"area": [], "street": []},
    "AR": {
        "street": [
            {
                "type": "regex",
                "regex": "^^\\d{4}|[A-Z]\\d{4}[a-zA-Z]{3}$$",
                "raw_regex": "^\\d{4}|[A-Z]\\d{4}[a-zA-Z]{3}$",
            }
        ],
        "area": [{"type": "regex", "regex": "^\\d{4}$", "raw_regex": "\\d{4}"}],
    },
    "AM": {
        "area": [{"type": "regex", "regex": "^\\d{4}$", "raw_regex": "\\d{4}"}],
        "street": [],
    },
    "AW": {"area": [], "street": []},
    "AU": {
        "area": [{"type": "regex", "regex": "^\\d{4}$", "raw_regex": "\\d{4}"}],
        "street": [],
    },
    "AT": {
        "area": [{"type": "regex", "regex": "^\\d{4}$", "raw_regex": "\\d{4}"}],
        "street": [],
    },
    "AZ": {
        "area": [
            {
                "type": "prefixed",
                "prefix_length": 2,
                "prefix": {"type": "country_code"},
                "main": {"type": "regex", "regex": "^\\d{4}$", "raw_regex": "\\d{4}"},
                "sep": " ",
            }
        ],
        "street": [],
    },
    "BS": {"area": [], "street": []},
    "BH": {
        "area": [
            {"type": "regex", "regex": "^\\d{3}$", "raw_regex": "\\d{3}"},
            {"type": "regex", "regex": "^\\d{4}$", "raw_regex": "\\d{4}"},
        ],
        "street": [],
    },
    "BD": {
        "area": [{"type": "regex", "regex": "^\\d{4}$", "raw_regex": "\\d{4}"}],
        "street": [],
    },
    "BZ": {"area": [], "street": []},
    "BJ": {"area": [], "street": []},
    "BM": {
        "street": [
            {
                "type": "regex",
                "regex": "^\\d{4}|[A-Z]\\d{4}[a-zA-Z]{3}$",
                "raw_regex": "\\d{4}|[A-Z]\\d{4}[a-zA-Z]{3}",
            }
        ],
        "area": [],
    },
    "BT": {
        "area": [{"type": "regex", "regex": "^\\d{5}$", "raw_regex": "\\d{5}"}],
        "street": [],
    },
    "BO": {"area": [], "street": []},
    "BQ": {"area": [], "street": []},
    "BA": {
        "area": [{"type": "regex", "regex": "^\\d{5}$", "raw_regex": "\\d{5}"}],
        "street": [],
    },
    "BW": {"area": [], "street": []},
    "BR": {"area": [{"type": "single", "code": "BIQQ 1ZZ"}], "street": []},
    "IO": {"area": [{"type": "single", "code": "BBND 1ZZ"}], "street": []},
    "VG": {
        "area": [
            {
                "type": "prefixed",
                "prefix_length": 2,
                "prefix": {"type": "country_code"},
                "main": {"type": "regex", "regex": "^\\d{4}$", "raw_regex": "\\d{4}"},
                "sep": "",
            }
        ],
        "street": [],
    },
    "KH": {"area": [{"type": "single", "code": "120000"}], "street": []},
    "CM": {"area": [], "street": []},
    "CA": {
        "area": [
            {
                "type": "regex",
                "regex": "^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$",
                "raw_regex": "[A-Z][0-9][A-Z] [0-9][A-Z][0-9]",
            }
        ],
        "street": [],
    },
    "CV": {
        "area": [{"type": "regex", "regex": "^\\d{4}$", "raw_regex": "\\d{4}"}],
        "street": [],
    },
    "KY": {
        "area": [
            {
                "type": "prefixed",
                "prefix_length": 3,
                "prefix": {
                    "type": "prefixed",
                    "prefix_length": 2,
                    "prefix": {"type": "country_code"},
                    "main": {
                        "type": "regex",
                        "regex": "^\\d{1}$",
                        "raw_regex": "\\d{1}",
                    },
                    "sep": "",
                },
                "main": {"type": "regex", "regex": "^\\d{4}$", "raw_regex": "\\d{4}"},
                "sep": "",
            }
        ],
        "street": [],
    },
    "CF": {"area": [], "street": []},
    "TD": {"area": [], "street": []},
    "CL": {
        "area": [
            {"type": "regex", "regex": "^\\d{7}$", "raw_regex": "\\d{7}"},
            {"type": "regex", "regex": "^\\d{3}-\\d{4}$", "raw_regex": "\\d{3}-\\d{4}"},
        ],
        "street": [],
    },
    "CN": {
        "area": [{"type": "regex", "regex": "^\\d{6}$", "raw_regex": "\\d{6}"}],
        "allow_none": [True],
        "street": [],
    },
    "CX": {
        "area": [{"type": "regex", "regex": "^\\d{4}$", "raw_regex": "\\d{4}"}],
        "street": [],
    },
    "CC": {
        "area": [{"type": "regex", "regex": "^\\d{4}$", "raw_regex": "\\d{4}"}],
        "street": [],
    },
    "CO": {
        "area": [{"type": "regex", "regex": "^\\d{6}$", "raw_regex": "\\d{6}"}],
        "street": [],
    },
    "KM": {"area": [], "street": []},
    "CG": {"area": [], "street": []},
    "CD": {"area": [], "street": []},
    "CK": {"area": [], "street": []},
    "CR": {
        "street": [
            {"type": "regex", "regex": "^\\d{5}-\\d{4}$", "raw_regex": "\\d{5}-\\d{4}"}
        ],
        "area": [{"type": "regex", "regex": "^\\d{5}$", "raw_regex": "\\d{5}"}],
    },
    "CI": {"area": [], "street": []},
    "HR": {
        "area": [{"type": "regex", "regex": "^\\d{5}$", "raw_regex": "\\d{5}"}],
        "street": [],
    },
    "CU": {
        "area": [{"type": "regex", "regex": "^\\d{5}$", "raw_regex": "\\d{5}"}],
        "street": [],
    },
    "CW": {"area": [], "street": []},
    "CY": {
        "area": [{"type": "regex", "regex": "^\\d{4}$", "raw_regex": "\\d{4}"}],
        "street": [],
    },
    "CZ": {
        "area": [
            {"type": "regex", "regex": "^\\d{3} \\d{2}$", "raw_regex": "\\d{3} \\d{2}"}
        ],
        "street": [],
    },
}
