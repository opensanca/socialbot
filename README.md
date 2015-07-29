# Socialbot
Bot written in Python 3.4 that get links from <a href="https://slack.com/" target="_blank">Slack</a> and publish on social networks.
<br>
More info at: <a href="https://opensanca.wordpress.com/2015/07/23/nosso-robo-mascote-robotson/" target="_blank">https://opensanca.wordpress.com/2015/07/23/nosso-robo-mascote-robotson/</a>

# Dependencies
`pip install -r requirements.txt`

# Configuration
Change <b>settings.py</b> and add your keys there.
<br>
Note: You'll need a <b><i>never expires token</i></b> to use Facebook API because it'll expire in one hour after the creation.

# Running
`python run.py`

# Share links from Slack
Type the configured key trigger. Default is `@share`.
<br>
When you type `@share Some text: somelink.com` the bot will share your message on Facebook and Twitter.

# Easter Egg
When you mention bot in a public channel it'll answer you.
<br>
e.g. `@robotson: How are you?`
<br>
And then:
<br>
<img src="http://s3.postimg.org/fm4keu8f7/robotson.png" />
<br>
So sweet :)
<br>
In background we are calling <a href="http://www.cleverbot.com/" target="_blank">Cleverbot</a> to answer the question.

# Licence
The MIT License (MIT)

Copyright (c) 2015 opensanca

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
