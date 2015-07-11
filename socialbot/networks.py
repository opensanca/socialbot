import abc


class SocialNetwork():
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def post(self):
        """
        :return:
        """


class Facebook(SocialNetwork):
    def post(self):
        pass


class Twitter(SocialNetwork):
    def post(self):
        pass
