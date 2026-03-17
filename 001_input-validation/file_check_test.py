"""
Test for the main program
"""

import errno
import unittest

from file_check import FileCheck


# Test Suite in order to organize our tests by groups of functionality
class FileCheckTest(unittest.TestSuite):
    class ParsingTests(unittest.TestCase):
        def test_ArgumentModelCreationOK(self):
            # given
            fc = FileCheck()
            # when

            # then
            self.assertIsNotNone(fc._args, "Object not initialized")
            self.assertTrue("file" in fc._args)

        def test_shouldFailWhenFileIsNone(self):
            # given
            fc = FileCheck()
            # when
            with self.assertRaises(SystemExit) as cm:
                fc.check_file()
            # then
            self.assertEqual(cm.exception.code, errno.EINVAL)

        def test_shouldFailWhenFileIsDirectory(self):
            # given
            fc = FileCheck()
            fc.file = "/"
            # when
            with self.assertRaises(SystemExit) as cm:
                fc.check_file()
            # then
            self.assertEqual(cm.exception.code, errno.EISDIR)

        def test_shouldFailWhenFileNotExist(self):
            # given
            fc = FileCheck()
            fc.file = "test_file.csv"
            # when
            with self.assertRaises(SystemExit) as cm:
                fc.check_file()
            # then
            self.assertEqual(cm.exception.code, errno.ENOENT)

        def test_shouldPassWhenCorrectFile(self):
            # given
            fc = FileCheck()
            fc.file = "test_ok.csv"
            # when

            # then
            self.assertTrue(fc.check_file())

        def test_shouldFailWhenIncorrectFile(self):
            # given
            fc = FileCheck()
            fc.file = "test_ko.csv"
            # when

            # then
            self.assertFalse(fc.check_file())


if __name__ == "__main__":
    unittest.main(FileCheckTest)  # Executing our TestSuite
