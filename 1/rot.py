import numpy as np
from matplotlib import pyplot as plt

from multiply_matrix import multiply


def rot_start(xr=0, yr=0, angle=30, obj=None):
    R_point = [xr, yr]
    R_angle = angle

    T_matrix = np.array([[np.cos(np.radians(R_angle)), np.sin(np.radians(R_angle)), 0],
                         [-(np.sin(np.radians(R_angle))), np.cos(np.radians(R_angle)), 0],
                         [(-(R_point[0] * (np.cos(np.radians(R_angle)) - 1)) + R_point[1] * (
                             np.sin(np.radians(R_angle)))),
                          (-(R_point[1] * (np.cos(np.radians(R_angle)) - 1)) - R_point[0] * (
                              np.sin(np.radians(R_angle)))),
                          1]])

    transform_obj = [multiply(*i, T_matrix) for i in obj]

    return transform_obj


if __name__ == "__main__":
    rot_start()
    plt.show()
