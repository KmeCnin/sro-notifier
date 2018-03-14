import manager

def update():
    chars = manager.Chars()
    friends = manager.Friends()
    for friend in friends:
        for char in friend['chars']:
            dataChar = BeautifulSoup(
                urllib.request.urlopen('https://www.m3stat.com/players/'+config['server']+'/'+char['name']).read(),
                'html.parser'
            )
            charData = loadChar(char['name'])
            oldLevel = None
            if charData is not None:
                oldLevel = charData['level']
            m = re.search('(\d+)\sLevel', dataChar.find('h4').get_text())
            if m is None:
                continue
            newLevel = int(m.group(1))
            chars.push({
                'char': char['name'],
                'level': newLevel,
            })
            if oldLevel is None:
                continue
            if oldLevel < newLevel:
                msg(
                    {
                        'text': '<@'+friend['slack']+'> est maintenant niveau *'+str(newLevel)+' * avec `'+char['name']+'` !'
                    },
                    config['webhook-sro']
                )

    chars.persist()