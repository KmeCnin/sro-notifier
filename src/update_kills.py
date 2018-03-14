import urllib.parse
import urllib.request
import manager

def update():
    dataKills = BeautifulSoup(
        urllib.request.urlopen('https://www.m3stat.com/uniques/'+config['server']).read(),
        'html.parser'
    )

    kills = manager.Kills()
    friends = manager.Friends()
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
                    image = loadUnique(newKill['unique'])
                    if image is not None:
                        image = image['spawn']
                    msg(
                        {
                            'text': '*'+newKill['unique']+'* est apparu !',
                            'attachments': [
                                {
                                    "title": "Lieux d'apparition",
                                    'image_url': image
                                }
                            ]
                        },
                        config['webhook-sro-notifier']
                    )
                else:
                    msg(
                        {
                            'text': '`'+newKill['player']+'` a éliminé *'+newKill['unique']+'*'
                        },
                        config['webhook-sro-notifier']
                    )

                # Friends
                friend = friends.findByName(newKill['player'])
                if friend != None:
                    image = loadUnique(newKill['unique'])
                    if image is not None:
                        image = image['wallpaper']
                    msg(
                        {
                            'text': '<@'+friend['slack']+'> a éliminé *'+newKill['unique']+'* avec `'+newKill['player']+'` !',
                            'attachments': [
                                {
                                    "title": "Gratz!",
                                    'image_url': image
                                }
                            ]
                        },
                        config['webhook-sro']
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