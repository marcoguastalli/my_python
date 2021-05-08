import unittest

from get_account_summary import main


class Test(unittest.TestSuite):
    class Tests(unittest.TestCase):

        def test(self):
            main()
            pass


if __name__ == "__main__":
    unittest.main(Test)
