import paramiko
import os
import sys
from os import listdir
from os.path import isfile, join, isdir


class Filemanager:
    def __init__(self):
        self.songfoldername = "usersongs"
        self.songdirpath = ""  # will be set in the next step
        self.filelist = self.load_filelist()

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
        return rasp.songs[song.name]  # = filename

    def connect_to(self, ip):
        print(f"ip {ip} in connect to")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(ip,  username="pi",
                    password="B!um3nBo+")
        print(f"sshdone")
        return ssh

    def send_command(self, comands, sshs):
        import threading

        def exe(ssh, comand):
            # comand
            print(f"comand bevor sending '{comand}'")
            ssh_stdin, ssh_stouz, ssh_stderr = ssh.exec_command(comand)
            # "python json2blinkt-time.py"

            print("bambam lights on")
            ssh.close()

        threads = set()
        for num, ssh in enumerate(sshs):
            threads.add(threading.Thread(target=exe, args=[ssh, comands[num]]))

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

        path = join(self.parent.songdirpath, filename)
        # + self.parent.songfoldername
        remotefilepath = join("/home/pi/", filename)

        ssh = self.connect_to(rasp.IP)
        print(f"path {path} remote {remotefilepath}")
        ftp_client = ssh.open_sftp()
        ftp_client.put(path, remotefilepath)  # get is downloading
        ftp_client.close()

        #self.send_command(comands, sshs)
