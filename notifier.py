import urllib.parse
import urllib.request
import json
import re
import time
import datetime
import http.client
import os
import src
from bs4 import BeautifulSoup
from bs4.diagnose import diagnose
from datetime import timezone

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(dir_path+'/config.json', 'r') as cf:
    config = json.load(cf)

def msg(msg, webhook):
    conn = http.client.HTTPSConnection('hooks.slack.com')
    conn.request(
        'POST',
        webhook,
        urllib.parse.urlencode({'payload': json.dumps(msg)}),
        {"Content-type": "application/x-www-form-urlencoded"}
    )
    response = conn.getresponse()
    conn.close()
    print(msg['text'])
    if response.status != 200:
        raise Exception('Error '+str(response.status)+': '+response.reason)

src.update_kills.update()
src.update_chars.update()