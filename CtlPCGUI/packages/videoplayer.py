import random


class Videoplayer():
    def __init__(self, FM, COM, Rasps):
        self.FM = FM
        self.COM = COM
        self.ssh = None
        self.Rasps = Rasps

    def mk_connection(self, rasp):
        print(f'videoplayer connects now to {rasp.IP}')
        self.ssh = self.COM.connect_to(rasp.IP)

    def start_playmode(self):
        if self.ssh == None:
            self.mk_connection(self.get_videorasp())

        initvideo = self.get_random_loop()
        if initvideo == None:
            initvideo = self.FM.videolist[0]
        comands = ['export DISPLAY=:0']
        self.COM.send_command(comands, [self.ssh])
        comands = ['vlc ' +
                   self.FM.targetvidopath + initvideo]
        self.COM.send_command(comands, [self.ssh])

    def get_videorasp(self):
        for rasp in self.Rasps.Rasplist:
            print(rasp.name)
            if rasp.is_video_pi:
                return rasp

    def stop_playmode(self):
        comands = ['quit']
        self.COM.send_command(comands, [self.ssh])

        self.ssh = None

    def play_video(self, song):
        # self.check_ssh(self.ssh)
        # hier könnte auch playlist stehen anstatt song.used_video
        comands = ['add ' + song.used_video]
        self.COM.send_command(comands, [self.ssh])

    def get_random_loop(self):
        max = len(self.FM.loops)-1
        if max > 0:
            int = random.randint(0, max)
            return self.FM.loops[int]
        else:
            return None
