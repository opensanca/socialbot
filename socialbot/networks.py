import re
import abc
import html
import settings
import facebook
import tweepy

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
        message = html.unescape(message)
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
        graph = facebook.GraphAPI(settings.FACEBOOK.get('token'))

        logger.debug('Posting to Facebook')
        graph.put_wall_post(message=message, attachment={'link': url[0]})

        logger.debug('Refreshing Facebook access token')
        graph.extend_access_token(app_id=settings.FACEBOOK.get('app_id'),
                                  app_secret=settings.FACEBOOK.get('app_secret'))


class Twitter(SocialNetwork):
    def post(self, message):
        message = html.unescape(message)
        self.auth = tweepy.OAuthHandler(settings.TWITTER.get('consumer_key'), settings.TWITTER.get('consumer_secret'))
        self.auth.set_access_token(settings.TWITTER.get('access_token'), settings.TWITTER.get('access_token_secret'))

        self.api = tweepy.API(self.auth)

        logger.debug('Posting to Twitter')
        self.api.update_status(status=message)
