import unittest

import metadata_hachoir


class Test(unittest.TestSuite):
    class Tests(unittest.TestCase):

        def test_extract_metadata(self):
            source_path = '/Users/marcoguastalli/Downloads/Fundamentals-of-Software-Architecture_Oreilly_Cover.png'
            result = metadata_hachoir.extract_metadata(source_path)
            print("\n")
            print(result)
            print("\n")
            self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main(Test)
