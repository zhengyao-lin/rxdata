import sys
import time
import json
from config import *

import matplotlib.pyplot as plot

from mpl_toolkits.mplot3d import Axes3D

class Record:
    def __init__(self, counter, ch, mac, rssi, tx_power):
        self.counter = counter
        self.ch = ch
        self.mac = mac
        self.rssi = rssi
        self.tx_power = tx_power

    @staticmethod
    def from_json(dat):
        return Record(**dat)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "@{}: counter {}, mac {}, rssi {}, tx_power {}" \
               .format(self.ch, self.counter, self.mac, self.rssi, self.tx_power)

def channel_draw(ch, color):
    last_rec = None
    last_counter = None

    begin = time.time()

    label_added = False

    def draw(rec):
        nonlocal last_rec, last_counter, label_added

        counter = rec.counter

        if last_rec:
            plot.xlim(counter - 20, counter + 10)
            plot.plot([last_counter, counter],
                      [last_rec.rssi - last_rec.tx_power, rec.rssi - rec.tx_power], c=color)
        
        plot.scatter(counter, rec.rssi - rec.tx_power, marker=".", c=color, **{ "label": str(ch) if not label_added else None })

        if not label_added:
            plot.legend(loc="best")
            label_added = True

        last_rec = rec
        last_counter = counter

    def last():
        return last_rec

    return draw, last

tag = sys.argv[1]
data_file = "{}/{}-{}.txt".format(DATA_DIR, tag, int(time.time()))

print("collecting data for tag {}".format(tag))
print("storing to {}".format(data_file))

with open(SERIAL_FILE) as f:
    with open(data_file, "w") as data:
        ch_draw = {
            37: channel_draw(37, "red"),
            38: channel_draw(38, "blue"),
            39: channel_draw(39, "green")
        }

        fig = plot.figure()
        ax = fig.add_subplot(122, projection="3d")
        ax.set_xlim(-70, 0)
        ax.set_ylim(-70, 0)
        ax.set_zlim(-70, 0)

        data_buf = {
            37: [],
            38: [],
            39: []
        }

        try:
            while True:
                line = f.readline().strip()

                try:
                    if line:
                        rec = Record.from_json(json.loads(line))
                        print(rec)

                        data_buf[rec.ch].append(rec.rssi)

                        while len(data_buf[37]) and len(data_buf[38]) and len(data_buf[39]):
                            data.write("{} {} {}\n".format(data_buf[37].pop(0),
                                                           data_buf[38].pop(0),
                                                           data_buf[39].pop(0)))

                            data.flush()

                except KeyboardInterrupt: break

                except Exception as e:
                    print(repr(e))
        
        except KeyboardInterrupt:
            print("exiting")

"""
draw, _ = ch_draw[rec.ch]

data_buf[rec.ch].append(rec)

plot.subplot(1, 2, 1)
plot.ylim(-100, 10)
draw(rec)

ch37 = ch_draw[37][1]()
ch38 = ch_draw[38][1]()
ch39 = ch_draw[39][1]()

if ch37 and ch38 and ch39:
    # plot.subplot(1, 2, 2)
    # plot.xlim(-50, 10)
    # plot.ylim(-50, 10)
    ax.scatter(ch37.rssi, ch38.rssi, ch39.rssi, marker=".")

plot.pause(0.00001)
"""
