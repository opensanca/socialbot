from slacker import Slacker
from cleverbot import Cleverbot
import settings
from socialbot.networks import Facebook, Twitter

import logging

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class SocialBot():
    def __init__(self):
        logger.debug('Instantiating SocialBot')
        self.token = settings.SECRET_KEY
        self.slack = Slacker(self.token)
        self.facebook = Facebook()
        self.twitter = Twitter()
        self.cleverbot = Cleverbot()
        self.history = {}

    def channels(self):
        logger.debug('Getting all channels')
        channels = []
        for channel in self.slack.channels.list().body['channels']:
            channels.append(channel)

        return channels

    def discover_userid(self, username):
        logger.debug('Getting user id')
        users = self.slack.users.list().body['members']
        for user in users:
            if user['name'] == username:
                return user['id']

    def discover_username(self, userid):
        logger.debug('Getting username')
        users = self.slack.users.list().body['members']
        for user in users:
            if user['id'] == userid:
                return user['name']

    def listen(self, channel):
        logger.debug('Listening...')
        self.messages = self.slack.channels.history(channel, count=3).body['messages']
        bot_id = self.discover_userid(settings.BOT_NAME)
        bot_mention = "<@" + bot_id + ">"
        if str(channel) in self.history:
            if self.history[str(channel)] != self.messages:
                for message in self.messages:
                    logger.debug('Getting new messages')
                    if dict(message) not in self.history[str(channel)]:
                        text = ''
                        try:
                            text = message['text']
                            logger.debug('New message: %s' % text)
                        except:
                            logger.error('Invalid message: %s' % str(message['text']))
                        if bot_mention in text:
                            logger.debug('Oh! Someone is talking to me :D')
                            self.talk(channel, message)
                        if settings.SHARE_TRIGGER in text:
                            logger.debug('Someone is calling me to share!')
                            self.share(channel, text)
                self.history[str(channel)] = self.messages
        else:
            self.history[str(channel)] = []
            self.listen(channel)

    def talk(self, channel, question):
        try:
            logger.debug('Talking to the moooon... ops, to the bot =P')
            answer = '@' + self.discover_username(question['user']) + ': ' + self.cleverbot.ask(question['text'])
            self.slack.chat.post_message(channel=channel, text=answer, as_user=settings.BOT_NAME)
        except Exception as ex:
            logger.error('Something wrong. Error: %s' % str(ex))

    def share(self, channel, message):
        try:
            logger.debug('Sharing...')
            message = message.replace(settings.SHARE_TRIGGER, '').strip().replace('<', '').replace('>', '')
            self.facebook.post(message)
            self.twitter.post(message)
        except Exception as ex:
            logger.error('Something wrong. Error: %s' % str(ex))
