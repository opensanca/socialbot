import time
import settings
from slackclient import SlackClient
from slackclient._client import SlackNotConnected
from cleverbot import Cleverbot


class Robotson():
    def __init__(self, token):
        self.token = token
        self.slack = SlackClient(token=self.token)
        self.cleverbot = Cleverbot()

    def _conn(self):
        return self.slack.rtm_connect()

    def run(self):
        while True:
            message = self.listen()
            time.sleep(1)

    def share(self):
        pass

    def talk(self, message):
        try:
            answer = '@%s: %s' % (message.get("user"), self.cleverbot.ask(message.get("text")))
            self.slack.rtm_send_message(channel=message.get("channel"), message=answer)
        except Exception:
            pass

    def listen(self):
        if self._conn():
            full_message = self.slack.rtm_read()
            try:
                body = full_message[0]
                sender = body.get("user")
                channel = body.get("channel")
                message_content = body.get("text")
                return {'sender': sender, 'channel': channel, 'message': message_content}
            except Exception:
                pass
        else:
            raise SlackNotConnected


if __name__ == '__main__':
    robotson = Robotson(token=settings.SLACK.get("token"))
    robotson.run()
