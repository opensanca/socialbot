from slacker import Slacker
from cleverbot import Cleverbot
import settings


class Bot():
    def __init__(self):
        self.slack = Slacker(settings.SECRET_KEY)

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

    def read(self, channel):
        messages = self.slack.channels.history(channel).body['messages']
        return messages

    def talk(self, channel, question):
        bot_id = self.discover_userid(settings.BOT_NAME)
        bot_mention = "<@" + bot_id + ">:"
        print(bot_mention)
        print(question['text'])
        if bot_mention in question['text']:
            print(question['text'])
            cleverbot = Cleverbot()
            answer = '@' + self.discover_username(question['user']) + ': ' + cleverbot.ask(question['text'])
            print(answer)
            self.slack.chat.post_message(channel=channel, text=answer, as_user=settings.BOT_NAME)

    def share(self, channel):
        for message in self.read(channel):
            if settings.SHARE_TRIGGER in message:
                pass
