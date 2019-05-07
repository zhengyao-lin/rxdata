import os

import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D

from config import *

# tags = ["10cm", "20cm", "30cm", "40cm", "50cm", "60cm", "70cm"]
tags = [str(d) + "cm" for d in range(10, 161, 5)]

def read_data(path):
    ch37 = []
    ch38 = []
    ch39 = []

    with open(path) as f:
        for line in f.readlines():
            if line:
                x, y, z = line.strip().split()

                ch37.append(int(x))
                ch38.append(int(y))
                ch39.append(int(z))

    return ch37, ch38, ch39

def show_data(dataset):
    fig = plot.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.set_xlim(-70, 0)
    ax.set_ylim(-70, 0)
    ax.set_zlim(-70, 0)

    for tag in dataset:
        ax.scatter(dataset[tag][37], dataset[tag][38], dataset[tag][39],
                   label=tag)

    ax.legend()

    plot.show()

print(os.listdir(DATA_DIR))

dataset = {}

for file_name in os.listdir(DATA_DIR):
    for tag in tags:
        if file_name.startswith(tag):
            ch37, ch38, ch39 = read_data(os.path.join(DATA_DIR, file_name))

            if tag not in dataset:
                dataset[tag] = { 37: [], 38: [], 39: [] }

            dataset[tag][37] += ch37
            dataset[tag][38] += ch38
            dataset[tag][39] += ch39

            break

print(dataset)

show_data(dataset)
