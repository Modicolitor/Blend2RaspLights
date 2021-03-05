import json
import time
#import threading
from pathlib import Path

from os import listdir
from os.path import isfile, join, isdir


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
                'Songs': d.songs,
                'description': d.description
            })

        with open('user_rasps.json', 'w') as outfile:
            json.dump(data, outfile)

    def read_json(self):
        filename = "user_rasps.json"

        folderpath = FM.self.appdatafoldername
        path = join()

        my_file = Path("user_rasps.json")
        if my_file.is_file():
            with open('user_rasps.json') as json_file:
                data = json.load(json_file)
                for p in data['rasps']:
                    # print(f"generating {p.name}")
                    rsp = Raspberry(parent=self)
                    rsp.name = p['name']
                    rsp.IP = p['IP']
                    rsp.songs = p['Songs']
                    rsp.decription = p['description']


class Raspberry(Rasberries):
    def __init__(self, parent):
        self.name = "Rasp"  # + str(len(.Rasplist))
        self.IP = "10.1.0.20"
        self.description = ""
        self.parent = parent
        # <---dict  {songname : ["filename .json","scritps .py"]}
        self.songs = {}

        parent.add(self)

    def removeRasp(self, Rasp):
        self.parent.Rasplist.remove(self)
        self.parent.write_json()

    def play(self):
        print("bambam lights on")

    def edit(self):
        print("editieren")

    def test(self):
        print("editieren")

    def addSong(self, songname, filename, scriptname):
        self.songs[songname] = [filename, scriptname]
        self.parent.write_json()

    def removeSong(self, song):
        self.songs.pop(song)
        self.parent.write_json()
