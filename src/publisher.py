import http.client
import urllib.parse
import urllib.request
import json

from src import config

class Publisher:

    def __init__(self):

        cf = config.Config()
        self.publicWebhook = cf.get('webhook-sro-notifier')
        self.privateWebhook = cf.get('webhook-sro')

    def publish(self, webhook, msg):
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

    def publishPublic(self, msg):
        # self.publish(self.publicWebhook, msg)

    def publishPrivate(self, msg):
        self.publish(self.privateWebhook, msg)