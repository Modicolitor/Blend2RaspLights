#!/usr/bin/env python3

from browsergui import GUI, Text, Button, List, Grid
from packages.rasps import Rasberries, Raspberry
from packages.songs import Songs, Song

RBs = Rasberries()
RBs.read_json()

raspa = Raspberry(RBs)
raspb = Raspberry(RBs)


Songs = Songs()
Songs.read_json()


#Sng = Song(name="Resistance", parent=Songs)
#Sng = Song(name="HellMount", parent=Songs)

# Songs.write_json()
# RBs.write_json()


class Lyout1(GUI):
    def __init__(self, **kwargs):
        super(Lyout1, self).__init__(**kwargs)

        self.songlist = Songs.Songlist

        title = Text("Marshall AR.TS Live Suit")
        self.body.append(title)
        self.guisonglist()

    def guisonglist(self):
        # if len(self.body) > 1:
        #    self.body.remove(self.songgrid)
        self.songgrid = Grid(n_rows=len(self.songlist), n_columns=4)
        print(Songs,)
        for num, song in enumerate(Songs.Songlist):
            print(f"song {song} song.name {song.name} num {num}")
            n = Text(str(num))
            edit = Button(text="edit", callback=song.edit)
            play = Button(text="play", callback=song.play)
            t = Text(song.name)
            self.songgrid[num, 0] = n
            self.songgrid[num, 1] = t
            self.songgrid[num, 2] = edit
            self.songgrid[num, 3] = play
        self.body.append(self.songgrid)
        self.reset()

    def testcallback(self):
        self.songlist.append("Mehr")
        print("append mehr")
        for s in self.songlist:
            print(s)
        self.guisonglist()
        self.reset()

    def reset(self):
        # if self.songgrid in self.body:

        print("In Reset")
        self.body.append(self.songgrid)


def main():

    Lyout1().run()


if __name__ == '__main__':
    main()
