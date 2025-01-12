from main import *


def pr1(x, y, P_matrix):
    temp = [[x[i], y[i], 1] for i in range(len(x))]
    res = np.array(temp)

    mulx = []
    muly = []
    for i in res:
        mulx.append(np.nan_to_num((i[0] * P_matrix[0, 0] + i[1] * P_matrix[1, 0] + P_matrix[2, 0]) / (
                i[0] * P_matrix[0, 2] + i[1] * P_matrix[1, 2] + P_matrix[2, 2])))
        muly.append(np.nan_to_num((i[0] * P_matrix[0, 1] + i[1] * P_matrix[1, 1] + P_matrix[2, 1]) / (
                i[0] * P_matrix[0, 2] + i[1] * P_matrix[1, 2] + P_matrix[2, 2])))
    # print(P_matrix)

    return mulx, muly


def pro_start(x11=80, x12=5, wx=1, x21=9, x22=80, wy=1, x31=0, x32=0, wo=10, obj=None):

    obj += 10

    P_matrix = np.array([[x11 * wx, x12 * wx, wx],
                         [x21 * wy, x22 * wy, wy],
                         [x31 * wo, x32 * wo, wo]])

    transform_obj = [pr1(*i, P_matrix) for i in obj]

    h = np.linspace(0, 20, 2)
    hx = np.array([])
    hy = np.array([])

    for i in range(20):
        hx = np.append(hx, h)
    for i in range(0, 200, 1):
        hy = np.append(hy, [i, i])

    transform_line = [[pr1((hx[i], hx[i + 1]), (hy[i], hy[i + 1]), P_matrix),
                       pr1((hy[i], hy[i + 1]), (hx[i], hx[i + 1]), P_matrix)] for i in
                      range(0, 40, 2)]

    return transform_obj, transform_line


if __name__ == "__main__":
    pro_start()
    plt.show()
