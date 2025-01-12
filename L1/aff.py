from main import *
from multiply_matrix import multiply


def aff_start(x111=1, x121=0, x131=0, x211=0, x221=1, x231=0, x311=0, x321=0, x331=1, obj=None):
    T_matrix = np.array([[x111, x121, x131],
                         [x211, x221, x231],
                         [x311, x321, x331]])

    transform_obj = [multiply(*i, T_matrix) for i in obj]

    h = np.linspace(-10, 10, 2)
    hx = np.array([])
    hy = np.array([])
    for i in range(20):
        hx = np.append(hx, h)
    for i in range(-10, 10, 1):
        hy = np.append(hy, [i, i])

    transform_line = [[multiply((hx[i], hx[i + 1]), (hy[i], hy[i + 1]), T_matrix),
                       multiply((hy[i], hy[i + 1]), (hx[i], hx[i + 1]), T_matrix)] for i in
                      range(0, 40, 2)]

    return transform_obj, transform_line


if __name__ == "__main__":
    aff_start()
    plt.show()
