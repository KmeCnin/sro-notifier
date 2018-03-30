import urllib.parse
import urllib.request
import re
import time
import datetime
from datetime import timezone
from bs4 import BeautifulSoup

from src import config
from src import manager
from src import publisher as p

def update():
    cf = config.Config()
    dataKills = BeautifulSoup(
        urllib.request.urlopen('https://www.m3stat.com/uniques/'+cf.get('server')).read(),
        'html.parser'
    )

    kills = manager.Kills()
    friends = manager.Friends()
    uniques = manager.Uniques()
    publisher = p.Publisher()
    for tr in dataKills.find('div', {'name': 'last_kills'}).table.tbody.find_all('tr', {}, False):
        if not tr.has_attr('style'):
            tds = tr.find_all('td', {}, False)
            unique = tds[0].get_text()[2:]
            oldKill = kills.findByUnique(unique)
            t = ts(tds[2].get_text())
            newKill = {
                'unique': unique,
                'player': tds[1].get_text(),
                'timestamp': t,
                'date': datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S'),
            }
            kills.push(newKill)
            if oldKill == None or (
                (oldKill['timestamp']+60) < newKill['timestamp']
            ):
                if newKill['player'] == '(Spawned)':
                    image = uniques.findByName(newKill['unique'])
                    if image is not None:
                        image = image['spawn']
                    publisher.publishPublic(
                        {
                            'text': '*'+newKill['unique']+'* est apparu !',
                            'attachments': [
                                {
                                    "title": "Lieux d'apparition",
                                    'image_url': image
                                }
                            ]
                        }
                    )
                else:
                    publisher.publishPublic(
                        {
                            'text': '`'+newKill['player']+'` a éliminé *'+newKill['unique']+'*'
                        }
                    )

                # Friends
                friend = friends.findByChar(newKill['player'])
                if friend != None:
                    image = uniques.findByName(newKill['unique'])
                    if image is not None:
                        image = image['wallpaper']
                    link = 'https://www.m3stat.com/players/Palmyra/'+newKill['player']

                    publisher.publishPrivate(
                        {
                            'text': '<@'+friend['slack']+'> a éliminé *'+newKill['unique']+'* avec <'+link+'|'+newKill['player']+'> !',
                            'attachments': [
                                {
                                    "title": "Gratz!",
                                    "image_url": image,
                                }
                            ]
                        }
                    )

    kills.persist()

def ts(string):
    m = re.search('(\d+)d, (\d+)h, (\d+)m', string)
    d = int(m.group(1)) * 24 * 60 * 60
    h = int(m.group(2)) * 60 * 60
    m = int(m.group(3)) * 60
    elapsed = d + h + m
    ts = int(time.time()) - int(elapsed)
    dt = datetime.datetime.fromtimestamp(ts)
    dt -= datetime.timedelta(
        minutes=0,
        seconds=dt.second,
        microseconds=dt.microsecond
    )
    return int(dt.replace(tzinfo=timezone.utc).timestamp())