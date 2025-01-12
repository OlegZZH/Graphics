import numpy as np


def projection_start(points,a,b):
    a/=10
    b/=10

    T_matrix = np.array([[1,0, 0, 0],
                         [0, 1, 0, 0],
                         [a, b, 0, 1],
                         [0, 0, 0, 1]])

    temp = np.c_[points, np.ones(len(points))]
    mul = np.array([i.dot(T_matrix) for i in temp])
    mul = mul[:, :3]
    return mul


if __name__ == "__main__":
    projection_start(np.array([[0., 0., 0.],
                               [1., 0., 0.],
                               [1., 1., 0.],
                               [0., 1., 0.],
                               [0., 0., 1.],
                               [1., 0., 1.],
                               [1., 1., 1.],
                               [0., 1., 1.]]))
