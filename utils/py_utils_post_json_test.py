import unittest

import py_utils_post_json


class Test(unittest.TestSuite):
    class Tests(unittest.TestCase):

        def test_post_json_to_url(self):
            url = 'http://localhost:8080/marco27-web/v1/bookmarks/create'
            json_string = '{"title":"DuckDuckGo","uri":"https://www.duckduckgo.com/","folder":"Bookmamrs",' \
                          '"icon":"","status":200,"created":"2018-04-27 11:35:37","modified":"2018-04-27 11:35:37"} '
            expected = json_string.encode("utf-8")
            result = py_utils_post_json.post_json_to_url(url, json_string)
            self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main(Test)
