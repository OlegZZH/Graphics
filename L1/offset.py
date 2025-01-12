from main import *
from multiply_matrix import multiply


def off_start(dx=2, dy=2, obj=None):
    T_matrix = np.array([[1, 0, 0],
                         [0, 1, 0],
                         [dx, dy, 1]])

    transform_obj = [multiply(*i, T_matrix) for i in obj]

    return transform_obj


if __name__ == "__main__":
    off_start()
    plt.show()
