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
        self.token = settings.SOCIAL_KEYS['facebook']
        graph = facebook.GraphAPI(access_token=self.token)
        try:
            graph.put_wall_post(message=message)
        except:
            print("deu ruim")


class Twitter(SocialNetwork):
    def post(self, message):
        pass
