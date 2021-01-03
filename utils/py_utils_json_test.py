import unittest

import py_utils_json


class Test(unittest.TestSuite):
    class Tests(unittest.TestCase):

        def test_read_json(self):
            json_as_string = '{"id":"MediaMarco27DataDiscoDVideoAnimeToTransferOnePunchManS1Ita01LUomoPiForteMp401LUomoPiForteMp4284962284","path":"/media/marco27/Data/DiscoD/video/anime/toTransfer/One-Punch Man S1/ita","name":"01 - L’uomo più forte.mp4","namespace":"toTransfer/One-Punch Man S1/ita","mime":"video/mp4","created":"2021-01-03 12:43:35","modified":"2021-01-03 10:47:51","size":284962284}'
            expected = '{"id":"MediaMarco27DataDiscoDVideoAnimeToTransferOnePunchManS1Ita01LUomoPiForteMp401LUomoPiForteMp4284962284","path":"/media/marco27/Data/DiscoD/video/anime/toTransfer/One-Punch Man S1/ita","name":"01 - L’uomo più forte.mp4","namespace":"toTransfer/One-Punch Man S1/ita","mime":"video/mp4","created":"2021-01-03 12:43:35","modified":"2021-01-03 10:47:51","size":284962284}'
            result = py_utils_json.read_json(json_as_string)
            self.assertEqual(expected, result.__str__())


if __name__ == "__main__":
    unittest.main(Test)
