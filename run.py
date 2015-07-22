import time
from socialbot.socialbot import SocialBot

if __name__ == '__main__':
    bot = SocialBot()
    while True:
        try:
            for channel in bot.channels():
                bot.listen(channel['id'])
        except Exception as ex:
            print(ex)
            bot = SocialBot()
            time.sleep(1)
