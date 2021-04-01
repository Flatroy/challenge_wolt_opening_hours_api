import json
import unittest

import opening_hours
from examples import example_input, example_output


class TestOpeningHours(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
