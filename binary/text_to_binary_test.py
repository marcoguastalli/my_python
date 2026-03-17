import unittest

from text_to_binary import text_to_binary


class Test(unittest.TestSuite):
    class Tests(unittest.TestCase):

        def test_text_to_binary(self):
            text = "dragon"
            result = text_to_binary(text)
            self.assertIsNotNone(result)
            self.assertEqual(result, "011001000111001001100001011001110110111101101110")


if __name__ == "__main__":
    unittest.main(Test)
