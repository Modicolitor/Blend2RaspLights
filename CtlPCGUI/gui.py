#!/usr/bin/env python3

from browsergui import GUI, Text, Button, List, Grid, TextField, Container, Dropdown
from packages.rasps import Rasberries, Raspberry
from packages.songs import Songs, Song

RBs = Rasberries()
RBs.read_json()


# raspa = Raspberry(RBs)
# raspb = Raspberry(RBs)


Songs = Songs()
Songs.read_json()

# Sng = Song(name="Resistance", parent=Songs, pis={})
# Sng = Song(name="HellMount", parent=Songs, pis={})

# Songs.write_json()
# RBs.write_json()


class Lyout1(GUI):
    def __init__(self, **kwargs):
        super(Lyout1, self).__init__(**kwargs)

        self.songlist = Songs.Songlist

        self.title = Text("Marshall AR.TS Live Suit")
        self.body.append(self.title)
        # prinbody(self.body)

        self.soedgrid = None

        self.guisonglist()

    def guisonglist(self):
        # if len(self.body) > 1:
        #    self.body.remove(self.songgrid)
        self.cleanUI()
        self.songgrid = Grid(n_rows=len(self.songlist), n_columns=5)
        snglist = Songs.Songlist[:]
        for num, song in enumerate(snglist):
            # print(f"song {song} song.name {song.name} num {num}")

            n = Text(str(num))
            edit = self.sngEditBtn(song)
            play = self.sngPlayBtn(song)
            delete = self.sngDeleteBtn(song)
            t = Text(song.name)
            self.songgrid[num, 0] = n
            self.songgrid[num, 1] = t
            self.songgrid[num, 2] = edit
            self.songgrid[num, 3] = delete
            self.songgrid[num, 4] = play
        # self.body.append(self.songgrid)

        self.newSngBtn = Button(text="New Song", callback=self.newsong)
        self.spacer = Text("      ---------------         ")
        self.RaspMenuButton = self.raspMenuBtn()
        self.Bottombutton = Container(
            self.newSngBtn, self.spacer,  self.RaspMenuButton)
        # self.body.append(self.newSngBtn)
        # prinbody(self.body)
        self.cleanUI()
        self.updatesonggrid()

    def sngDeleteBtn(self, song):
        def callback():
            song.remove()
            Rasplist = RBs.Rasplist[:]

            for pi in Rasplist:
                songs = pi.songs.copy()
                for sng in songs:
                    if song.name == sng:
                        pi.songs.pop(sng)
            self.guisonglist()
        return Button(text="Delete", callback=callback)

    def raspMenuBtn(self):
        def callback():
            self.guiRasplist()
        return Button(text="Raspberry Menu", callback=callback)

    def sngEditBtn(self, song):
        def callback():
            self.EditSong(song)
        return Button(text="edit", callback=callback)

    def sngPlayBtn(self, song):
        def callback():
            song.playRasps()
            song.playVideo()
        return Button(text="Play", callback=callback)

    def sng_raspUpdateBtn(self, rasps, rasp, song):
        def callback():
            rasps[rasp] = self.rfilenameTfield.value

            for ras in RBs.Rasplist:
                if ras.name == rasp:
                    ras.songs[song.name] = self.rfilenameTfield.value

            # self.EditSong(song)

        return Button(text="Update", callback=callback)

    def sng_raspDeleteBtn(self, song, rasp):
        def callback():
            song.removeRasp(rasp)

            for ras in RBs.Rasplist:
                if ras.name == rasp:
                    ras.removeSong(song.name)
            self.EditSong(song)
        return Button(text="Delete", callback=callback)

    def newsong(self):

        sng = Song(name="Default", parent=Songs, pis={})
        RBs.write_json()
        Songs.write_json
        self.guisonglist()

    def updatesonggrid(self):
        self.cleanUI()
        self.body.append(self.title)
        self.body.append(self.songgrid)
        # self.body.append(self.newSngBtn)
        self.body.append(self.Bottombutton)
        # if self.soedgrid != None:
        #    self.body.append(self.soedgrid)

        # self.body.append(self.songgrid)

    def cleanUI(self):
        bo = self.body[:]
        for e in bo:
            # print(f"delete element {e}")
            self.body.remove(e)

    def EditSong(self, song):
        self.cleanUI()
        # print(song.name)
        self.soedgrid = Grid(n_rows=3, n_columns=3)
        # if self.soedgrid in self.body:
        #    self.body.remove(self.soedgrid)
        n1 = Text("Name")
        n2 = Text("used_pis")
        n3 = Text("description")
        nda1 = Text(song.name)
        nda2 = Text(str(song.used_pis))
        nda3 = Text(song.description)

        self.ns1 = TextField(value=song.name)
        self.ns2 = TextField("pis")
        self.ns3 = TextField(value=song.description)

        self.soedgrid[0, 0] = n1
        self.soedgrid[1, 0] = n2
        self.soedgrid[2, 0] = n3
        self.soedgrid[0, 1] = nda1
        self.soedgrid[1, 1] = nda2
        self.soedgrid[2, 1] = nda3
        self.soedgrid[0, 2] = self.ns1
        # self.soedgrid[1, 2] = self.ns2
        self.soedgrid[2, 2] = self.ns3
        trenner = Text(
            "---------------------------------------------------------------------")
        # Rasplist of this song with filename
        self.rasedgrid = Grid(n_rows=len(song.used_pis), n_columns=5)
        for num, rasp in enumerate(song.used_pis):
            # print(str(num) + rasp)
            rname = Text(str(rasp))
            rfilename = Text(str(song.used_pis[rasp]))
            self.rfilenameTfield = TextField(value=song.used_pis[rasp])

            rupdate = self.sng_raspUpdateBtn(
                song.used_pis, rasp, song)
            rdelete = self.sng_raspDeleteBtn(song, rasp)
            self.rasedgrid[num, 0] = rname
            self.rasedgrid[num, 1] = rfilename
            self.rasedgrid[num, 2] = self.rfilenameTfield
            self.rasedgrid[num, 3] = rupdate
            self.rasedgrid[num, 4] = rdelete

        # dropdown = Dropdown(['Dr', 'op', 'do', 'wn'])
        newText = Text("New Rasp")
        RaspNamelist = []
        for ra in RBs.Rasplist:
            if ra.name not in song.used_pis:
                RaspNamelist.append(ra.name)
        RaspNamelist.append("  ")
        self.raspsdrop = Dropdown(RaspNamelist)
        self.newrasfilename = TextField(value="Unknown File")
        raddButton = self.appendRasptoSongBtn(song)
        self.NewRaspCont = Container(
            newText, self.raspsdrop, self.newrasfilename, raddButton)

        # print("appending EditSong UI")
        self.body.append(self.title)
        self.body.append(self.soedgrid)
        # self.body.append(self.rasedgrid)
        self.body.append(self.rasedgrid)
        self.body.append(self.NewRaspCont)
        saveBtn = self.songeditsaveBtn(song)
        self.body.append(saveBtn)

        # self.cleanUI()

    def appendRasptoSongBtn(self, song):
        def callback():
            song.addRasp(self.raspsdrop.value, self.newrasfilename.value)

            for rasp in RBs.Rasplist:
                print(f"rasps vorhanden {rasp.name}")
                if self.raspsdrop.value == rasp.name:
                    print(
                        f"rasps richtig {rasp.name} drop value {self.raspsdrop.value}")
                    rasp.addSong(song.name, self.newrasfilename.value)
            # tester
            for rasp in RBs.Rasplist:
                for sng in rasp.songs:
                    print(f"in rasp {rasp.name} song {sng}")
                # break

            self.EditSong(song)
        return Button(text="Add", callback=callback)

    def songeditsaveBtn(self, song):
        def callback():
            # when the name changes name of song in rasp.songliste will be changed
            Rasplist = RBs.Rasplist.copy()
            for rasp in Rasplist:
                songs = rasp.songs.copy()
                print(f"rasp.songs {songs} for rasp {rasp.name}")
                for sng in songs:
                    print(
                        f"song found in rrasps songs: {sng} song.name {song.name}")
                    if sng == song.name:
                        # remove song from list
                        rasp.addSong(self.ns1.value, rasp.songs[song.name])
                        # rasp.songs.pop(song.name)

                        # add new instance with new name

            song.name = self.ns1.value
            song.description = self.ns3.value

            RBs.write_json()
            Songs.write_json()
            # self.cleanUI()
            self.guisonglist()
        return Button(text="Save", callback=callback)
    ##########################Rasppart #############

    def guiRasplist(self):
        # if len(self.body) > 1:
        #    self.body.remove(self.songgrid)
        self.cleanUI()
        self.raspgrid = Grid(n_rows=len(RBs.Rasplist),
                             n_columns=5)
        rasplist = RBs.Rasplist[:]
        for num, rasp in enumerate(rasplist):
            # print(f"song {song} song.name {song.name} num {num}")

            n = Text(str(num))
            t = Text(rasp.name)
            ip = Text(rasp.IP)
            redit = self.raspEditBtn(rasp)
            rdelete = self.raspDeleteBtn(rasp)

            self.raspgrid[num, 0] = n
            self.raspgrid[num, 1] = t
            self.raspgrid[num, 2] = ip
            self.raspgrid[num, 3] = redit
            self.raspgrid[num, 4] = rdelete

        self.newRaspBtn = Button(text="New Rasp", callback=self.newrasp)
        self.songmenubtn = self.songMenuBtn()
        self.body.append(self.raspgrid)
        self.body.append(self.newRaspBtn)
        self.body.append(self.songmenubtn)

        # prinbody(self.body)
        # self.cleanUI()
        # self.updatesonggrid()

    def editRaspMenu(self, rasp):
        self.cleanUI()

        self.raspedgrid = Grid(n_rows=3, n_columns=3)
        RaspMenuTitle = Text(f"Editiere {rasp.name}")
        n1 = Text("Name")
        n2 = Text("IP")
        n3 = Text("Description")
        nda1 = Text(rasp.name)
        nda2 = Text(str(rasp.IP))
        nda3 = Text(rasp.description)

        self.rnamefield = TextField(value=rasp.name)
        self.rIPfield = TextField(value=rasp.IP)
        self.rDescfield = TextField(value=rasp.description)

        self.raspedgrid[0, 0] = n1
        self.raspedgrid[1, 0] = n2
        self.raspedgrid[2, 0] = n3
        self.raspedgrid[0, 1] = nda1
        self.raspedgrid[1, 1] = nda2
        self.raspedgrid[2, 1] = nda3
        self.raspedgrid[0, 2] = self.rnamefield
        self.raspedgrid[1, 2] = self.rIPfield
        self.raspedgrid[2, 2] = self.rDescfield
        trenner = Text(
            "---------------------------------------------------------------------")
        # Songlist
        self.raspSonglistgrid = Grid(n_rows=len(rasp.songs), n_columns=5)
        for num, sng in enumerate(rasp.songs):
            sngname = Text(sng)
            sngfilename = Text(rasp.songs[sng])
            self.sngFiletextfield = TextField(value=rasp.songs[sng])

            updateBtn = self.rsngupdateBtn(rasp.songs, sng, rasp)
            deleteBtn = self.rsngdeleteBtn(rasp.songs, sng, rasp)

            self.raspSonglistgrid[num, 0] = sngname
            self.raspSonglistgrid[num, 1] = sngfilename
            self.raspSonglistgrid[num, 2] = self.sngFiletextfield
            self.raspSonglistgrid[num, 3] = updateBtn
            self.raspSonglistgrid[num, 4] = deleteBtn

        # song dropdown
        newText = Text("New Song")
        RaspNamelist = []
        print(f"rasp songs {Songs.Songlist}")
        print(f"rasp songs {rasp.songs}")
        for son in Songs.Songlist:
            if son.name not in rasp.songs:
                RaspNamelist.append(son.name)
        RaspNamelist.append("  ")
        self.rsongdrop = Dropdown(RaspNamelist)
        self.newrasfilename = TextField(value="Unknown File")

        self.raddButton = self.appendsongtoraspbtn(
            rasp)

        self.NewRSongCont = Container(
            newText, self.rsongdrop, self.newrasfilename, self.raddButton)
        # SaveButton
        saveraspeditBtn = self.saveraspeditBtn(rasp)

        self.body.append(RaspMenuTitle)
        self.body.append(self.raspedgrid)
        self.body.append(trenner)
        self.body.append(self.raspSonglistgrid)
        self.body.append(self.NewRSongCont)
        self.body.append(saveraspeditBtn)

    def rsngupdateBtn(self, songs, song, rasp):
        def callback():
            songs[song] = self.sngFiletextfield.value

            # change song in mainsonglist
            for so in Songs.Songlist:
                if song == so.name:
                    so.addRasp(rasp.name, self.sngFiletextfield.value)
                    break
            self.editRaspMenu(rasp)
        return Button(text="Update", callback=callback)

    def rsngdeleteBtn(self, songs, song, rasp):
        def callback():
            rasp.removeSong(song)
            Songlist = Songs.Songlist[:]
            for so in Songlist:
                if song == so.name:
                    so.removeRasp(rasp.name)
                    break
            self.editRaspMenu(rasp)
        return Button(text="Delete", callback=callback)

    def saveEditdata(self, rasp):
        rasp.name = self.rnamefield.value
        rasp.IP = self.rIPfield.value
        rasp.description = self.rDescfield.value

        RBs.write_json()
        Songs.write_json()

    def saveraspeditBtn(self, rasp):
        def callback():
            self.saveEditdata(rasp)
            self.guiRasplist()
        return Button(text="Save", callback=callback)

    def appendsongtoraspbtn(self, rasp):
        def callback():
            songstr = self.rsongdrop.value
            filename = self.newrasfilename.value
            rasp.addSong(songstr, filename)
            self.saveEditdata(rasp)

            for song in Songs.Songlist:
                if song.name == self.rsongdrop.value:
                    song.addRasp(rasp.name, self.newrasfilename.value)
                    break

            self.editRaspMenu(rasp)
        return Button(text="Add", callback=callback)

    def songMenuBtn(self):
        def callback():
            # RBs.write_json()
            # Songs.write_json()
            self.guisonglist()

        return Button(text="Songlist", callback=callback)

    def newrasp(self):

        newrasp = Raspberry(parent=RBs)
        self.guiRasplist()

    def raspEditBtn(self, rasp):
        def callback():
            self.editRaspMenu(rasp)
        return Button(text="Edit", callback=callback)

    def raspDeleteBtn(self, rasp):
        def callback():
            print(f"Deleted {rasp.name}")
            rasp.removeRasp()

            for song in Songs.Songlist:
                for pi in song.used_pis:
                    if pi == rasp.name:
                        song.removeRasp(pi)

        return Button(text="Delete", callback=callback)


def main():

    Lyout1().run()


if __name__ == '__main__':
    main()
