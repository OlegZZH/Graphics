import numpy as np
from matplotlib import pyplot as plt


def start_main(a=4):
    t = np.arange(-5, 5, 0.05)
    x = a * s
    y = a * t * (t ** 2 - 3) / (t ** 2 + 1)
    return x, y


if __name__ == "__main__":
    fig, ax = plt.subplots()
    ax.plot(*start_main())
    plt.gca().set_aspect("equal")

    plt.grid()
    plt.show()
