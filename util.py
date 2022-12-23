import random


# Terminal colour codes
COLOR_RED = "\x1b[31m"
COLOR_GREEN = "\x1b[32m"


def color_wrap(string, color):
    """Applies an ANSI colour code to a string"""
    return f"{color}{string}\033[0m"


def print_error(*msg):
    print(color_wrap(" ".join(msg), COLOR_RED))


def print_success(*msg):
    print(color_wrap(" ".join(msg), COLOR_GREEN))


def generate_id(bits=64):
    random_int = random.randint(0, 2**bits)
    return hex(random_int)
