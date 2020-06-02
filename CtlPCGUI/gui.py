#!/usr/bin/env python3

from browsergui import GUI, Text, Button, List, Grid
from packages.rasps import Rasberries, Raspberry
from packages.songs import Songs, Song

''''
RBs = Rasberries()
Songs = Songs()

RB = Raspberry(RBs)
RB = Raspberry(RBs)
RB = Raspberry(RBs)


for ele in RBs.Rasplist:
    print(f"In RBs {ele.name}, ele.IP {ele.IP}")

'''
Songs.read_json()

Son = Song(name="Resistance", parent=RBs)
Song = Song(name="Marscha", parent=RBs)
'''
print(f"{RB.name}, {RB.IP}, {RB.description}")


'''for ele in Songs.Songlist:
    print(f"In Songs {ele.name}")'''

'''
while len(Songs.Songlist) > 1:
    for sng in Songs.Songlist:
        print(f"remove {sng.name}")
        sng.remove()'''

'''for ele in Songs.Songlist:
    print(f"In Songs after {ele.name}")'''

Songs.write_json()

RBs.write_json()
''''


class Lyout1(GUI):
    def __init__(self, **kwargs):
        super(Lyout1, self).__init__(**kwargs)

        self.songlist = ["Arcade Riot", "Resistance",
                         "MadMenSin", "RussianStandard"]

        title = Text("Marshall AR.TS Live Suit")
        self.body.append(title)
        self.guilist()

    def guilist(self):
        if len(self.body) > 1:
            self.body.remove(self.songgrid)
        self.songgrid = Grid(n_rows=len(self.songlist), n_columns=2)
        for num, song in enumerate(self.songlist):
            b = Button(text=song, callback=self.testcallback)
            t = Text(song)
            self.songgrid[num, 0] = t
            self.songgrid[num, 1] = b
       # self.body.append(self.songgrid)
        self.reset()

    def testcallback(self):
        self.songlist.append("Mehr")
        print("append mehr")
        for s in self.songlist:
            print(s)
        self.guilist()
        self.reset()

    def reset(self):
        # if self.songgrid in self.body:

        print("In Reset")
        self.body.append(self.songgrid)


def main():
    RBs = Rasberries()
    RBs.read_json()
    Songs = Songs()
    Songs.read_json()

    Lyout1().run()


if __name__ == '__main__':
    main()
