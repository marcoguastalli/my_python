import unittest

import metadata_hachoir


class Test(unittest.TestSuite):
    class Tests(unittest.TestCase):

        def test_extract_metadata_from_video(self):
            source_path = '/home/marco27/Downloads/IMG_7561.JPG'
            result = metadata_hachoir.extract_metadata(source_path)
            print("\n")
            print(result)
            print("\n")
            self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main(Test)
