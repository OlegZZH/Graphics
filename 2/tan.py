from matplotlib import pyplot as plt
from matplotlib.patches import *
from numpy import cos, sin, tan

from main import start_main


def start_tnn(point=2.5, a=1, n=2 / 5):
    if point == 0:
        point = 1e-5
    ydx = (a * n * sin(point) * cos(n * point) + a * cos(point) * sin(n * point)) / (
            a * n * cos(point) * cos(n * point) - a * sin(point) * sin(n * point))
    x0 =  a * np.cos(point) * np.sin(n * point)
    y0 =  a * np.sin(point) * np.sin(n * point)
    x = np.array([-1000, 1000])
    y = ydx * (x - x0) + y0
    yn = (-1 / ydx) * (x - x0) + y0

    return x, y, yn


if __name__ == "__main__":
    xt, yt = start_main()
    x, y, yn = start_tnn()
    fig, ax = plt.subplots()
    ax.plot(xt, yt, color="#607cff", linewidth=3)
    ax.plot(x, y, color="#FFE74A")
    ax.plot(x, yn, color="#FFA74A")
    ax.grid(color="#1A83A6")
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_facecolor("#2A2A2A")
    plt.gca().set_aspect("equal")
    plt.show()
