import os
import json

from src import config

class Collection:

    def __init__(self, name):
        self.cf = config.Config()
        self.name = name.lower()
        self.inMemoryList = []
        self.persistedList = []
        try:
            file = open(self.cf.databasePath()+self.name+'.json', 'r')
            self.persistedList = json.load(file)
        except:
            file = open(self.cf.databasePath()+self.name+'.json', 'w+')
            json.dump(self.persistedList, file)

    def push(self, item):
        self.inMemoryList.append(item)

    def persist(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(self.cf.databasePath()+self.name+'.json', 'w') as file:
            json.dump(self.inMemoryList, file, False, True, True, True, None, 4)
            self.persistedList = self.inMemoryList
            self.inMemoryList = []

    def find(self, attribute, value):
        for item in self.persistedList:
            if item[attribute] == value:
                return item
        return None

class ImmutableCollection:

    def __init__(self, name):
        self.cf = config.Config()
        self.name = name.lower()
        self.list = []
        with open(self.cf.configPath()+self.name+'.json', 'r') as file:
            self.list = json.load(file)

    def find(self, attribute, value):
        for item in self.list:
            if item[attribute] == value:
                return item
        return None

class Kills(Collection):

    def __init__(self):
        Collection.__init__(self, 'kills')

    def findByUnique(self, unique):
        return Collection.find(self, 'unique', unique)

class Chars(Collection):

    def __init__(self):
        Collection.__init__(self, 'chars')

    def findByName(self, name):
        return Collection.find(self, 'name', name)

class Friends(ImmutableCollection):

    def __init__(self):
        ImmutableCollection.__init__(self, 'friends')

    def findByName(self, name):
        return ImmutableCollection.find(self, 'name', name)

    def findByChar(self, charName):
        for player in self.list:
            for char in player['chars']:
                if char['name'] == charName or char['job'] == charName:
                    return player
        return None

class Uniques(ImmutableCollection):

    def __init__(self):
        ImmutableCollection.__init__(self, 'uniques')

    def findByName(self, name):
        return ImmutableCollection.find(self, 'name', name)