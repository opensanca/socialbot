import abc
from facepy import GraphAPI
import settings


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
        self.token = settings.SOCIAL_KEYS['facebook']
        graph = GraphAPI(oauth_token=self.token, version='2.4')
        graph.post(
            path='me',
            message=message
        )


class Twitter(SocialNetwork):
    def post(self, message):
        pass
