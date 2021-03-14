from utils.py_utils_post_json import post_json_to_url


class StoreJson:
    def __init__(self, url, json_string):
        self.url = url
        self.json_string = json_string

    def store(self):
        return post_json_to_url(self.url, self.json_string)
