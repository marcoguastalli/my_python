import os
import unittest

from remove_parameters_from_url import remove_parameters_from_url_in_file


class Test(unittest.TestSuite):
    class Tests(unittest.TestCase):

        def test_remove_parameters_from_url_in_file(self):
            source_file_name = os.environ['MY_HOME'] + "/Downloads/todo_insta.txt"
            target_file_name = os.environ['MY_HOME'] + "/Downloads/todo_insta_filtered.txt"
            self.assertIsNotNone(self, remove_parameters_from_url_in_file(source_file_name, target_file_name))


if __name__ == "__main__":
    unittest.main(Test)
