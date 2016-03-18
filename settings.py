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

FACEBOOK = {
    'token': get_secret(api='facebook', secret='token'),
    'app_id': get_secret(api='facebook', secret='app_id'),
    'app_secret': get_secret(api='facebook', secret='app_secret')
}

TWITTER = {
    'consumer_key': get_secret(api='twitter', secret='consumer_key'),
    'consumer_secret': get_secret(api='twitter', secret='consumer_secret'),
    'access_token': get_secret(api='twitter', secret='access_token'),
    'access_token_secret': get_secret(api='twitter', secret='access_token_secret')
}

MONGO = {
    "url": get_secret(api='mongo', secret='url'),
    "port": get_secret(api='mongo', secret='port'),
    "database": get_secret(api='mongo', secret='database'),
    "collection": get_secret(api='mongo', secret='collection')
}

BOT_NAME = "robotson_v2"

SHARE_TRIGGER = "@share"
