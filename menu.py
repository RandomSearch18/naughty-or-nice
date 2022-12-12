from inspect import signature

# Terminal colour codes
COLOR_RED = "\x1b[31m"

"""Applies an ANSI colour code to a string"""
def color_wrap(string, color):
    return f"{color}{string}\033[0m"

def get_selection(max):
    try:
        raw_input = input("Make a selection: ")
    except KeyboardInterrupt:
        print(color_wrap("Selection cancelled!", COLOR_RED))
        return -1

    if not raw_input.isnumeric():
        print("Your selection must be a positive number!")
        return get_selection(max)

    selection = int(raw_input)
    if selection < 0:
        print("Select a positive number!")
        return get_selection(max)
    if selection > max:
        print("Selection out of bounds: Must be below", max)
        return get_selection(max)

    # Subtract one from the selection, since the user is given options that are
    # indexed from 1, but we want them to be zero-indexed
    selection -= 1
    return selection


"""System for creating a menu with multiple options that the user can pick from"""
def create_menu(title=None):
    options = []

    """Add an option to the menu.
    name: The text that is shown to the user, in the menu
    callback: The function to run when the user selects the option
    show: An optional function that can return False to prevent the option from being shown
    """
    def add_option(name, callback, show=None):
        options.append({"name": name, "callback": callback, "show": show})

    """Show the menu (once you've added all the options)"""
    def show_menu(loop=False):
        """Cleanup functions run once the menu item callback is done, i.e. if the function ends normally or if it's cancelled by the user with ^C. Useful for things like closing files."""
        def add_cleanup(cleanup):
            cleanups.append(cleanup)

        cleanups = []

        relevant_options = []
        for option in options:
            if option["show"]:
                shouldShow = option["show"]()
                if shouldShow:
                    relevant_options.append(option)
            else:
                relevant_options.append(option)

        if len(relevant_options) == 0:
            print("No options available. Goodbye!")
            return

        if title:
            print(title)
        for i, option in enumerate(relevant_options):
            print(f"{i+1}) {option['name']}")

        selection = get_selection(len(relevant_options))
        if selection == -1:
            # Exit the menu if the user entered "0" (to cancel the selection)
            return

        print()
        callback = relevant_options[selection]["callback"]
        try:
            # Only give the callback function an argument if it wants one
            parameters = len(signature(callback).parameters)
            callback() if parameters == 0 else callback(add_cleanup)
        except KeyboardInterrupt:
            message = "Aborting..." if len(cleanups) else "Aborted!"
            print(color_wrap("\n" + message, COLOR_RED))
        finally:
            for cleanup in cleanups:
                cleanup()

        if not loop:
            return
        print("\n")
        show_menu(loop)

    return add_option, show_menu
