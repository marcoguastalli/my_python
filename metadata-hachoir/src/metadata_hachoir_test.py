import unittest

import metadata_hachoir


class Test(unittest.TestSuite):
    class Tests(unittest.TestCase):

        def test_extract_metadata_from_video(self):
            source_path = '/media/marco27/Data/DiscoD/video/moviesToWatchAndDelete/2011 - A Few Best Men.mp4'
            result = metadata_hachoir.extract_metadata_from_video(source_path)
            print("\n")
            print(result)
            print("\n")
            self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main(Test)
