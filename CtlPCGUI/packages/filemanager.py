import paramiko
import os
import sys
from os import listdir
from os.path import isfile, join, isdir


class Filemanager:
    def __init__(self):
        self.settings = ""  # must be written
        self.appdatafoldername = "appdata"
        self.songfoldername = "usersongs"
        self.scriptfoldername = "userscripts"
        self.videofoldername = "uservideo"
        self.songdirpath = ""  # will be set in the next step
        self.targetvidopath = "/home/pi/uservideo/"
        scriptdirpath = ""
        #self.videodirpath = "uservideo"
        self.filelist = self.load_filelist()
        self.scriptlist = self.load_scriptlist()
        self.videolist = self.load_videolist()
        self.loops = self.load_looplist()

    def load_filelist(self):
        # path = os.path()
        self.filelist = []
        self.workpath = os.getcwd()
        self.songdirpath = join(self.workpath, self.songfoldername)

        # sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
        # print(self.songdirpath)
        # print(path)
        # print(glob.glob("/userfiles/*.json"))

        if not isdir(self.songdirpath):
            self.genfolder(self.songdirpath)

        self.filelist = [f for f in listdir(
            self.songdirpath) if isfile(join(self.songdirpath, f))]

        self.filelist.insert(0, " ")
        print(self.filelist)
        return self.filelist

    def genfolder(self, path):
        os.mkdir(path)

    def path_from_filename(self, name):
        return join(self.songdirpath, name)

    def load_settings(self):
        pass

    def load_scriptlist(self):

        self.scriptlist = []
        self.workpath = os.getcwd()
        self.scriptdirpath = join(self.workpath, self.scriptfoldername)

        if not isdir(self.scriptdirpath):
            self.genfolder(self.scriptdirpath)

        self.scriptlist = [f for f in listdir(
            self.scriptdirpath) if isfile(join(self.scriptdirpath, f))]

        self.scriptlist.insert(0, " ")
        print(self.scriptlist)
        return self.scriptlist

    def load_videolist(self):

        self.videolist = []
        self.workpath = os.getcwd()
        self.videodirpath = join(self.workpath, self.videofoldername)

        if not isdir(self.videodirpath):
            self.genfolder(self.videodirpath)

        self.videolist = [f for f in listdir(
            self.videodirpath) if isfile(join(self.videodirpath, f))]  # and not 'loop' in f

        self.videolist.insert(0, " ")
        print(self.videolist)
        return self.videolist

    def load_looplist(self):
        self.looplist = []
        self.workpath = os.getcwd()
        self.videodirpath = join(self.workpath, self.videofoldername)

        if not isdir(self.videodirpath):
            self.genfolder(self.videodirpath)

        self.looplist = [f for f in listdir(
            self.videodirpath) if isfile(join(self.videodirpath, f)) and 'loop' in f]

        #self.looplist.insert(0, " ")
        print(self.looplist)
        return self.looplist


class Communicator(Filemanager):
    def __init__(self, parent):
        self.parent = parent
        pass

    def get_delaytime(self):
        import time

        standarddelay = 5  # seconds

        currentimestr = time.ctime()
        print(currentimestr)
        seconds = int(currentimestr[17]+currentimestr[18])
        futuresec = (seconds + standarddelay) if (seconds +
                                                  standarddelay) < 60 else (seconds + standarddelay) - 60
        futuresec = "0" + str(futuresec) if len(str(futuresec)
                                                ) == 1 else str(futuresec)
        starttime = currentimestr[:17] + \
            str(futuresec) + currentimestr[19:]
        print(starttime)
        return starttime

    # takes used_pis list

    def play_song(self, song):

        filename = "Multicolortest1.json"
        ips = []
        cons = []
        comands = []

        pythonfilename = "json2blinkt-time_MultiColor.py"
        # ips.append(r.IP)

        # ips = ["10.0.1.24"]  # , "10.0.1.25"

        rasps = song.get_slaves()

        for rasp in rasps:
            con = self.connect_to(rasp.IP)
            cons.append(con)

            comand = "python " + pythonfilename + ' "' + \
                self.get_delaytime() + '"' + ' "' + self.get_filename(rasp, song) + '"'
            print(comand)
            comands.append(comand)

        self.send_command(comands, cons)

    def command_from_type(self, type):
        if type == "shutdown":
            return "sudo shutdown now"  # command
        elif type == "reboot":
            return "sudo reboot now"

    def get_filename(self, rasp, song):
        file = rasp.songs[song.name]
        return file[0]  # = filename

    def connect_to(self, ip):
        print(f"ip {ip} in connect to")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(ip,  username="pi",
                    password="B!um3nBo+")
        print(f"ssh started")
        return ssh

    def send_command(self, comands, sshs):
        # send one command per ssh, by equal position in List
        import threading

        def exe(ssh, comand):
            # comand
            print(f"comand bevor sending '{comand}'")
            ssh_stdin, ssh_stouz, ssh_stderr = ssh.exec_command(comand)
            # "python json2blinkt-time.py"
            print(ssh_stouz)
            print(ssh_stdin)
            print(ssh_stderr)
            print("bambam lights on")
            # ssh.close()

        threads = set()
        # for cnum, comand in enumerate(comands):
        for num, ssh in enumerate(sshs):
            threads.add(threading.Thread(
                target=exe, args=[ssh, comands[num]]))

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    def shutdown_rasp(self, rasp):
        con = self.connect_to(rasp.IP)
        self.send_command([self.command_from_type("shutdown")], [con])

    def reboot_rasp(self, rasp):
        con = self.connect_to(rasp.IP)
        self.send_command([self.command_from_type("reboot")], [con])

    def upload_light(self, rasp, filename):
        homepath = join(self.parent.songdirpath, filename)
        remote_homefolder = "/home/pi/"
        remotepath = join(remote_homefolder, filename)
        self.upload(rasp, homepath, remote_homefolder, remotepath)

    def upload_script(self, rasp, scriptname):
        homepath = join(self.parent.scriptdirpath, scriptname)
        remotepath = join("/home/pi/", scriptname)
        self.upload(rasp, homepath, remotepath)

    def upload_video(self, rasp, videoname):
        homepath = join(self.parent.videodirpath, videoname)
        remote_folders = self.parent.targetvidopath
        remotepath = join(remote_folders, videoname)
        self.upload(rasp, homepath, remote_folders, remotepath)

    def upload(self, rasp, homepath, remote_folders, remotepath):
        ssh = self.connect_to(rasp.IP)
        ftp_client = ssh.open_sftp()
        self.send_command([f'mkdir -p {remote_folders}'], [ssh])
        print('mkdir done')
        ftp_client.put(homepath, remotepath)  # get is downloading
        print('upload done')
        ftp_client.close()
        print('ftp client closed')

        #self.send_command(comands, sshs)
