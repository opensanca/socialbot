import re
import abc
import html
import time
import settings
import facebook
import tweepy
from pymongo import MongoClient

import logging

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class SocialNetwork():
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.mongo_client = MongoClient(settings.MONGO.get("url"), settings.MONGO.get("port"))
        self.collection = self.mongo_client[settings.MONGO.get("database")][settings.MONGO.get("collection")]

    @abc.abstractmethod
    def post(self, message):
        """
        Post some data to a social network
        """
        pass

    def save_message(self, message):
        url = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
        document = {'message': message, 'timestamp': time.time()}
        try:
            document['url'] = url[0]
        except:
            pass
        self.collection.insert(document)

    def clean_message(self, message):
        cleaned_message = html.unescape(message)
        regex_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        url = re.findall(regex_pattern, cleaned_message)
        return {'message': cleaned_message, 'url': url[0] if len(url) > 0 else ""}

    def already_posted(self, url):
        if list(self.collection.find({"url": url})):
            return True
        else:
            return False


class Facebook(SocialNetwork):
    def post(self, message):
        cleaned_message = self.clean_message(message)
        graph = facebook.GraphAPI(settings.FACEBOOK.get('token'))

        logger.debug('Posting to Facebook')
        graph.put_wall_post(message=cleaned_message.get("message"), attachment={'link': cleaned_message.get("url")})

        logger.debug('Refreshing Facebook access token')
        graph.extend_access_token(app_id=settings.FACEBOOK.get('app_id'),
                                  app_secret=settings.FACEBOOK.get('app_secret'))


class Twitter(SocialNetwork):
    def post(self, message):
        cleaned_message = self.clean_message(message)
        self.auth = tweepy.OAuthHandler(settings.TWITTER.get('consumer_key'),
                                        settings.TWITTER.get('consumer_secret'))
        self.auth.set_access_token(settings.TWITTER.get('access_token'),
                                   settings.TWITTER.get('access_token_secret'))

        self.api = tweepy.API(self.auth)

        logger.debug('Posting to Twitter')
        self.api.update_status(status=cleaned_message.get("message"))

        self.save_message(cleaned_message)
