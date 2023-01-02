from datetime import datetime
from util import COLOR_GRAY, COLOR_ITALIC, color_wrap


def add_to_history(event: str):
    history.append({"time": datetime.now(), "event": event})


def print_history(max_lines=9):
    recent_events = history[-max_lines:]

    extra_lines = len(history) - max_lines
    if extra_lines > 0:
        print(color_wrap(f"+{extra_lines} older event(s)", COLOR_ITALIC))
        # Since the "..." takes up one line, we show one less item:
        recent_events.pop(0)

    for item in recent_events:
        time: datetime = item["time"]
        event: str = item["event"]

        time_string = color_wrap(f"[{time.strftime('%X')}]", COLOR_GRAY)
        print(time_string, event)


# Keeps track of all the actions that the user has taken in this session
history = []
