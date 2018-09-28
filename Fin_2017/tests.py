#!/usr/bin/python

import unittest
import json
from cafe import Cafe, InvalidInputModeException, InvalidInputDataException

class TestFIFO(unittest.TestCase):

    def test_invalid_order_time(self):
        cafe = Cafe(0,
                    [{
                        "order_time": -1,
                        "order_id": 1,
                        "type": "affogato"
                    }],
                    'test_output.json')
        self.assertRaises(InvalidInputDataException, cafe.open_for_business)

    def test_invalid_order_type(self):
        cafe = Cafe(0,
                    [{
                        "order_time": 1,
                        "order_id": 1,
                        "type": "idon'tknow"
                    }],
                    'test_output.json')
        self.assertRaises(InvalidInputDataException, cafe.open_for_business)

    def test_invalid_order_id(self):
        cafe = Cafe(0,
                    [{
                        "order_time": 1,
                        "order_id": -45,
                        "type": "affogato"
                    }],
                    'test_output.json')
        self.assertRaises(InvalidInputDataException, cafe.open_for_business)

    def test_one_order(self):
        cafe = Cafe(0, [{"order_time": 4, "order_id": 1, "type": "tea"}], 'test_output.json')
        cafe.open_for_business()
        self.assertEqual(cafe.output_data, [{"barista_id": 1, "start_time": 4, "order_id": 1}])

        cafe = Cafe(1, [{"order_time": 4, "order_id": 1, "type": "tea"}], 'test_output.json')
        cafe.open_for_business()
        self.assertEqual(cafe.output_data, [{"barista_id": 1, "start_time": 4, "order_id": 1}])

    def test_no_orders(self):
        cafe = Cafe(0, [], 'test_output.json')
        cafe.open_for_business()
        self.assertEqual(cafe.output_data, [])

        cafe = Cafe(1, [], 'test_output.json')
        cafe.open_for_business()
        self.assertEqual(cafe.output_data, [])

    def test_other_general(self):
        cafe = Cafe(1,
                    [
                        {"order_id": 1, "order_time": 0, "type": "affogato"},
                        {"order_id": 2, "order_time": 1, "type": "tea"},
                        {"order_id": 3, "order_time": 2, "type": "latte"},
                        {"order_id": 4, "order_time": 2, "type": "tea"}
                    ],
                    'test_output.json')
        # So the input data doesn't have to be huge
        cafe.open_time = 5
        cafe.open_for_business()
        self.assertEqual(cafe.output_data, [
            {"order_id": 2, "start_time": 1, "barista_id": 1},
            {"order_id": 3, "start_time": 2, "barista_id": 2},
            {"order_id": 4, "start_time": 4, "barista_id": 1}
        ])

    def test_fifo_general(self):
        # test general case with given same input file
        with open('sample_input.json', 'r') as input_file:
            decoder = json.JSONDecoder()
            input_data = decoder.decode(input_file.read())
        cafe = Cafe(0, input_data, 'test_output.json')
        cafe.open_for_business()

        # use given sample output file as "rubric"
        with open('sample_output_fifo.json', 'r') as input_file:
            decoder = json.JSONDecoder()
            sample_output = decoder.decode(input_file.read())

        self.assertEqual(cafe.output_data, sample_output)


# Run the tests
if __name__ == '__main__':
    unittest.main()
