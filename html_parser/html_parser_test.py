import unittest

import html_parser


class Test(unittest.TestSuite):
    class Tests(unittest.TestCase):

        def test(self):
            html = "<html><head></head><body><div class='wrapper'>WRAPPER</div></body></html>"
            result = html_parser.parse_html(html)
            print("\n")
            print(result)
            print("\n")
            self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main(Test)
