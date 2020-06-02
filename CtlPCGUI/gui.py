from browsergui import GUI, Text, Button, List, Grid
import time
import threading

texta = Text("BamBAm")
textb = Text("dig")
# GUI(Text("Hello world!"), texta).run()

list = List(items=[texta, textb])


button = Button('0')


@button.def_callback
def increment():
    button.text = str(int(button.text)+1)


now = Text("")


def update_now_forever():
    while True:
        now.text = time.strftime("%Y-%m-%d %H:%M:%S")
        time.sleep(1)


t = threading.Thread(target=update_now_forever)
t.daemon = True
t.start()


# GUI(button, texta, Text("\n The time is: ",), now, list, title='Marshall AR.TS Live Suit').run()

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
    Lyout1().run()


if __name__ == '__main__':
    main()
