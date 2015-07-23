import abc
import facebook
import tweepy
from settings import *
import re


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
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
        graph = facebook.GraphAPI(FACEBOOK['token'])
        graph.put_wall_post(message=message, attachment={'link': url[0]})
        graph.extend_access_token(app_id=FACEBOOK['app_id'], app_secret=FACEBOOK['app_secret'])


class Twitter(SocialNetwork):
    def post(self, message):
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
        self.auth = tweepy.OAuthHandler(TWITTER['consumer_key'], TWITTER['consumer_secret'])
        self.auth.set_access_token(TWITTER['access_token'], TWITTER['access_token_secret'])

        self.api = tweepy.API(self.auth)

        self.api.update_status(status=message)
