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
            error_message = "Amiguinhos, tive um problema. Podem me ajudar? Erro: %s", ex
            bot.slack.chat.post_message(channel='#general',
                                        text=error_message,
                                        as_user=settings.BOT_NAME)
            time.sleep(1)
