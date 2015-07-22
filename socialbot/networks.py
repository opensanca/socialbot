import abc
import facebook
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
        self.token = settings.TOKENS['facebook']
        graph = facebook.GraphAPI(access_token=self.token)
        graph.put_wall_post(message=message)


class Twitter(SocialNetwork):
    def post(self, message):
        pass
