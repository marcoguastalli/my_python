import unittest

import rpc_client


class Test(unittest.TestSuite):
    class Tests(unittest.TestCase):

        def rpc_client_test(self):
            endpoint = "https://mempool.space:60602"
            json_rpc_client = rpc_client.JsonRPCClient
            result = json_rpc_client.add_method(endpoint)
            print("\n")
            print(result)
            print("\n")
            self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main(Test)
