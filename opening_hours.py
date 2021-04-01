from datetime import datetime, timezone
from typing import Dict, List

from flask import Flask, abort, request, redirect, url_for

from examples import example_input, example_output

app = Flask(__name__)

ordered_weekdays = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]


def show_shifts_endpoint_instructions():
    return f"""
        <html>
        <head><title>Opening Hours</title></head>
        <body>
            <p>Send POST request with JSON string to parse, e.g.</p>
            <code>curl --header "Content-Type: application/json" \
                  --request POST --data '{example_input}' \
                  http://localhost:5000/shifts</code>
            <p>The result will be as below:</p>
            <pre>{example_output}</pre>
        </body>
        </html>
        """


def validate_shifts(shifts_data: dict) -> List[str]:
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
    """ Converts given weekday shifts in a human-readable format.
    E.g,  'tuesday': ['10 AM - 6 PM'] -> 'Tuesday: 10 AM - 6 PM' """
    opening_hours = ", ".join(day_shifts) if day_shifts else "Closed"
    return f"{weekday.capitalize()}: {opening_hours}"


def format_opening_hours_as_text(shifts_data: dict) -> str:
    week_shifts = parse_hours(shifts_data)
    formatted_shifts = "\n".join(
        format_day_shifts(day, week_shifts[day]) for day in ordered_weekdays)
    return formatted_shifts


@app.route('/')
def index():
    return redirect(url_for('shifts'))


@app.route("/shifts", methods=["GET", "POST"])
def shifts():
    if request.method == "POST":
        json_data = request.get_json()  # raise and return "bad request" if non-valid JSON
        errors = validate_shifts(json_data)
        if errors:
            abort(400, description="\n".join(errors))
        return format_opening_hours_as_text(json_data)
    else:
        return show_shifts_endpoint_instructions()
