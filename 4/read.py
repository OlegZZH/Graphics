import numpy as np
from matplotlib import pyplot as plt

f = open("RabbitPoint.txt", "r")
px = np.array(f.readline().split()).astype(float)
py = np.array(f.readline().split()).astype(float)
f.close()

f = open("RabbitCur.txt", "r")
pxc = np.array(f.readline().split()).astype(float)
pyc = np.array(f.readline().split()).astype(float)
f.close()

f = open("RabbitPoint2.txt", "r")
mx = np.array(f.readline().split()).astype(float)
my = np.array(f.readline().split()).astype(float)

f = open("RabbitCur2.txt", "r")
mxc = np.array(f.readline().split()).astype(float)
myc = np.array(f.readline().split()).astype(float)
f.close()

f.close()
# px[0] = px[-1]
# py[0] = py[-1]
# mx[0] = mx[-1]
# my[0] = my[-1]

if len(px) - len(mx) > 0:
    for i in range(len(px) - len(mx)):
        mx = np.append(mx, mx[-1])
        my = np.append(my, my[-1])
elif len(px) - len(mx) < 0:
    for i in range(len(mx) - len(px)):
        px = np.append(px, px[-1])
        py = np.append(py, py[-1])

# mx+=120
# mxc*=1.2
# myc*=1.2
# mx*=1.2
# my*=1.2

if __name__ == "__main__":
    fig2, ax2 = plt.subplots()

    plt.gca().invert_yaxis()

    plt.gca().set_aspect("equal")
    curvaM = ax2.plot(mxc, myc, linewidth=5, color="tab:orange")

    curvaP = ax2.plot(pxc, pyc, linewidth=5, color="tab:orange")

    plt.show()
