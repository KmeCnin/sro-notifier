import urllib
import json
import re
import time
import httplib
from bs4 import BeautifulSoup

domain = 'https://www.m3stat.com'
server = 'Palmyra'

def ts(string):
    m = re.search('(\d+)d, (\d+)h, (\d+)m', string)
    d = int(m.group(1)) * 24 * 60 * 60
    h = int(m.group(2)) * 60 * 60
    m = int(m.group(3)) * 60
    elapsed = d + h + m
    return int(time.time()) - int(elapsed)

def saveKills(kills):
    with open('kills.json', 'w') as file:
        json.dump(kills, file)

def loadKill(unique):
    with open('kills.json', 'r') as file:
        kills = json.load(file)
    for kill in kills:
        if kill['unique'] == unique:
            return kill
    return None

def msg(msg):
    conn = httplib.HTTPSConnection('hooks.slack.com')
    conn.request(
        'POST',
        '/services/T0B0Z6SKB/B9L0J4848/C7uDdHncmIXZ2QE6Tys2hJPy',
        urllib.urlencode({'payload': json.dumps({'text': msg})}),
        {"Content-type": "application/x-www-form-urlencoded"}
    )
    response = conn.getresponse()
    conn.close()
    print(msg)
    if response.status != 200:
        raise Exception('Error '+str(response.status)+': '+response.reason)

def updateKills():
    dataKills = BeautifulSoup(
        urllib.urlopen(domain+'/uniques/'+server).read(),
        'html.parser'
    )
    kills = []
    for tr in dataKills.select('[name=last_kills] > table > tbody > tr'):
        if not tr.has_attr('id'):
            unique = tr.select_one('td:nth-of-type(1)').get_text()[2:]
            oldKill = loadKill(unique)
            newKill = {
                'unique': unique,
                'player': tr.select_one('td:nth-of-type(2)').get_text(),
                'timestamp': ts(tr.select_one('td:nth-of-type(3)').get_text()),
            }
            kills.append(newKill)
            if oldKill == None or oldKill['timestamp'] > newKill['timestamp']+60:
                # Kill has been updated
                if newKill['player'] == '(Spawned)':
                    # New spawn
                    msg(newKill['unique']+' has appeared!')
                else:
                    # New kill
                    msg(newKill['player']+' killed '+newKill['unique'])
    saveKills(kills)

updateKills()