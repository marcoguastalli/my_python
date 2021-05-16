import requests


def post_json_to_url(url, json_string):
    json_string_utf8 = str(json_string).encode("utf-8")
    headers = {'Content-type': 'application/json', 'Accept': '*/*'}
    try:
        response = requests.post(url, data=json_string_utf8, headers=headers)
    except Exception as e:
        print("Error store json:\n %s" % json_string_utf8)
        print(e)

    return json_string_utf8
