import numpy as np
from matplotlib import pyplot as plt


def start_main(a=1, n=2 / 5, N=5):
    t = np.arange(0, N, 0.05)

    x = a * np.cos(t) * np.sin(n * t)
    y = a * np.sin(t) * np.sin(n * t)
    return x, y


if __name__ == "__main__":
    fig, ax = plt.subplots()
    ax.plot(*start_main())
    plt.gca().set_aspect("equal")

    plt.grid()
    plt.show()
