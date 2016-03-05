import os
import json

BASE_DIR = os.path.dirname(__file__)

SECRET_FILE = os.path.join(BASE_DIR, "secrets.json")


def get_secret(api, secret):
    with open(SECRET_FILE) as f:
        content = f.read()
    return json.loads(content).get(api).get(secret)


SLACK = {
    'token': get_secret(api='slack', secret='token')
}

BOT_NAME = "robotson_v2"

SHARE_TRIGGER = "@share"
