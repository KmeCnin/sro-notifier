import urllib.parse
import urllib.request
import re
from bs4 import BeautifulSoup

from src import config
from src import manager

def update():
    cf = config.Config()
    chars = manager.Chars()
    for friend in manager.Friends().list:
        for char in friend['chars']:
            dataChar = BeautifulSoup(
                urllib.request.urlopen('https://www.m3stat.com/players/'+cf.get('server')+'/'+char['name']).read(),
                'html.parser'
            )
            charData = chars.findByName(char['name'])
            oldLevel = None
            if charData is not None:
                oldLevel = charData['level']
            m = re.search('(\d+)\sLevel', dataChar.find('h4').get_text())
            if m is None:
                continue
            newLevel = int(m.group(1))
            chars.push({
                'name': char['name'],
                'level': newLevel,
            })
            if oldLevel is None:
                continue
            if oldLevel < newLevel:
                publisher.publishPrivate(
                    {
                        'text': '<@'+friend['slack']+'> est maintenant niveau *'+str(newLevel)+' * avec `'+char['name']+'` !'
                    }
                )

    chars.persist()