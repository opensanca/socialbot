import re
import time
import json
from slackclient import SlackClient
from slackclient._client import SlackNotConnected
from cleverbot import Cleverbot
import settings
from socialbot.networks import Facebook, Twitter


class Robotson():
    def __init__(self, token):
        self.token = token
        self.slack = SlackClient(token=self.token)
        self.cleverbot = Cleverbot()
        self.botname = settings.BOT_NAME
        self.facebook = Facebook()
        self.twitter = Twitter()

    def run(self, interval):
        if self.slack.rtm_connect():
            while True:
                full_message = self.slack.rtm_read()
                if full_message:
                    content = full_message[0]
                    if content.get("type") == 'message':
                        sender = self.username_as_str(content.get("user"))
                        channel = content.get("channel")
                        message = content.get("text")

                        match = re.search(r'<@(.*)>', message)
                        bot_mention = match.group() if match else None

                        if bot_mention in message:
                            self.talk(channel, sender, message)
                        elif settings.SHARE_TRIGGER in message:
                            self.share(message)
                time.sleep(interval)
        else:
            raise SlackNotConnected

    def share(self, message):
        try:
            message = message.replace(settings.SHARE_TRIGGER, '').strip().replace('<', '').replace('>', '')
            print(message)
            self.facebook.post(message)
            self.twitter.post(message)
        except Exception:
            pass

    def talk(self, channel, user, message):
        try:
            answer = '@%s: %s' % (user, self.cleverbot.ask(message))
            self.slack.rtm_send_message(channel=channel, message=answer)
        except Exception:
            pass

    def username_as_str(self, userid):
        response = json.loads(self.slack.api_call('users.info', user=userid))
        return response.get("user").get("name")


if __name__ == '__main__':
    robotson = Robotson(token=settings.SLACK.get("token"))
    robotson.run(interval=1)
