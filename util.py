from pathlib import Path
import random
from typing import Union


# Terminal colour codes
COLOR_RED = "\x1b[31m"
COLOR_GREEN = "\x1b[32m"
COLOR_CYAN = "\x1b[36m"
COLOR_GRAY = "\x1b[90m"
COLOR_YELLOW = "\x1b[33m"

COLOR_BOLD = "\x1b[1m"
COLOR_ITALIC = "\x1b[3m"


def remove_nullish_values(dict: dict):
    # https://stackoverflow.com/a/33797147
    return {key: value for key, value in dict.items() if value is not None}


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


def print_warning(*msg: str):
    print_colored(msg, COLOR_YELLOW)


def print_success(*msg: str):
    print_colored(msg, COLOR_GREEN)


def print_info(*msg: str):
    print_colored(msg, COLOR_CYAN, icon="🛈  ")


def print_gray(*msg: str):
    print_colored(msg, COLOR_GRAY)


def print_heading(*msg: str):
    print_colored(msg, COLOR_BOLD)


def generate_id(bits=64):
    random_int = random.randint(0, 2**bits)
    return hex(random_int)


def clear_folder(path: Union[str, Path]):
    for item in Path(path).iterdir():
        if item.is_file():
            item.unlink()
