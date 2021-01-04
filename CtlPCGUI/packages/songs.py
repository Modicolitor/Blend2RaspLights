import json
import time
import threading
from pathlib import Path
# from gui import Lyout1


class Songs():
    def __init__(self):
        self.Songlist = []

    def add(self, song):
        self.Songlist.append(song)

    def write_json(self):
        data = {}
        data['songs'] = []

        for d in self.Songlist:

            data['songs'].append({
                'name': d.name,
                'used_pis': d.used_pis,
                'description': d.description
            })

        with open('user_songs.json', 'w') as outfile:
            json.dump(data, outfile)

    def read_json(self):
        my_file = Path("user_songs.json")
        if my_file.is_file():
            with open('user_songs.json') as json_file:
                data = json.load(json_file)
                for p in data['songs']:
                    # print(f"generating {p.name}")
                    sng = Song(name=p['name'], parent=self, pis={})
                    sng.used_pis = p['used_pis']
                    sng.decription = p['description']


class Song(Songs):
    def __init__(self, name, parent, pis):
        self.name = name
        self.used_pis = pis  # raspname, filename
        self.description = ""
        self.parent = parent

        self.parent.add(self)

    def ping(self):
        print("ping")

    # def append_pi(self, song):
    #    self.used_pis.append(song)

    def remove(self):
        self.parent.Songlist.remove(self)
        self.parent.write_json()

    def addRasp(self, Rasp, filename):
        self.used_pis[Rasp] = filename
        self.parent.write_json()

    def removeRasp(self, Rasp):
        self.used_pis.pop(Rasp)
        self.parent.write_json()

    def playRasps(self):
        import paramiko

        sshs = []
        ips = ["10.0.1.20", "10.0.1.20"]
        for ip in ips:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())

            # ssh.load_host_keys()

            # print(key)

            ssh.connect(ip,  username="pi",
                        password="B!um3nBo+")  # password error
            sshs.append(ssh)
        # ssh.start_client()

        # ssh_stdin, ssh_stouz, ssh_stderr = ssh.exec_command('cd /BLEND2BLINK/')
        # "ls -l")  # cd /BLEND2BLINK/")
        for ssh in sshs:
            ssh_stdin, ssh_stouz, ssh_stderr = ssh.exec_command(
                'python json2blinkt-time.py')
            print("bambam lights on")
            ssh.close()

    def playVideo(self):
        import cv2  # opencv

        cap = cv2.VideoCapture("testmovie.mp4")
        ret, frame = cap.read()
        while(1):
            ret, frame = cap.read()
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q') or ret == False:
                cap.release()
                cv2.destroyAllWindows()
                break
            cv2.imshow('frame', frame)
        #import vlc
        #player = vlc.MediaPlayer("testmovie.mp4")
        # player.play()

    def edit(self):
        print("editieren")
        return self
