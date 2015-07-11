"""
Python library allowing interaction with the Cleverbot API.
Updated to use Python 3.
Credits to: https://github.com/folz/cleverbot.py
"""
import http.cookiejar
import hashlib
import urllib
import urllib.request
import urllib.parse


class Cleverbot():
    """
    Wrapper over the Cleverbot API.
    """
    HOST = "www.cleverbot.com"
    PROTOCOL = "http://"
    RESOURCE = "/webservicemin"
    API_URL = PROTOCOL + HOST + RESOURCE

    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)',
        'Accept': 'text/html,application/xhtml+xml,'
                  'application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
        'Accept-Language': 'en-us,en;q=0.8,en-us;q=0.5,en;q=0.3',
        'Cache-Control': 'no-cache',
        'Host': HOST,
        'Referer': PROTOCOL + HOST + '/',
        'Pragma': 'no-cache'
    }

    def __init__(self):
        """ The data that will get passed to Cleverbot's web API """
        self.data = {
            'stimulus': '',
            'start': 'y',  # Never modified
            'sessionid': '',
            'vText8': '',
            'vText7': '',
            'vText6': '',
            'vText5': '',
            'vText4': '',
            'vText3': '',
            'vText2': '',
            'icognoid': 'wsf',  # Never modified
            'icognocheck': '',
            'fno': 0,  # Never modified
            'prevref': '',
            'emotionaloutput': '',  # Never modified
            'emotionalhistory': '',  # Never modified
            'asbotname': '',  # Never modified
            'ttsvoice': '',  # Never modified
            'typing': '',  # Never modified
            'lineref': '',
            'sub': 'Say',  # Never modified
            'islearning': 1,  # Never modified
            'cleanslate': False,  # Never modified
        }

        # the log of our conversation with Cleverbot
        self.conversation = []
        self.resp = str()

        # install an opener with support for cookies
        cookies = http.cookiejar.LWPCookieJar()
        handlers = [
            urllib.request.HTTPHandler(),
            urllib.request.HTTPSHandler(),
            urllib.request.HTTPCookieProcessor(cookies)
        ]
        opener = urllib.request.build_opener(*handlers)
        urllib.request.install_opener(opener)

        # get the main page to get a cookie (see bug  #13)
        try:
            urllib.request.urlopen(Cleverbot.PROTOCOL + Cleverbot.HOST)
        except urllib.request.HTTPError as ex:
            print(ex)

    def ask(self, question):
        """Asks Cleverbot a question.

        Maintains message history.

        Args:
            q (str): The question to ask
        Returns:
            Cleverbot's answer
        """
        # Set the current question
        self.data['stimulus'] = question

        # Connect to Cleverbot's API and remember the response
        try:
            self.resp = self._send()
        except urllib.request.HTTPError:
            # request failed. returning empty string
            return str()

        return self._parse()

    def _send(self):
        """POST the user's question and all required information to the
        Cleverbot API
        Cleverbot tries to prevent unauthorized access to its API by
        obfuscating how it generates the 'icognocheck' token, so we have
        to URLencode the data twice: once to generate the token, and
        twice to add the token to the data we're sending to Cleverbot.
        """
        # Set data as appropriate
        if self.conversation:
            linecount = 1
            for line in reversed(self.conversation):
                linecount += 1
                self.data['vText' + str(linecount)] = line
                if linecount == 8:
                    break

        # Generate the token
        enc_data = urllib.parse.urlencode(self.data).encode('utf-8')
        digest_txt = enc_data[9:35]
        token = hashlib.md5(digest_txt).hexdigest()
        self.data['icognocheck'] = token

        # Add the token to the data
        enc_data = urllib.parse.urlencode(self.data)
        enc_data = enc_data.encode('utf-8')
        conn = urllib.request.urlopen(self.API_URL, enc_data)

        # POST the data to Cleverbot's API
        # conn = urllib.request.urlopen(req)
        resp = str(conn.read())

        # Return Cleverbot's response
        return resp

    def _parse(self):
        """Parses Cleverbot's response"""
        parsed = self.resp[1:].split('\\r\\r\\r\\r\\r\\')
        cleaned_list = []
        for item in parsed:
            cleaned_list.append(item.split('\\r'))

        return cleaned_list[0][0].replace("'", "").replace('"', '')
