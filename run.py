from slacker import Slacker

import settings
from socialbot.networks import Facebook
from socialbot.socialbot import Bot

slack = Slacker(settings.SECRET_KEY)

bot = Bot()

messages = bot.read(settings.CHANNELS_IDS['#random'])

# for message in messages:
#    bot.talk(settings.CHANNELS_IDS['#random'], message)
# print(bot.read(settings.CHANNELS_IDS['#random']))
facebook = Facebook()
facebook.post("Testing facebook developer API via Python console")
