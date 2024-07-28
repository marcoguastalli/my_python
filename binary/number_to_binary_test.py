import unittest

from number_to_binary import number_to_binary


class Test(unittest.TestSuite):
    class Tests(unittest.TestCase):

        def test_number_to_binary(self):
            number = 1
            result = number_to_binary(number)
            self.assertIsNotNone(result)
            self.assertEqual(result, "00000001")


if __name__ == "__main__":
    unittest.main(Test)
