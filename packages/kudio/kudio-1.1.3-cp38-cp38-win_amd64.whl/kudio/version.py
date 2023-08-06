import json

version_json = '''
{
 "author": "recklight",
 "date": 2022.12,
 "version":"1.1.3"
}
'''


def get_versions():
    return json.loads(version_json)
