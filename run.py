import time
from socialbot.socialbot import SocialBot

import logging

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.debug('Running bot')
    bot = SocialBot()
    while True:
        try:
            for channel in bot.channels():
                logger.debug('Listening channel: %s' % str(channel['name']))
                bot.listen(channel['id'])
        except Exception as ex:
            logger.error('Something wrong. Error: %s' % str(ex))
            time.sleep(1)
