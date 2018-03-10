import urllib.parse
import urllib.request
import json
import re
import time
import datetime
import http.client
import os
from bs4 import BeautifulSoup
from bs4.diagnose import diagnose
from datetime import timezone

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(dir_path+'/config.json', 'r') as cf:
    config = json.load(cf)

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

def saveKills(kills):
    with open(dir_path+'/database/kills.json', 'w') as file:
        json.dump(kills, file, False, True, True, True, None, 4)

def loadKill(unique):
    try:
        file = open(dir_path+'/database/kills.json', 'r')
        kills = json.load(file)
    except:
        file = open(dir_path+'/database/kills.json', 'w+')
        kills = []
        json.dump(kills, file)
    for kill in kills:
        if kill['unique'] == unique:
            return kill
    return None

def loadFriends():
    with open(dir_path+'/friends.json', 'r') as file:
        return json.load(file)

def msg(msg, webhook):
    conn = http.client.HTTPSConnection('hooks.slack.com')
    conn.request(
        'POST',
        webhook,
        urllib.parse.urlencode({'payload': json.dumps({'text': msg})}),
        {"Content-type": "application/x-www-form-urlencoded"}
    )
    response = conn.getresponse()
    conn.close()
    print(msg)
    if response.status != 200:
        raise Exception('Error '+str(response.status)+': '+response.reason)

def notif(msg):
    msg(msg, config['webhook-sro-notifier'])

def private(msg):
    msg(msg, config['webhook-sro'])

def isFriend(target):
    friends = loadFriends()
    for friend in friends:
        for char in friend['chars']:
            if char['name'] == target or char['job'] == target
                return friend
    return False

def updateKills():
    dataKills = BeautifulSoup(
        urllib.request.urlopen('https://www.m3stat.com/uniques/'+config['server']).read(),
        'html.parser'
    )

    kills = []
    for tr in dataKills.find('div', {'name': 'last_kills'}).table.tbody.find_all('tr', {}, False):
        if not tr.has_attr('style'):
            tds = tr.find_all('td', {}, False)
            unique = tds[0].get_text()[2:]
            oldKill = loadKill(unique)
            t = ts(tds[2].get_text())
            newKill = {
                'unique': unique,
                'player': tds[1].get_text(),
                'timestamp': t,
                'date': datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S'),
            }
            kills.append(newKill)
            if oldKill == None or (
                (oldKill['timestamp']+60) < newKill['timestamp']
            ):
                if newKill['player'] == '(Spawned)':
                    notif('*'+newKill['unique']+'* est apparu !')
                else:
                    notif('`'+newKill['player']+'` a éliminé *'+newKill['unique']+'*')

                # Friends
                friend = isFriend(newKill['player'])
                if friend != False
                    private('@'+friend['slack']+' a éliminé *'+newKill['unique']+'* avec `'+newKill['player']+'`')

    saveKills(kills)

updateKills()