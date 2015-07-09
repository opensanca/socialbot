from slacker import Slacker
import settings

slack = Slacker(settings.SECRET_KEY)

# Send a message to #general channel
# slack.chat.post_message('#random', 'Olá! Estou enviando esta mensagem de teste via console usando o Python.', as_user='robotson')

# Get users list
# response = slack.users.list()
# users = response.body['members']
# print(users)

print(slack.channels.history('C077BBUJU').body)
# print(slack.channels.list().body)
