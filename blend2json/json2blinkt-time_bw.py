from blinkt import set_clear_on_exit, set_brightness, set_pixel, show, clear, set_all
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
            val = frame["y"] * 255
            datalist.append(val)

    period = 0.04
    t = time.time()
    for frame in datalist:
        t += period
        # print(frame["y"])

        # for px in range(8):
        #    set_pixel(px, val,val, val)
        #    show()
        set_all(frame, frame, frame)
        show()

        time.sleep(max(0, t-time.time()))

    clear()
    show()


if __name__ == "__main__":
    make_light(str(sys.argv[1]), str(sys.argv[2]))
