from typing import List

from flask import Flask, abort, request, redirect, url_for

from examples import example_input, example_output

app = Flask(__name__)

weekday_order = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}


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
    for day in weekday_order:
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

        return json_data
    else:
        return show_shifts_endpoint_instructions()
