import json
import unittest

from examples import example_input, example_output
from opening_hours import app


class TestOpeningHours(unittest.TestCase):
    def test_shifts_handler_valid_input(self):
        input_data = json.loads(example_input)
        with app.test_client() as c:
            resp = c.post("/shifts", json=input_data)
            self.assertEqual(resp.data.decode(), example_output)


if __name__ == '__main__':
    unittest.main()
