import unittest

from binary_to_text import binary_to_text


class Test(unittest.TestSuite):
    class Tests(unittest.TestCase):

        def test_binary_to_text(self):
            binary = "011001000111001001100001011001110110111101101110"
            result = binary_to_text(binary)
            self.assertIsNotNone(result)
            self.assertEqual(result, "dragon")


if __name__ == "__main__":
    unittest.main(Test)
