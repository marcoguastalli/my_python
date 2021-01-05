from urllib.parse import quote_plus

from pymongo import MongoClient


class StoreMongoPfs:
    def __init__(self, json_string):
        self.json_string = json_string
        uri = "mongodb://%s:%s@%s" % (quote_plus('local'), quote_plus('qwerty'), 'localhost')
        self.mongo_client = MongoClient(uri, port=27017)
        self.mongo_database = self.mongo_client["local"]
        self.collection = self.mongo_database["printfilesystem"]

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
