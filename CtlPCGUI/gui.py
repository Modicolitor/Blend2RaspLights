#!/usr/bin/env python3

from browsergui import GUI, Text, Button, List, Grid, TextField
from packages.rasps import Rasberries, Raspberry
from packages.songs import Songs, Song

RBs = Rasberries()
RBs.read_json()

raspa = Raspberry(RBs)
raspb = Raspberry(RBs)


Songs = Songs()
Songs.read_json()


# Sng = Song(name="Resistance", parent=Songs)
# Sng = Song(name="HellMount", parent=Songs)

# Songs.write_json()
# RBs.write_json()

def prinbody(body):
    for ele in body:
        print(ele)


class Lyout1(GUI):
    def __init__(self, **kwargs):
        super(Lyout1, self).__init__(**kwargs)

        self.songlist = Songs.Songlist

        self.title = Text("Marshall AR.TS Live Suit")
        self.body.append(self.title)
        prinbody(self.body)

        self.soedgrid = None

        self.guisonglist()

    def guisonglist(self):
        # if len(self.body) > 1:
        #    self.body.remove(self.songgrid)
        self.cleanUI()
        self.songgrid = Grid(n_rows=len(self.songlist), n_columns=4)
        snglist = Songs.Songlist[:]
        for num, song in enumerate(snglist):
            print(f"song {song} song.name {song.name} num {num}")

            n = Text(str(num))
            edit = Button(text="edit")

            @edit.def_callback
            def button_clicked():
                self.cleanUI()
                self.EditSong(song)

            play = Button(text="play")
            t = Text(song.name)
            self.songgrid[num, 0] = n
            self.songgrid[num, 1] = t
            self.songgrid[num, 2] = edit
            self.songgrid[num, 3] = play
        # self.body.append(self.songgrid)

        self.newSngBtn = Button(text="New Song", callback=self.newsong)
        # self.body.append(self.newSngBtn)
        # prinbody(self.body)
        self.cleanUI()
        self.updatesonggrid()

    def newsong(self):

        sng = Song(name="Default", parent=Songs)

        # print("append mehr")
        # for s in self.songlist:
        #    print(s)
        self.guisonglist()
        # self.updatesonggrid()

    def updatesonggrid(self):
        self.cleanUI()
        self.body.append(self.title)
        self.body.append(self.songgrid)
        self.body.append(self.newSngBtn)

        # if self.soedgrid != None:
        #    self.body.append(self.soedgrid)

        # self.body.append(self.songgrid)

    def cleanUI(self):
        for e in self.body:
            self.body.remove(e)

    def EditSong(self, song):
        self.cleanUI()
        print(song.name)
        self.soedgrid = Grid(n_rows=3, n_columns=3)
        if self.soedgrid in self.body:
            self.body.remove(self.soedgrid)
        n1 = Text("Name")
        n2 = Text("used_pis")
        n3 = Text("description")
        nda1 = Text(song.name)
        nda2 = Text(str(song.used_pis))
        nda3 = Text(song.description)

        ns1 = TextField(value=song.name)
        ns2 = TextField("pis")
        ns3 = TextField(value=song.description)

        self.soedgrid[0, 0] = n1
        self.soedgrid[1, 0] = n2
        self.soedgrid[2, 0] = n3
        self.soedgrid[0, 1] = nda1
        self.soedgrid[1, 1] = nda2
        self.soedgrid[2, 1] = nda3
        self.soedgrid[0, 2] = ns1
        self.soedgrid[1, 2] = ns2
        self.soedgrid[2, 2] = ns3

        print("appending EditSong UI")
        self.body.append(self.title)
        self.body.append(self.soedgrid)

        saveBtn = Button("Save")
        self.body.append(saveBtn)

        @saveBtn.def_callback
        def button_clicked():
            #
            song.name = ns1.value
            # song.rasps =
            song.description = ns3.value
            # self.cleanUI()
            self.guisonglist()


def main():

    Lyout1().run()


if __name__ == '__main__':
    main()
