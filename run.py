import time
import settings
from socialbot.socialbot import SocialBot

if __name__ == '__main__':
    bot = SocialBot()
    while True:
        try:
            for channel in bot.channels():
                bot.listen(channel['id'])
        except Exception as ex:
            print("Erro: %s" % ex)
            time.sleep(1)
