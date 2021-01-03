import unittest

import py_utils_string


class Test(unittest.TestSuite):
    class Tests(unittest.TestCase):

        def test_convert_list_to_string(self):
            input = ["one", "two", "three"]
            expected = 'onetwothree'
            self.assertEqual(expected, py_utils_string.convert_list_to_string(input))

        def test_create_json_array_string_from_string_list(self):
            input = ["one", "two", "three"]
            expected = '["one","two","three"]'
            result = py_utils_string.create_json_array_string_from_string_list(input)
            self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main(Test)
