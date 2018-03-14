import os
import json

class Config:
    
    def __init__(self):
        self.dir = os.path.dirname(os.path.realpath(__file__))+'/../'
        with open(self.configPath()+'config.json', 'r') as file:
            self.conf = json.load(file)

    def get(self, attr):
        return self.conf[attr]

    def databasePath(self):
        return self.dir+'database/'

    def configPath(self):
        return self.dir+'config/'