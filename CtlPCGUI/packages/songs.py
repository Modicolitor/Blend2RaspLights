import json
import time
import threading
from pathlib import Path
#from gui import Lyout1


class Songs():
    def __init__(self):
        self.Songlist = []

    def add(self, song):
        self.Songlist.append(song)

    def write_json(self):
        data = {}
        data['songs'] = []
        for d in self.Songlist:

            data['songs'].append({
                'name': d.name,
                'used_pis': d.used_pis,
                'description': d.description
            })

        with open('user_songs.json', 'w') as outfile:
            json.dump(data, outfile)

    def read_json(self):
        my_file = Path("user_songs.json")
        if my_file.is_file():
            with open('user_songs.json') as json_file:
                data = json.load(json_file)
                for p in data['songs']:
                    #print(f"generating {p.name}")
                    sng = Song(name=p['name'], parent=self)
                    sng.used_pis = p['used_pis']
                    sng.decription = p['description']


class Song(Songs):
    def __init__(self, name, parent):
        self.name = name
        self.used_pis = []
        self.description = ""
        self.parent = parent

        self.parent.add(self)

    def ping(self):
        print("ping")

    def append_pi(self, song):
        self.used_pis.append(song)

    def remove(self):
        self.parent.Songlist.remove(self)

    def play(self):
        print("bambam lights on")

    def edit(self):
        print("editieren")
        return self
