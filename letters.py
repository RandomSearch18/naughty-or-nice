from inputs import yes_no
from menu import create_menu
from util import COLOR_BOLD, color_wrap, print_gray
import inputs

LETTERS_FOLDER = "letters"

# By default, send a letter
# to kids from one to ninety-two
# (zero-indexed)
range_start = 0
range_length = 92


def range_string():
    range_end = range_start + range_length

    if range_start == 0 and range_length == -1:
        return "All children"

    start_text = f"#{range_start + 1}"
    end_text = "the end" if range_length == -1 else f"#{range_end + 1}"
    return f"{start_text} to {end_text}"


def select_range():
    global range_start, range_end
    print_gray(f"Current range: {range_string()}")
    if yes_no("Include all children?", default="n"):
        range_start = 0
        range_end = -1
        return

    start = inputs.positive_integer("Start at child #") - 1
    if yes_no(f"Include children from #{start} to the end of the list?", default="n"):
        range_start = start
        range_end = -1
        return

    end = inputs.positive_integer("End at child #")
    range_start = start
    range_end = end
    return


def personalised_letters():
    add_option, show_menu = create_menu(color_wrap("Personalised Letters", COLOR_BOLD))
    add_option(
        f"Change the range of children ({range_string()})",
        select_range,
        loop_after=True,
    )
    # add_option("Export letters to a folder", save_to_folder)
    show_menu(sep="\n")
