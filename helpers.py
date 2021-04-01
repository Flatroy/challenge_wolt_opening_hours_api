from datetime import datetime, timezone
from typing import List, Dict

ordered_weekdays = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]


def validate_shifts(shifts_data: dict) -> List[str]:
    """ Validate if given shifts data has all the required fields and values """
    errors = list()
    for day in ordered_weekdays:
        if day not in shifts_data:
            errors.append(f"'{day}' data missed in JSON input")
        else:
            for hours in shifts_data[day]:
                if ("type" not in hours or
                        "value" not in hours or
                        hours["type"] not in ("open", "close") or
                        not isinstance(hours["value"], int)):
                    errors.append(f"'{day}' has invalid hours data")
    return errors


def str_time(unix_ts: int) -> str:
    """ Parse Unix timestamp as UTC datetime and convert to human readable string
    e.g, 64800 -> "6 PM"
         3600 -> "1 AM"
    """
    return datetime.fromtimestamp(unix_ts, timezone.utc).strftime("%-I %p")


def parse_hours(shifts_data: Dict[str, List[Dict[str, str or int]]]) -> Dict[str, List[str]]:
    """ Parse hours from given shifts data and combine them into open-close time pairs (shifts) """
    day_shifts = dict()
    open_day, open_time, close_time, close_overflow = None, None, None, None

    for day in ordered_weekdays:
        day_shifts[day] = list()
        for hours in shifts_data[day]:
            if hours["type"] == "open":
                open_time = str_time(hours["value"])
                open_day = day
            elif hours["type"] == "close":
                close_time = str_time(hours["value"])
                if open_time is not None:
                    day_shifts[open_day].append(f"{open_time} - {close_time}")
                else:
                    close_overflow = close_time

    if close_overflow:
        day_shifts[open_day].append(f"{open_time} - {close_overflow}")

    return day_shifts


def format_day_shifts(weekday: str, day_shifts: List[str]) -> str:
    """ Convert given weekday shifts in a human-readable format.
    E.g,  'tuesday': ['10 AM - 6 PM'] -> 'Tuesday: 10 AM - 6 PM' """
    opening_hours = ", ".join(day_shifts) if day_shifts else "Closed"
    return f"{weekday.capitalize()}: {opening_hours}"


def format_opening_hours_as_text(shifts_data: dict) -> str:
    """ Format opening hours data for each weekday into a single human-readable string representation """
    week_shifts = parse_hours(shifts_data)
    formatted_shifts = "\n".join(
        format_day_shifts(day, week_shifts[day]) for day in ordered_weekdays)
    return formatted_shifts
