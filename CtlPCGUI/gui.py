#!/usr/bin/env python3

from browsergui import GUI, Text, Button, List, Grid, TextField, Container, Dropdown
from packages.rasps import Rasberries, Raspberry
from packages.songs import Songs, Song
from packages.filemanager import Filemanager, Communicator
from packages.playlists import Playlists, Playlist


RBs = Rasberries()
RBs.read_json()


# raspa = Raspberry(RBs)
# raspb = Raspberry(RBs)


Songs = Songs(RBs)
Songs.read_json()
Songs.update_songs()

PLs = Playlists(Songs)
# try:
PLs.read_json()
# except:
# PLs.write_json()


FM = Filemanager()
COM = Communicator(FM)


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

    def GuiMain_BtnGrid(self):
        self.cleanUI()
        self.title = Text("Marshall AR.TS Live Suit")

        PLMenuButton = self.PLMenuBtn()
        songmenubtn = self.songMenuBtn()
        RaspMenuButton = self.raspMenuBtn()
        PlayMenuBtn = self.playMenuBtn()

        self.MainButtongrid = Grid(n_rows=1, n_columns=4)
        self.MainButtongrid[0, 0] = songmenubtn
        self.MainButtongrid[0, 1] = RaspMenuButton
        self.MainButtongrid[0, 2] = PLMenuButton
        self.MainButtongrid[0, 3] = PlayMenuBtn

        self.body.append(self.title)
        self.body.append(self.MainButtongrid)

    def guisonglist(self):
        # if len(self.body) > 1:
        #    self.body.remove(self.songgrid)
        self.GuiMain_BtnGrid()
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

        sngnameTF = TextField(value="Default")
        self.newSngBtn = self.newsongBtn(sngnameTF)
        self.spacer = Text("      ---------------         ")
        #self.RaspMenuButton = self.raspMenuBtn()
        #PLMenuButton = self.PLMenuBtn()
        self.Bottombutton = Container(sngnameTF, self.newSngBtn)
        # self.body.append(self.newSngBtn)
        # prinbody(self.body)
        # self.cleanUI()
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
            COM.play_song(song)
            # song.playRasps()
            # song.playVideo()
        return Button(text="Play", callback=callback)

    def sng_raspUpdateBtn(self, rasps, rasp, song, dropdown):
        def callback():
            rasps[rasp] = dropdown.value

            for ras in RBs.Rasplist:
                print(f"ras.name {ras.name} == rasp as string {rasp}")
                if ras.name == rasp:
                    ras.songs[song.name] = dropdown.value

            self.EditSong(song)

        return Button(text="Update", callback=callback)

    def sng_raspDeleteBtn(self, song, rasp):
        def callback():
            song.removeRasp(rasp)

            for ras in RBs.Rasplist:
                if ras.name == rasp:
                    ras.removeSong(song.name)
            self.EditSong(song)
        return Button(text="Delete", callback=callback)

    def newsongBtn(self, nametf):
        def callback():
            sng = Song(name=nametf.value, parent=Songs, pis={})
            # RBs.write_json()
            Songs.write_json()
            self.guisonglist()
        return Button(text="New Song", callback=callback)

    def updatesonggrid(self):
        # self.cleanUI()
        # self.body.append(self.title)
        self.GuiMain_BtnGrid()
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
        self.GuiMain_BtnGrid()
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
        self.rasedgrid = Grid(n_rows=len(song.used_pis), n_columns=6)
        for num, rasp in enumerate(song.used_pis):
            print(str(num) + rasp)
            rname = Text(str(rasp))
            rfilename = Text(str(song.used_pis[rasp]))
            # self.rfilenameTfield = TextField(value=song.used_pis[rasp])
            dropdown = Dropdown(FM.filelist)
            if rfilename.text in FM.filelist:
                dropdown.value = rfilename.text

            # str rasp --> rasp obj
            raspname = rasp
            for ra in RBs.Rasplist:
                if ra.name == rasp:
                    rasp = ra
                    break

            rupdate = self.sng_raspUpdateBtn(
                song.used_pis, rasp.name, song, dropdown)
            # better take the saved not the dropdown
            rupload = self.rsnguploadBtn(rasp, rfilename.text)
            rdelete = self.sng_raspDeleteBtn(song, rasp.name)
            self.rasedgrid[num, 0] = rname
            self.rasedgrid[num, 1] = rfilename
            self.rasedgrid[num, 2] = dropdown  # self.rfilenameTfield
            self.rasedgrid[num, 3] = rupdate
            self.rasedgrid[num, 4] = rupload
            self.rasedgrid[num, 5] = rdelete

        dropdown = Dropdown(FM.filelist)
        newText = Text("New Rasp")
        RaspNamelist = []
        for ra in RBs.Rasplist:
            if ra.name not in song.used_pis:
                RaspNamelist.append(ra.name)
        RaspNamelist.append("  ")
        raspsdrop = Dropdown(RaspNamelist)
        # self.newrasfilename = TextField(value="Unknown File")
        filedropdown = Dropdown(FM.filelist)

        raddButton = self.appendRasptoSongBtn(song, raspsdrop, filedropdown)
        self.NewRaspCont = Container(
            newText, raspsdrop, filedropdown, raddButton)

        # print("appending EditSong UI")
        self.body.append(self.title)
        self.body.append(self.soedgrid)
        # self.body.append(self.rasedgrid)
        self.body.append(self.rasedgrid)
        self.body.append(self.NewRaspCont)
        saveBtn = self.songeditsaveBtn(song)
        self.body.append(saveBtn)

        # self.cleanUI()

    def appendRasptoSongBtn(self, song, raspsdrop, filedropdown):
        def callback():
            song.addRasp(raspsdrop.value, filedropdown.value)

            for rasp in RBs.Rasplist:
                print(f"rasps vorhanden {rasp.name}")
                if raspsdrop.value == rasp.name:
                    # print(
                    #    f"rasps richtig {rasp.name} drop value {self.raspsdrop.value}")
                    rasp.addSong(song.name, filedropdown.value)
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
        self.GuiMain_BtnGrid()
        self.raspgrid = Grid(n_rows=len(RBs.Rasplist),
                             n_columns=7)
        rasplist = RBs.Rasplist[:]
        for num, rasp in enumerate(rasplist):
            # print(f"song {song} song.name {song.name} num {num}")

            n = Text(str(num))
            t = Text(rasp.name)
            ip = Text(rasp.IP)
            redit = self.raspEditBtn(rasp)
            rdelete = self.raspDeleteBtn(rasp)
            rshutdown = self.raspshutdownBtn(rasp)
            rreboot = self.raspsrebootBtn(rasp)

            self.raspgrid[num, 0] = n
            self.raspgrid[num, 1] = t
            self.raspgrid[num, 2] = ip
            self.raspgrid[num, 3] = redit
            self.raspgrid[num, 4] = rdelete
            self.raspgrid[num, 5] = rshutdown
            self.raspgrid[num, 6] = rreboot

        self.newRaspBtn = Button(text="New Rasp", callback=self.newrasp)
        #self.songmenubtn = self.songMenuBtn()
        self.body.append(self.raspgrid)
        self.body.append(self.newRaspBtn)
        # self.body.append(self.songmenubtn)

        # prinbody(self.body)
        # self.cleanUI()
        # self.updatesonggrid()

    def editRaspMenu(self, rasp):
        self.GuiMain_BtnGrid()

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
        self.raspSonglistgrid = Grid(n_rows=len(rasp.songs), n_columns=6)
        for num, sng in enumerate(rasp.songs):
            sngname = Text(sng)
            sngfilename = Text(rasp.songs[sng])
            # self.sngFiletextfield = TextField(value=rasp.songs[sng])

            dropdown = Dropdown(FM.filelist)
            if sngfilename.text in FM.filelist:
                dropdown.value = sngfilename.text

            updateBtn = self.rsngupdateBtn(
                rasp.songs, sng, rasp, dropdown)
            uploadBtn = self.rsnguploadBtn(rasp, dropdown.value)
            deleteBtn = self.rsngdeleteBtn(rasp.songs, sng, rasp)

            self.raspSonglistgrid[num, 0] = sngname
            self.raspSonglistgrid[num, 1] = sngfilename
            self.raspSonglistgrid[num, 2] = dropdown
            self.raspSonglistgrid[num, 3] = updateBtn
            self.raspSonglistgrid[num, 4] = uploadBtn
            self.raspSonglistgrid[num, 5] = deleteBtn
            # self.raspSonglistgrid[num, 5] = deleteBtn

        # new song dropdown
        newText = Text("New Song")
        #RaspNamelist = []
        # print(f"rasp songs {Songs.Songlist}")
        # print(f"rasp songs {rasp.songs}")
        # for son in Songs.Songlist:
        #    if son.name not in rasp.songs:
        #        RaspNamelist.append(son.name)
        #RaspNamelist.append("  ")

        SongNamelist = Songs.get_DDList()
        self.rsongdrop = Dropdown(SongNamelist)

        # self.newrasfilename = TextField(value="Unknown File")

        self.raddButton = self.appendsongtoraspbtn(
            rasp)

        self.NewRSongCont = Container(
            newText, self.rsongdrop, self.raddButton)
        # SaveButton
        saveraspeditBtn = self.saveraspeditBtn(rasp)

        self.body.append(RaspMenuTitle)
        self.body.append(self.raspedgrid)
        self.body.append(trenner)
        self.body.append(self.raspSonglistgrid)
        self.body.append(self.NewRSongCont)
        self.body.append(saveraspeditBtn)

    def rsngupdateBtn(self, songs, song, rasp, dropdown):
        def callback():
            # print(f"enum des knopfes ist {enum}")
            filename = dropdown.value
            songs[song] = filename  # self.sngFiletextfield.value

            # change song in mainsonglist
            for so in Songs.Songlist:
                if song == so.name:
                    # self.sngFiletextfield.value
                    so.addRasp(rasp.name, filename)
                    break
            self.editRaspMenu(rasp)
        return Button(text="Update", callback=callback)

    def rsnguploadBtn(self, rasp, value):
        def callback():
            # print(f"enum des knopfes ist {enum}")
            filename = value

            # tell file manager to upload
            COM.upload_light(rasp, filename)

            # self.editRaspMenu(rasp)
        return Button(text="Upload", callback=callback)

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

    def raspshutdownBtn(self, rasp):

        def callback():
            COM.shutdown_rasp(rasp)

        return Button(text="Shutdown", callback=callback)

    def raspsrebootBtn(self, rasp):

        def callback():
            COM.reboot_rasp(rasp)

        return Button(text="Reboot", callback=callback)


###############################################
###############################################Playlistgui#####


    def guiPlaylists(self):
        # if len(self.body) > 1:
        #    self.body.remove(self.songgrid)
        self.GuiMain_BtnGrid()
        self.plgrid = Grid(n_rows=len(PLs.Playlistlist),
                           n_columns=5)
        playlistlist = PLs.Playlistlist[:]
        for num, pl in enumerate(playlistlist):
            # print(f"song {song} song.name {song.name} num {num}")

            n = Text(str(num))
            t = Text(pl.name)
            used_songs = Text(str(pl.used_songs))
            redit = self.plEditBtn(pl)
            rdelete = self.plDeleteBtn(pl)
            # rshutdown = self.raspshutdownBtn(rasp)
            # rreboot = self.raspsrebootBtn(rasp)

            self.plgrid[num, 0] = n
            self.plgrid[num, 1] = t
            self.plgrid[num, 2] = used_songs
            self.plgrid[num, 3] = redit
            self.plgrid[num, 4] = rdelete
            # self.plgrid[num, 5] = rshutdown
            # self.plgrid[num, 6] = rreboot
        self.nfNewpl = TextField(value='Default')
        # Button(text="New Playlist", callback=PLs.add()
        self.newPLBtn = self.newplBtn()
        self.body.append(self.plgrid)
        self.body.append(self.nfNewpl)
        self.body.append(self.newPLBtn)
        # self.body.append(self.songmenubtn)

    # Edit Playlist
    def guiEditPlaylist(self, pl):
        # self.cleanUI()
        self.GuiMain_BtnGrid()
        self.plsnggrid = Grid(n_rows=len(pl.songs),
                              n_columns=8)
        # playlistlist = PLs.Playlistlist[:]
        for num, sng in enumerate(pl.songs[:]):
            # print(f"song {song} song.name {song.name} num {num}")

            n = Text(str(num))
            t = Text(sng.name)
            delaytime = Text(text=pl.used_songs[sng.name])
            delayset = TextField(value=pl.used_songs[sng.name])
            rup = self.plsngupBtn(pl, sng)
            rdown = self.plsngdownBtn(pl, sng)
            rsngupdate = self.plsngupdateBtn(pl, sng, delayset)
            rdelete = self.plsngdeleteBtn(pl, sng)
            # rreboot = self.raspsrebootBtn(rasp)

            self.plsnggrid[num, 0] = n
            self.plsnggrid[num, 1] = t
            self.plsnggrid[num, 2] = delaytime
            self.plsnggrid[num, 3] = delayset
            self.plsnggrid[num, 4] = rup
            self.plsnggrid[num, 5] = rdown
            self.plsnggrid[num, 6] = rsngupdate
            self.plsnggrid[num, 7] = rdelete
            # self.plgrid[num, 6] = rreboot

        self.plsong = Dropdown(Songs.get_DDList())
        pausefield = TextField("0")
        self.newsngBtn = self.plsngnewBtn(pl, self.plsong, pausefield)

        self.body.append(self.plsnggrid)
        self.body.append(self.plsong)
        self.body.append(pausefield)
        self.body.append(self.newsngBtn)

    def PLMenuBtn(self):
        def callback():
            self.guiPlaylists()
        return Button(text="Playlist Manager", callback=callback)

    def plEditBtn(self, pl):
        def callback():
            self.guiEditPlaylist(pl)
        return Button(text="Edit", callback=callback)

    def newplBtn(self):
        def callback():
            # PLs.add()
            pl = Playlist(name=self.nfNewpl.value, parent=PLs)
            PLs.write_json()

            self.guiPlaylists()

        return Button(text="New Playlist", callback=callback)

    def plsngnewBtn(self, pl, songdd, pausefield):
        def callback():
            pause = pausefield.value
            pl.add_song(Songs.get_song(songdd.value), pause)
            self.guiEditPlaylist(pl)
        return Button(text="New Song", callback=callback)

    def plDeleteBtn(self, pl):
        def callback():
            pl.remove()
            self.guiPlaylists()
        return Button(text="Delete", callback=callback)

    def plsngdeleteBtn(self, pl, song):
        def callback():
            pl.remove_song(song)
            self.guiEditPlaylist(pl)
        return Button(text="Delete", callback=callback)

    def plsngupdateBtn(self, pl, sng, pausetime):
        def callback():
            ptime = pausetime.value
            pl.used_songs[sng.name] = ptime
            PLs.write_json()
            self.guiEditPlaylist(pl)
        return Button(text="Update", callback=callback)

    def plsngupBtn(self, pl, song):
        def callback():
            pl.up(song)
            self.guiEditPlaylist(pl)
        return Button(text="Up", callback=callback)

    def plsngdownBtn(self, pl, song):
        def callback():
            pl.down(song)
            self.guiEditPlaylist(pl)
        return Button(text="Down", callback=callback)


####################
# Playmode


    def playMenuBtn(self):
        def callback():
            pass
            # self.guiEditPlaylist(pl)
        return Button(text="Play Mode", callback=callback)


def main():

    Lyout1().run()


if __name__ == '__main__':
    main()
