import multiprocessing
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from qt_material import apply_stylesheet

from multiply_matrix import multiply
from read import *

face_color = "#1E212B"
curva_color = "#4D8B31"
tick_color = '#FFC800'
line_color = "#FF8427"

ofsx = np.array([np.linspace(px[i], mx[i], 50) for i in range(len(px))])

ofsy = np.array([np.linspace(py[i], my[i], 50) for i in range(len(py))])

t = np.linspace(0, 1, 20)
f = 0.4# 0 < f <0.5
wa = 1
wb = f/(1-f)
wc = 1


def col(ax):
    ax.set_facecolor(face_color)
    ax.tick_params(labelcolor=tick_color)

    return ax


def curva2(points):
    a, b, c = points
    r = np.array(
        [(a * wa * (1 - u) ** 2 + 2 * b * wb * u * (1 - u) + c * wc * u ** 2) / (
                wa * (1 - u) ** 2 + 2 * wb * u * (1 - u) + wc * u * u) for u in t])

    return r


def cal_curva(x, y):
    c = np.empty((1, 2, 20))
    if len(x) >= 3:
        k = len(x[2::2])
        points = np.array([[[x[d], y[d]], [x[d + 1], y[d + 1]], [x[d + 2], y[d + 2]]] for d in
                           range(0, 2 * k, 2)])
        Cur = pool.map(curva2, points)
        c = np.array([[Cur[d][:, 0], Cur[d][:, 1]] for d in range(k)])
    return c


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('untitled.ui', self)
        self.pxc, self.pyc, self.px, self.py = pxc, pyc, px, py
        self.button_off = self.findChild(QtWidgets.QPushButton, 'pushButton_6')
        self.button_rot = self.findChild(QtWidgets.QPushButton, 'pushButton_7')
        self.button_cla = self.findChild(QtWidgets.QPushButton, 'pushButton_2')
        self.button_Anim = self.findChild(QtWidgets.QPushButton, 'pushButton')

        self.spinBox_dx = self.findChild(QtWidgets.QSpinBox, 'spinBox_3')
        self.spinBox_dy = self.findChild(QtWidgets.QSpinBox, 'spinBox_4')
        self.spinBox_X = self.findChild(QtWidgets.QSpinBox, 'spinBox')
        self.spinBox_Y = self.findChild(QtWidgets.QSpinBox, 'spinBox_2')
        self.angle = self.findChild(QtWidgets.QSpinBox, 'spinBox_5')

        self.horizontalLayout = self.findChild(QtWidgets.QHBoxLayout, 'horizontalLayout_2')
        self.fig = Figure(figsize=(10, 10))
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot()
        self.fig.patch.set_facecolor(face_color)
        self.ax.set_aspect(1. / self.ax.get_data_ratio())
        self.ax = col(self.ax)
        self.ax.grid()

        self.curva = self.ax.plot(self.pxc, -self.pyc, linewidth=5, color=curva_color)[0]
        self.line = self.ax.plot(self.px, -self.py, linewidth=1, color=line_color)[0]
        self.point = self.ax.plot(self.px, - self.py, 'o', picker=True, pickradius=5, color=tick_color)[0]
        self.press = None
        self.connect()
        self.button_Anim.clicked.connect(self._anim)
        self.button_cla.clicked.connect(self._clear)
        self.button_rot.clicked.connect(self._rot)
        self.button_off.clicked.connect(self._off)

        self.horizontalLayout.addWidget(self.canvas)
        self.fc = 0  # frame_count

    def connect(self):
        print("connect")
        self.cidpik = self.canvas.mpl_connect('pick_event', self.onpick)
        self.cid = self.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidmotion = self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.cidrelease = self.canvas.mpl_connect('button_release_event', self.on_release)

    def on_press(self, event):
        print("on_press")
        if event.button == 1:
            x = np.array(self.point.get_data()[0])
            x = np.append(x, event.xdata)
            y = np.array(self.point.get_data()[1])
            y = np.append(y, event.ydata)

            c = cal_curva(x, y)
            self.point.set_data(x, y)
            self.line.set_data(x, y)

            self.curva.set_data(c[:, 0], c[:, 1])

        if event.button == 3:
            """Check whether mouse is over us; if so, store some data."""

            if event.inaxes != self.point.axes:
                return
            contains, attrd = self.point.contains(event)
            if not contains:
                return
            self.press = self.point.get_data()

    def onpick(self, event):

        ind = event.ind
        print('onpick points:', ind)

        self.i = ind[0]

    def on_motion(self, event):
        if self.press is None or event.inaxes != self.point.axes:
            return

        x0, y0 = self.press
        x0[self.i] = event.xdata
        y0[self.i] = event.ydata
        self.point.set_data(x0, y0)
        self.line.set_data(x0, y0)
        c = cal_curva(x0, y0)

        self.curva.set_data(c[:, 0], c[:, 1])
        self.canvas.draw()

    def on_release(self, event):
        self.press = None

        self.canvas.draw()

    def anim_decorator(func):
        def wrraper(self):

            self.l, a = func(self)

            self.ax.set_xlim(min(self.point.get_xdata()) - 50, max(self.point.get_xdata()) + 50)
            self.ax.set_ylim(max(self.point.get_ydata()) + 50, min(self.point.get_ydata()) - 50)
            self.canvas.draw()

            if self.fc < self.l:
                self.fc += 1
            else:
                print(self.fc + 1)
                self.pxc = self.curva.get_xdata()
                self.pyc = self.curva.get_ydata()
                self.px = self.point.get_xdata()
                self.py = self.point.get_ydata()
                self.fc = 0
                self.timer.stop()
                return

            self.timer = QtCore.QTimer()
            self.timer.setInterval(1)
            self.timer.timeout.connect(a)
            self.timer.start()

        return wrraper

    @anim_decorator
    def _anim(self):
        x = ofsx[:, self.fc]
        y = ofsy[:, self.fc]
        c = cal_curva(x, y)

        self.curva.set_data(c[:, 0].flatten(), c[:, 1].flatten())
        self.line.set_data(x, y)
        self.point.set_data(x, y)
        return 49, self._anim

    def _clear(self):
        self.ax.cla()  # Clear the canvas.
        self.ax.invert_yaxis()
        self.ax.grid(True)
        self.curva = self.ax.plot(np.random.rand(0), linewidth=5, color=curva_color)[0]
        self.line = self.ax.plot(np.random.rand(0), linewidth=1, color=line_color)[0]
        self.point = self.ax.plot(np.random.rand(0), 'o', picker=True, pickradius=5, color=tick_color)[0]
        self.canvas.draw()

    def _rot(self):
        if int(self.angle.text()) >= 0:
            grad = np.arange(0, int(self.angle.value()), 1)
        else:

            grad = np.arange(0, int(self.angle.value()), -1)

        R_point = [self.spinBox_X.value(), self.spinBox_Y.value()]

        self.matrices = np.array([[[np.cos(np.radians(angle)), np.sin(np.radians(angle)), 0],
                                   [-(np.sin(np.radians(angle))), np.cos(np.radians(angle)), 0],
                                   [(-(R_point[0] * (np.cos(np.radians(angle)) - 1)) + R_point[1] * (
                                       np.sin(np.radians(angle)))),
                                    (-(R_point[1] * (np.cos(np.radians(angle)) - 1)) - R_point[0] * (
                                        np.sin(np.radians(angle)))),
                                    1]] for angle in grad])

        self.transform_start()

    def _off(self):
        off_x = np.linspace(0, self.spinBox_3.value())
        off_y = np.linspace(0, self.spinBox_4.value())

        self.matrices = np.array([[[1, 0, 0],
                                   [0, 1, 0],
                                   [off_x[o], off_y[o], 1]] for o in range(len(off_x))])

        self.transform_start()

    @anim_decorator
    def transform_start(self):
        xt1, yt1 = multiply(self.pxc, self.pyc, self.matrices[self.fc])
        x1, y1 = multiply(self.px, self.py, self.matrices[self.fc])

        self.curva.set_data(xt1, yt1)
        self.line.set_data(x1, y1)
        self.point.set_data(x1, y1)
        return len(self.matrices) - 1, self.transform_start


if __name__ == "__main__":
    pool = multiprocessing.Pool()
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    apply_stylesheet(app, theme='theme.xml')
    window.show()
    sys.exit(app.exec_())
