import json
import time
import threading
from pathlib import Path
# from gui import Lyout1


class Playlists():
    def __init__(self, SongsCol):
        self.Playlistlist = []
        self.Playliststrings = []
        self.SongsCol = SongsCol  # Main SongsObject
        self.active = None

    def add(self, pl):
        self.Playlistlist.append(pl)

    def write_json(self):
        data = {}
        data['pls'] = []

        for d in self.Playlistlist:

            data['pls'].append({
                'name': d.name,
                'used_songs': d.used_songs,
                'description': d.description
            })

        with open('user_pls.json', 'w') as outfile:
            json.dump(data, outfile)
        self.get_playliststrings()

    def read_json(self):
        my_file = Path("user_pls.json")
        if my_file.is_file():
            with open('user_pls.json') as json_file:
                data = json.load(json_file)
                for p in data['pls']:
                    # print(f"generating {p.name}")
                    pl = Playlist(name=p['name'], parent=self)
                    pl.used_songs = p['used_songs']
                    pl.description = p['description']

                    pl.fill_songobj()  # makes the songsob list from the used _songs
        self.get_playliststrings()

    def get_playliststrings(self):
        self.Playliststrings = []
        for ele in self.Playlistlist:
            self.Playliststrings.append(ele.name)


class Playlist(Playlists):
    def __init__(self, name, parent):
        self.name = name
        # song names <-- Dictionary with Pauseafter, and, !!!songlength!!! !!!videofile!!!
        self.used_songs = {}
        self.songs = []  # object songs
        self.description = ""

        self.parent = parent
        self.parent.add(self)

    def remove(self):
        self.parent.Playlistlist.remove(self)
        self.parent.write_json()

    def add_song(self, song, pause, songlenth, videofile):
        self.songs.append(song)

        self.used_songs[song.name] = [pause, songlenth, videofile]
        #plitemdata[0] = pause
        #plitemdata[1] = songlenth
        #plitemdata[2] = videofile
        self.parent.write_json()

    def remove_song(self, song):
        self.used_songs.pop(song.name)
        self.songs.remove(song)
        self.parent.write_json()

    def fill_songobj(self):
        self.songs = []
        for sngname in self.used_songs:
            for songob in self.parent.SongsCol.Songlist:
                if sngname == songob.name:
                    self.songs.append(songob)

    def up(self, song):
        index = self.songs.index(song)
        print(index)
        if index != 0:
            index -= 1
        self.songs.remove(song)
        self.songs.insert(index, song)
        self.update_songlist()

    def down(self, song):
        index = self.songs.index(song)
        print(index)
        print(len(self.songs))
        if index < len(self.songs):
            index += 1

        self.songs.remove(song)
        self.songs.insert(index, song)
        self.update_songlist()

    # update dictionary after resorting pl
    def update_songlist(self):
        self.intermediate = {}
        for sng in self.songs:
            self.intermediate[sng.name] = self.used_songs[sng.name]

        self.used_songs = self.intermediate
