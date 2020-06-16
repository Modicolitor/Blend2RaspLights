import json
import time
#import threading
from pathlib import Path


class Rasberries():
    def __init__(self):
        self.Rasplist = []

    def add(self, rasp):
        self.Rasplist.append(rasp)

    def write_json(self):
        data = {}
        data['rasps'] = []
        for d in self.Rasplist:
            data['rasps'].append({
                'name': d.name,
                'IP': d.IP,
                'Songs': self.songs,
                'description': d.description
            })

        with open('user_rasps.json', 'w') as outfile:
            json.dump(data, outfile)

    def read_json(self):

        my_file = Path("user_rasps.json")
        if my_file.is_file():
            with open('user_rasps.json') as json_file:
                data = json.load(json_file)
                for p in data['rasps']:
                    # print(f"generating {p.name}")
                    rsp = Raspberry(parent=self)
                    rsp.IP = p['IP']
                    rsp.songs = p['Songs']
                    rsp.decription = p['description']


class Raspberry(Rasberries):
    def __init__(self, parent):
        self.name = "Rasp"  # + str(len(.Rasplist))
        self.IP = "10.1.0.20"
        self.description = ""
        self.parent = parent
        self.songs = {}

        parent.add(self)

    def ping(self):
        print("ping")

    def play(self):
        print("bambam lights on")

    def edit(self):
        print("editieren")

    def test(self):
        print("editieren")

    def addSong(self, song, filename):
        self.songs[song.name] = filename

    def removeSong(self, song):
        self.songs.pop(song.name)
