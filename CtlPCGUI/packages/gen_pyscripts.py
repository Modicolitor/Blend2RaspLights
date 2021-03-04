import json
import os
from os import join


def write_json(self, name, text):
    data = text
    scriptfolder = "scripts"

    self.workpath = os.getcwd()
    self.scriptdirpath = join(self.workpath, scriptfolder)
    with open(name, 'w') as outfile:
        json.dump(data, outfile)


def gen_blinktScript():
    text = "from blinkt import set_clear_on_exit, set_brightness, set_pixel, show, clear, set_all
    import json
     import time
      import sys

       # Blend2BlinkTest.json

       def make_light(start_time, filename):  # getting time.ctime()
            beginnAt = time.mktime(time.strptime(start_time))
            time.sleep(max(0, beginnAt-time.time()))

            # set_clear_on_exit()
            datalist = []
            with open(filename) as json_file:
                data = json.load(json_file)
                for frame in data:
                    # json structure: list of dict(keyframeX,KeyframeY,r,g,b)
                    val = [frame["r"], frame["g"], frame["b"], frame["y"]]
                    datalist.append(val)

            period = 0.04
            t = time.time()
            for frame in datalist:
                t += period
                # print(frame["y"])

                # for px in range(8):
                #    set_pixel(px, val,val, val)
                #    show()
                ###set_all(r,g, b, brightness)
                set_all(frame[0], frame[1], frame[2], frame[3])
                #set_all(frame, frame, frame)
                show()

                time.sleep(max(0, t-time.time()))

            clear()
            show()

        if __name__ == "__main__":
            make_light(str(sys.argv[1]), str(sys.argv[2]))
        "

    write_json(self, name, text)
