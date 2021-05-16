import unittest

import html_parser


class Test(unittest.TestSuite):
    class Tests(unittest.TestCase):

        def test_parse_html_first_impact(self):
            html = "<html><head></head><body><div class='wrapper'>WRAPPER</div></body></html>"
            result = html_parser.parse_html_first_impact(html)
            print("\n")
            print(result)
            print("\n")
            self.assertIsNotNone(result)

        def test_get_tags_from_soup(self):
            html = '<a href="http://localhost">localhost</a>, <a href="http://127.0.0.1">127.0.0.1</a>'
            soup = html_parser.get_soup_from_html(html)
            result = html_parser.get_tags_from_soup(soup, 'a')
            print("\n")
            print(result)
            print("\n")
            self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main(Test)
