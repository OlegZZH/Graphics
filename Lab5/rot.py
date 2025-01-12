import numpy as np
from matplotlib import pyplot as plt
from numpy import cos, sin


def rot_start(points, alfa, beta, gamma):

    a = np.deg2rad(alfa)
    b = np.deg2rad(beta)
    g = np.deg2rad(gamma)
    x_matrix = np.array([[1, 0, 0, 0],
                         [0, cos(a), sin(a), 0],
                         [0, -sin(a), cos(a), 0],
                         [0, 0, 0, 1]])
    y_matrix = np.array([[cos(b), 0, -sin(b), 0],
                         [0, 1, 0, 0],
                         [sin(b), 0, cos(b), 0],
                         [0, 0, 0, 1]])
    z_matrix = np.array([[cos(g), sin(g), 0, 0],
                         [-sin(g), cos(g), 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])

    T_matrix = x_matrix.dot(y_matrix)
    T_matrix = T_matrix.dot(z_matrix)

    temp = np.c_[points, np.ones(len(points))]
    mul = np.array([i.dot(T_matrix) for i in temp])
    mul = mul[:, :3]

    return mul


if __name__ == "__main__":
    rot_start(np.array([[0., 0., 0.],
                        [1., 0., 0.],
                        [1., 1., 0.],
                        [0., 1., 0.],
                        [0., 0., 1.],
                        [1., 0., 1.],
                        [1., 1., 1.],
                        [0., 1., 1.]]), 0, 0, 0)
    plt.show()
