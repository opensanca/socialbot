from slacker import Slacker

import settings
from socialbot.socialbot import Bot

slack = Slacker(settings.SECRET_KEY)

bot = Bot()

print(bot.discover_userid('lucasmarques'))
