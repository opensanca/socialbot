# Socialbot
Bot written in Python 3.4 that get links from <a href="https://slack.com/" target="_blank">Slack</a> and publish on social networks.
<br>
More info at: https://opensanca.wordpress.com/2015/07/23/nosso-robo-mascote-robotson/

# Dependencies
`pip install -r requirements.txt`

# Configuration
Change <b>settings.py</b> and add your keys there.
<br>
Note: You'll need a <b><i>never expires token</i></b> to use Facebook API because it'll expire in one hour after the creation.

# Run
`python run.py`

# Share links from Slack
Type the configured key trigger. Default is `@share`
<br>
When you type `@share Some text: somelink.com` the bot will share your message on Facebook and Twitter

# Easter Egg
When you mention bot in a public channel it'll answer you.
<br>
e.g. `@robotson: How are you?`
<br>
In background we are calling <a href="http://www.cleverbot.com/" target="_blank">Cleverbot</a> to answer the question.

