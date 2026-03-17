import unittest
from datetime import datetime

import py_utils_date


class Test(unittest.TestSuite):
    class Tests(unittest.TestCase):

        def test_get_current_datetime_as_int(self):
            actual = py_utils_date.get_current_datetime_as_int()
            print(actual)
            print(datetime.fromtimestamp(actual))
            self.assertTrue(type(actual) == int)
            self.assertIsNotNone(actual)

        def test_get_current_datetime_with_format_as_string(self):
            date_format = "%Y-%m-%d %H:%M:%S"
            actual = py_utils_date.get_current_datetime_with_format_as_string(date_format)
            print(actual)
            self.assertIsInstance(actual, str)
            self.assertIsNotNone(actual)
            # self.assertEqual(str('2021-03-12 10:04'), actual)

        def test_get_current_datetime_with_format_microseconds_as_string(self):
            date_format_microseconds = "%Y-%m-%d %H:%M:%S.%f"
            actual = py_utils_date.get_current_datetime_with_format_as_string(date_format_microseconds)
            print(actual)
            self.assertIsInstance(actual, str)
            self.assertIsNotNone(actual)
            # self.assertEqual(str('2021-03-12 10:04'), actual)

        def test_convert_datetime_to_timestamp(self):
            date_time = datetime(1975, 12, 27, 13, 14, 15)
            actual = py_utils_date.convert_datetime_to_timestamp(date_time)
            print(actual)
            self.assertIsInstance(actual, float)
            self.assertIsNotNone(actual)
            self.assertEqual(float(188914455), actual)

        def test_convert_timestamp_to_datetime(self):
            time_stamp = 188914455
            actual = py_utils_date.convert_timestamp_to_datetime(time_stamp)
            print(actual)
            self.assertIsInstance(actual, datetime)
            self.assertIsNotNone(actual)
            self.assertEqual(datetime(1975, 12, 27, 13, 14, 15), actual)

        def test_convert_timestamp_to_str_with_format(self):
            time_stamp = 188914455
            date_format = "%Y-%m-%d %H:%M:%S"
            actual = py_utils_date.convert_timestamp_to_str_with_format(time_stamp, date_format)
            print(actual)
            self.assertIsInstance(actual, str)
            self.assertIsNotNone(actual)
            self.assertEqual(str('1975-12-27 13:14:15'), actual)

            time_stamp: str = "188914455"
            date_format = "%Y-%m-%d %H:%M:%S"
            actual = py_utils_date.convert_timestamp_to_str_with_format(time_stamp, date_format)
            print(actual)
            self.assertIsInstance(actual, str)
            self.assertIsNotNone(actual)
            self.assertEqual(str('1975-12-27 13:14:15'), actual)


if __name__ == "__main__":
    unittest.main(Test)
