import json
import unittest

import helpers
import opening_hours
from examples import example_input, example_output


class TestOpeningHoursHandlers(unittest.TestCase):
    def test_shifts_handler_post_valid_input(self):
        input_data = json.loads(example_input)
        with opening_hours.app.test_client() as c:
            resp = c.post("/shifts", json=input_data)
            self.assertEqual(resp.data.decode(), example_output)

    def test_shifts_handler_get_instructions(self):
        expected_data = opening_hours.show_shifts_endpoint_instructions()
        with opening_hours.app.test_client() as c:
            resp = c.get("/shifts")
            self.assertEqual(resp.data.decode(), expected_data)

    def test_root_handler_get(self):
        expected_data = opening_hours.show_shifts_endpoint_instructions()
        with opening_hours.app.test_client() as c:
            resp = c.get("/", follow_redirects=True)
            self.assertEqual(resp.data.decode(), expected_data)


class TestHelpers(unittest.TestCase):
    def test_validate_shifts(self):
        input_data = json.loads(example_input)
        del input_data["monday"]
        input_data["tuesday"][0]["type"] = "incorrect"
        expected_errors = [
            "'monday' data missed in JSON input",
            "'tuesday' has invalid hours data",
        ]
        res = helpers.validate_shifts(input_data)
        self.assertSequenceEqual(res, expected_errors, seq_type=list)

    def test_str_time(self):
        self.assertEqual(helpers.str_time(64800), "6 PM")
        self.assertEqual(helpers.str_time(3600), "1 AM")
        self.assertEqual(helpers.str_time(86399), "11 PM")  # 1 Jan 23.59:59
        self.assertEqual(helpers.str_time(86400), "12 AM")  # 2 Jan 00:00:00
        self.assertEqual(helpers.str_time(0), "12 AM")

    def test_parse_hours(self):
        input_data = json.loads(example_input)
        expected_result = {
            'monday': [],
            'tuesday': ['10 AM - 6 PM'],
            'wednesday': [],
            'thursday': ['10 AM - 6 PM'],
            'friday': ['10 AM - 1 AM'],
            'saturday': ['10 AM - 1 AM'],
            'sunday': ['12 PM - 9 PM'],
        }
        res = helpers.parse_hours(input_data)
        self.assertDictEqual(res, expected_result)

    def test_format_day_shifts(self):
        input_data = {
            'monday': [],
            'tuesday': ['10 AM - 6 PM', '7 PM - 10 PM'],
            'wednesday': ['12 PM - 9 PM'],
        }
        expected = {
            'monday': 'Monday: Closed',
            'tuesday': 'Tuesday: 10 AM - 6 PM, 7 PM - 10 PM',
            'wednesday': 'Wednesday: 12 PM - 9 PM',
        }
        for day, shifts in input_data.items():
            res = helpers.format_day_shifts(day, shifts)
            self.assertEqual(res, expected[day])

    def test_format_opening_hours_as_text(self):
        input_data = json.loads(example_input)
        res = helpers.format_opening_hours_as_text(input_data)
        expected_result = example_output
        self.assertEqual(res, expected_result)


if __name__ == '__main__':
    unittest.main()
