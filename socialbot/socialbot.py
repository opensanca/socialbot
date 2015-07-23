from slacker import Slacker
from cleverbot import Cleverbot
import settings
from socialbot.networks import Facebook, Twitter


class SocialBot():
    def __init__(self):
        self.token = settings.SECRET_KEY
        self.slack = Slacker(self.token)
        self.facebook = Facebook()
        self.twitter = Twitter()
        self.history = {}

    def channels(self):
        channels = []
        for channel in self.slack.channels.list().body['channels']:
            channels.append(channel)

        return channels

    def discover_userid(self, username):
        users = self.slack.users.list().body['members']
        for user in users:
            if user['name'] == username:
                return user['id']

    def discover_username(self, userid):
        users = self.slack.users.list().body['members']
        for user in users:
            if user['id'] == userid:
                return user['name']

    def listen(self, channel):
        self.messages = self.slack.channels.history(channel, count=5).body['messages']
        bot_id = self.discover_userid(settings.BOT_NAME)
        bot_mention = "<@" + bot_id + ">"
        if str(channel) in self.history:
            if self.history[str(channel)] != self.messages:
                for message in self.messages:
                    if dict(message) not in self.history[str(channel)]:
                        text = ''
                        try:
                            text = message['text']
                        except:
                            print('Invalid message')
                        if bot_mention in text:
                            self.talk(channel, message)
                        if settings.SHARE_TRIGGER in text:
                            self.share(channel, text)
                self.history[str(channel)] = self.messages
        else:
            self.history[str(channel)] = []
            self.listen(channel)

    def talk(self, channel, question):
        try:
            cleverbot = Cleverbot()
            answer = '@' + self.discover_username(question['user']) + ': ' + cleverbot.ask(question['text'])
            self.slack.chat.post_message(channel=channel, text=answer, as_user=settings.BOT_NAME)
        except Exception as ex:
            print(ex)

    def share(self, channel, message):
        try:
            message = message.replace(settings.SHARE_TRIGGER, '').strip().replace('<', '').replace('>', '')
            self.facebook.post(message)
            self.twitter.post(message)
        except Exception as ex:
            print(ex)
