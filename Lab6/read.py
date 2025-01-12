import numpy as np
from matplotlib import pyplot as plt

f = open("FishCur.txt", "r")
pxc = np.array(f.readline().split()).astype(float)
pyc = np.array(f.readline().split()).astype(float)
f.close()

mx = max(pxc)
my = max(pyc)
pxc /= mx*2
pyc /= my*2


pxc = pxc[::2]
pyc = pyc[::2]
if __name__ == "__main__":
    fig2, ax2 = plt.subplots()

    plt.gca().set_aspect("equal")
    curvaP = ax2.plot(pxc, pyc, linewidth=5, color="tab:orange")
    plt.show()
