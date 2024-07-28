import unittest

from text_to_number_binary import text_to_binary_number


class Test(unittest.TestSuite):
    class Tests(unittest.TestCase):

        def test_text_to_binary_number(self):
            text = "dragon"
            result = text_to_binary_number(text)
            self.assertIsNotNone(result)
            self.assertEqual(result, 110442423218030)


if __name__ == "__main__":
    unittest.main(Test)
