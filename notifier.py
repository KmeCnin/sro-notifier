import urllib.parse
import urllib.request
import json
import re
import time
import http.client
import os
from bs4 import BeautifulSoup

domain = 'https://www.m3stat.com'
server = 'Palmyra'

dir_path = os.path.dirname(os.path.realpath(__file__))

def ts(string):
    m = re.search('(\d+)d, (\d+)h, (\d+)m', string)
    d = int(m.group(1)) * 24 * 60 * 60
    h = int(m.group(2)) * 60 * 60
    m = int(m.group(3)) * 60
    elapsed = d + h + m
    return int(time.time()) - int(elapsed)

def saveKills(kills):
    with open(dir_path+'/kills.json', 'w') as file:
        json.dump(kills, file, False, True, True, True, None, 4)

def loadKill(unique):
    with open(dir_path+'/kills.json', 'r') as file:
        kills = json.load(file)
    for kill in kills:
        if kill['unique'] == unique:
            return kill
    return None

def msg(msg):
    conn = http.client.HTTPSConnection('hooks.slack.com')
    conn.request(
        'POST',
        '/services/T0B0Z6SKB/B9L0J4848/C7uDdHncmIXZ2QE6Tys2hJPy',
        urllib.parse.urlencode({'payload': json.dumps({'text': msg})}),
        {"Content-type": "application/x-www-form-urlencoded"}
    )
    response = conn.getresponse()
    conn.close()
    # print(msg)
    if response.status != 200:
        raise Exception('Error '+str(response.status)+': '+response.reason)

def updateKills():
    dataKills = BeautifulSoup(
        urllib.request.urlopen(domain+'/uniques/'+server).read(),
        'lxml'
    )
    kills = []
    foo = 0
    for tr in dataKills.select('[name=last_kills] > table > tbody > tr'):
        # print(tr)
            # foo = foo+1
            # print(foo)
        if not tr.has_attr('style'):
            tds = tr.select('td')
            unique = tds[0].get_text()[2:]
            oldKill = loadKill(unique)
            newKill = {
                'unique': unique,
                'player': tds[1].get_text(),
                'timestamp': ts(tds[2].get_text()),
            }
            kills.append(newKill)
            if oldKill == None or oldKill['timestamp'] > (newKill['timestamp']+60):
                if newKill['player'] == '(Spawned)':
                    msg(newKill['unique']+' has appeared!')
                else:
                    msg(newKill['player']+' killed '+newKill['unique'])
    saveKills(kills)

updateKills()