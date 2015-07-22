import abc
import facebook
import tweepy
from settings import *


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
        graph = facebook.GraphAPI(access_token=FACEBOOK['token'])
        graph.put_wall_post(message=message)


class Twitter(SocialNetwork):
    def post(self, message):
        self.auth = tweepy.OAuthHandler(TWITTER['consumer_key'], TWITTER['consumer_secret'])
        self.auth.set_access_token(TWITTER['access_token'], TWITTER['access_token_secret'])

        self.api = tweepy.API(self.auth)

        self.api.update_status(status=message)