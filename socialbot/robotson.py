import re
import time
import json
from slackclient import SlackClient
from slackclient._client import SlackNotConnected
from cleverbot import Cleverbot
import settings
from socialbot.networks import SocialNetwork, Facebook, Twitter


class Robotson():
    def __init__(self, token):
        self.token = token
        self.slack = SlackClient(token=self.token)
        self.cleverbot = Cleverbot()
        self.botname = settings.BOT_NAME
        self.facebook = Facebook()
        self.twitter = Twitter()
        self.network = SocialNetwork()

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

                        try:
                            match = re.search(r'<@[A-Z0-9]+>', message)
                            bot_mention = match.group() if match else ""

                            if bot_mention:
                                # TODO: Remove hardcoding
                                if settings.BOT_UID in bot_mention:
                                    self.talk(channel, sender, message)
                            elif settings.SHARE_TRIGGER in message.lower():
                                self.share(message)
                        except:
                            pass
                time.sleep(interval)
        else:
            raise SlackNotConnected

    def share(self, message):
        try:
            match_share_trigger = re.search(r'%s[\:]?' % settings.SHARE_TRIGGER, message)
            message = message.replace(match_share_trigger.group(), "")

            match_lt_mt = re.search(r'[<]+(.*)[>]+', message)
            message = message.replace(match_lt_mt.group(0), match_lt_mt.group(1))

            message = message.strip()

            url = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
            if len(url) > 0:
                if not self.network.already_posted(url[0]):
                    self.facebook.post(message)
                    self.twitter.post(message)
                    self.network.save_message(message)
        except Exception:
            pass

    def talk(self, channel, user, message):
        try:
            answer = '@%s: %s' % (user, self.cleverbot.ask(message))
            self.slack.rtm_send_message(channel=channel, message=answer)
        except Exception:
            pass

    def username_as_str(self, userid):
        try:
            response = json.loads(self.slack.api_call('users.info', user=userid))
            return response.get("user").get("name")
        except:
            return ""


if __name__ == '__main__':
    def run():
        try:
            robotson = Robotson(token=settings.SLACK.get("token"))
            robotson.run(interval=1)
        except:
            # Bot will never die
            time.sleep(1)
            run()


    run()
