from addresses import address_to_text
from inputs import yes_no
from menu import create_menu
from util import COLOR_BOLD, color_wrap, print_gray, print_success, print_warning
from child_database import child_database
import inputs
import time

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
    end_text = "the end" if range_length == -1 else f"#{range_end}"
    return f"{start_text} to {end_text}"


def generate_letters():
    # If we need a return address: https://www.wikidata.org/wiki/Q25409136
    letters = {}
    total_letters = 0
    start_time = time.time()
    for child in child_database:
        if "address" not in child:
            continue

        letter_text = f"""\
        {address_to_text(child["address"])}
        
        Dear {child["name"]},
        I am writing to inform you that you have been classed as a naughty child this
        year, which has prevented you from receiving any presents. To continue to receive
        Christmas presents, you need to behave well in the upcoming year.

        Yours sincerely,
        Santa Claus"""

        # Use the child's ID as the key in `letters`
        letters[child["id"]] = letter_text
        total_letters += 1

    time_elapsed = time.time() - start_time
    print_success(f"Generated {total_letters} letters in {time_elapsed:.2f} seconds")
    return letters


def select_range():
    global range_start, range_length
    print_gray(f"Current range: {range_string()}")
    if yes_no("Include all children?", default="n"):
        range_start = 0
        range_length = -1
        return

    start = inputs.positive_integer("Start at child #") - 1
    if yes_no(f"Include children from #{start+1} to the end of the list?", default="n"):
        range_start = start
        range_length = -1
        return

    total_children = len(child_database)
    length = inputs.positive_integer("Number of children to include: ")
    excess_children = (start + length) - total_children
    if excess_children > 0:
        print_warning(
            f"Note: There are currently only {total_children} registered children, so {length - excess_children} letters will be produced."
        )
    range_start = start
    range_length = length
    return


def save_to_folder():
    generate_letters()


def personalised_letters():
    add_option, show_menu = create_menu(color_wrap("Personalised Letters", COLOR_BOLD))
    add_option(
        f"Change the range of children",
        select_range,
        loop_after=True,
    )
    add_option("Export letters to a folder", save_to_folder)
    show_menu(sep="\n")
