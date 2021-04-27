from urllib.parse import quote_plus

from dotenv import dotenv_values
from pymongo import MongoClient


class StoreMongoPfs:
    def __init__(self, json_string):
        dot_env = dotenv_values(".env")
        self.json_string = json_string
        uri = "mongodb://%s:%s@%s" % (quote_plus(dot_env['MONGODB_LOGIN']), quote_plus(dot_env['MONGODB_SECRET']), dot_env['MONGODB_HOST'])
        self.mongo_client = MongoClient(uri, port=int(dot_env['MONGODB_PORT']))
        self.mongo_database = self.mongo_client[dot_env['MONGODB_DATABASE']]
        self.collection = self.mongo_database[dot_env['MONGODB_COLLECTION']]

    def store(self):
        try:
            json_dict: dict = eval(self.json_string)
            self.collection.insert_one(json_dict)
        except Exception as e:
            print("Error store json in MongoDB:\n %s" % self.json_string)
            print(e)
        finally:
            self.mongo_client.close()
        return self.json_string
