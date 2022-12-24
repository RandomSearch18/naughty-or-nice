import random


# Terminal colour codes
COLOR_RED = "\x1b[31m"
COLOR_GREEN = "\x1b[32m"
COLOR_CYAN = "\x1b[36m"
COLOR_GRAY = "\x1b[90m"

COLOR_BOLD = "\x1b[1m"
COLOR_ITALIC = "\x1b[3m"


def color_wrap(string, color):
    """Applies an ANSI colour code to a string"""
    return f"{color}{string}\033[0m"


def print_colored(message_parts: tuple[str], *colors: str, icon: str = ""):
    message = " ".join(message_parts)
    color_string = "".join(colors)
    print(color_wrap(icon + message, color_string))


def print_abort(*msg: str):
    print_colored(msg, COLOR_RED, COLOR_BOLD)


def print_error(*msg: str):
    print_colored(msg, COLOR_RED)


def print_success(*msg: str):
    print_colored(msg, COLOR_GREEN)


def print_info(*msg: str):
    print_colored(msg, COLOR_CYAN, icon="🛈  ")


def generate_id(bits=64):
    random_int = random.randint(0, 2**bits)
    return hex(random_int)
