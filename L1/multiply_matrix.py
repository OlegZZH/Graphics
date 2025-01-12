import numpy as np


def multiply(x, y, T_matrix):
    temp = np.c_[x, y, np.ones(len(x))]
    mul = temp @ T_matrix
    return mul[:, 0], mul[:, 1]
