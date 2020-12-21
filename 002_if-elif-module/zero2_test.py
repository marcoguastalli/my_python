import unittest
import zero2

class ZeroTwoTest(unittest.TestSuite):
    class ZeroTwoTestNo(unittest.TestCase):
        def test_main(self):
            # given
            answer = zero2.main()
            # when

            # then
            self.assertIsNone(answer)


if __name__ == "__main__":
    unittest.main(ZeroTwoTest)