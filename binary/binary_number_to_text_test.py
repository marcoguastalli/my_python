import unittest

from binary_number_to_text import binary_number_to_text


class Test(unittest.TestSuite):
    class Tests(unittest.TestCase):

        def test_text_to_binary_number(self):
            number = 110442423218030
            result = binary_number_to_text(number)
            self.assertIsNotNone(result)
            self.assertEqual(result, "dragon")


if __name__ == "__main__":
    unittest.main(Test)
