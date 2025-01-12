import matplotlib.pyplot as plt
from matplotlib.patches import *

from rot import rot_start

main_color = '#01F0A8'
axis_color = "#5B6A75"
face_color = '#2F323A'
tick_color = "#F7ACCF"


def grid(fig, ax):
    h = np.linspace(-20, 20, 2)
    hx = np.array([])
    hy = np.array([])

    for i in range(40):
        hx = np.append(hx, h)
    for i in range(-20, 20, 1):
        hy = np.append(hy, [i, i])
    for i in range(0, 80, 2):
        if i == 40:
            ax.plot((hx[i], hx[i + 1]), (hy[i], hy[i + 1]), linewidth=2.5, color=axis_color)
            ax.plot((hy[i], hy[i + 1]), (hx[i], hx[i + 1]), linewidth=2.5, color=axis_color)
        else:
            ax.plot((hx[i], hx[i + 1]), (hy[i], hy[i + 1]), linewidth=0.5, color=axis_color)
            ax.plot((hy[i], hy[i + 1]), (hx[i], hx[i + 1]), linewidth=0.5, color=axis_color)

    fig.patch.set_facecolor(face_color)
    ax.set_facecolor(face_color)
    ax.tick_params(axis="x", colors=tick_color)
    ax.tick_params(axis="y", colors=tick_color)
    ax.spines['bottom'].set_color('w')
    ax.spines['top'].set_color('w')
    ax.spines['right'].set_color('w')
    ax.spines['left'].set_color('w')
    plt.gca().set_aspect("equal")


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])  # Typo was here

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


def cent(xlt1, ylt1, xlt2, ylt2):
    return line_intersection(((xlt1[0], ylt1[0]), (xlt1[1], ylt1[1])), ((xlt2[0], ylt2[0]), (xlt2[1], ylt2[1])))


def start_main(R1=1, R2=2, R3=5, R4=3, S1=2):
    pi = np.pi

    theta = np.linspace(pi, 2 * pi)
    half_theta = np.linspace(pi, pi * 1.3)
    half_theta2 = np.linspace(pi * 1.5, pi * 1.2)
    half_theta3 = np.linspace(pi, pi * 0.7)
    half_theta4 = np.linspace(2 * pi, pi)

    x1 = R1 * np.cos(theta)
    y1 = R1 * np.sin(theta)

    x2 = R2 * np.cos(half_theta)
    y2 = R2 * np.sin(half_theta)

    x3 = np.array([x2[-1], x2[-1]])
    y3 = np.array([y2[-1], y2[-1] - R3])

    x4 = R3 * np.cos(half_theta2) + x2[-1]
    y4 = R3 * np.sin(half_theta2) + y2[-1]

    x5 = np.array([x4[-1], x4[-1]])
    y5 = np.array([y4[-1], y4[-1] + 8])

    x6 = R4 * np.cos(half_theta3)
    x6 = x6 + (x5[-1] - x6[0])
    y6 = R4 * np.sin(half_theta3) + y5[-1]

    R5 = x6[-1]

    x7 = R5 * np.cos(theta)
    y7 = -R5 * np.sin(theta)+y6[-1]

    center = (-2.5, -5)

    x8 = center[0] + np.array([0, np.cos(np.pi / 3), np.cos(2 * np.pi / 3), 0]) * S1
    y8 = center[1] + np.array([0, np.sin(np.pi / 3), np.sin(2 * np.pi / 3), 0]) * S1

    x8,y8=rot_start(*center,25,[[x8,y8]])[0]

    x9=np.array([x1[0],x2[0]])
    y9=np.array([y1[0],y2[0]])

    obj = np.array(
        [[x1, y1], [x2, y2], [x3, y3], [x4, y4], [x5, y5], [x6, y6], [x7, y7], [x8, y8],[x9, y9], [-x2, y2], [-x3, y3], [-x4, y4], [-x5, y5], [-x6, y6],[-x8, y8],[-x9, y9]],
        dtype=object)

    return obj


if __name__ == "__main__":
    fig, ax = plt.subplots()
    grid(fig, ax)
    for i in start_main():
        ax.plot(*i, linewidth=3, color=main_color)
    # ax.set(xlim=(-10, 10), ylim=(-10, 10))

    plt.show()
