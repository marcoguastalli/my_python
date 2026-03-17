import unittest

from binary_to_number import binary_to_number


class Test(unittest.TestSuite):
    class Tests(unittest.TestCase):

        def test_binary_to_number(self):
            binary = "00000001"
            result = binary_to_number(binary)
            self.assertIsNotNone(result)
            self.assertEqual(result, 1)
            binary = "10000000"
            result = binary_to_number(binary)
            self.assertIsNotNone(result)
            self.assertEqual(result, 128)


if __name__ == "__main__":
    unittest.main(Test)
