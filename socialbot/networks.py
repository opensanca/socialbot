import abc
import facebook
import tweepy
from settings import *
from html.parser import HTMLParser
import re

import logging

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class SocialNetwork():
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def post(self, message):
        """
        Post some data to a social network
        """
        pass


class Facebook(SocialNetwork):
    def post(self, message):
        h = HTMLParser()
        message = h.unescape(message)
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
        graph = facebook.GraphAPI(FACEBOOK['token'])

        logger.debug('Posting to Facebook')
        graph.put_wall_post(message=message, attachment={'link': url[0]})

        logger.debug('Refreshing Facebook access token')
        graph.extend_access_token(app_id=FACEBOOK['app_id'], app_secret=FACEBOOK['app_secret'])


class Twitter(SocialNetwork):
    def post(self, message):
        h = HTMLParser()
        message = h.unescape(message)
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
        self.auth = tweepy.OAuthHandler(TWITTER['consumer_key'], TWITTER['consumer_secret'])
        self.auth.set_access_token(TWITTER['access_token'], TWITTER['access_token_secret'])

        self.api = tweepy.API(self.auth)

        logger.debug('Posting to Twitter')
        self.api.update_status(status=message)
