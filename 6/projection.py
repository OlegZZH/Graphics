from math import cos, sin

import numpy as np


def pr1(points, P_matrix):
    temp = np.c_[points, np.ones(len(points))]

    mulx = []
    muly = []
    mulz = []
    for i in temp:
        mulx.append(
            np.nan_to_num((i[0] * P_matrix[0, 0] + i[1] * P_matrix[1, 0] + i[2] * P_matrix[2, 0] + P_matrix[3, 0]) / (
                    i[0] * P_matrix[0, 3] + i[1] * P_matrix[1, 3] + i[2] * P_matrix[2, 3] + P_matrix[3, 3])))
        muly.append(
            np.nan_to_num((i[0] * P_matrix[0, 1] + i[1] * P_matrix[1, 1] + i[2] * P_matrix[2, 1] + P_matrix[3, 1]) / (
                    i[0] * P_matrix[0, 3] + i[1] * P_matrix[1, 3] + i[2] * P_matrix[2, 3] + P_matrix[3, 3])))
        mulz.append(
            np.nan_to_num((i[0] * P_matrix[0, 2] + i[1] * P_matrix[1, 2] + i[2] * P_matrix[2, 2] + P_matrix[3, 2]) / (
                    i[0] * P_matrix[0, 3] + i[1] * P_matrix[1, 3] + i[2] * P_matrix[2, 3] + P_matrix[3, 3])))

    return mulx, muly, mulz
def projection_start(points,alfa):
    a = np.deg2rad(alfa)
    b = np.deg2rad(60)
    T_matrix = np.array([[cos(b),sin(a)*cos(b),-cos(a)*sin(b),0],
                         [0, cos(a),sin(a), 0],
                         [sin(b), -sin(a)*cos(b), cos(a)*cos(b),  0],
                         [0, 0, 0, 1]])

    temp = np.c_[points, np.ones(len(points))]
    mul = np.array([i.dot(T_matrix) for i in temp])
    mul = mul[:, :3]

    return mul[:,0],mul[:,1],mul[:,2]


if __name__ == "__main__":
    projection_start(np.array([[0., 0., 0.],
                               [1., 0., 0.],
                               [1., 1., 0.],
                               [0., 1., 0.],
                               [0., 0., 1.],
                               [1., 0., 1.],
                               [1., 1., 1.],
                               [0., 1., 1.]]))
