import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from qt_material import apply_stylesheet

from main import *
from multiply_matrix import multiply
from tan import start_tnn

face_color = "#2F323A"
curva_color = "#01F0A8"
tick_color = '#F7ACCF'
line_color = "#5B6A75"


def col(axis):
    axis.set_facecolor(face_color)
    axis.tick_params(labelcolor=tick_color)

    return axis


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.yt = None
        self.xt = None
        self.yn = None
        self.y = None
        self.x = None
        self.matrices = None
        uic.loadUi('untitled.ui', self)
        self.button_off = self.findChild(QtWidgets.QPushButton, 'pushButton_6')
        self.button_rot = self.findChild(QtWidgets.QPushButton, 'pushButton_7')
        self.button_Bui = self.findChild(QtWidgets.QPushButton, 'pushButton_2')
        self.button_Anim = self.findChild(QtWidgets.QPushButton, 'pushButton')
        self.button_tan = self.findChild(QtWidgets.QPushButton, 'pushButton_3')

        self.spinBox_dx = self.findChild(QtWidgets.QSpinBox, 'spinBox_3')
        self.spinBox_dy = self.findChild(QtWidgets.QSpinBox, 'spinBox_4')
        self.spinBox_X = self.findChild(QtWidgets.QSpinBox, 'spinBox')
        self.spinBox_Y = self.findChild(QtWidgets.QSpinBox, 'spinBox_2')
        self.angle = self.findChild(QtWidgets.QSpinBox, 'spinBox_5')
        self.area = self.findChild(QtWidgets.QLabel, 'label_7')
        self.length = self.findChild(QtWidgets.QLabel, 'label_10')

        self.a = self.findChild(QtWidgets.QDoubleSpinBox, 'doubleSpinBox')

        self.point = self.findChild(QtWidgets.QDoubleSpinBox, 'doubleSpinBox_3')
        self.layout = self.findChild(QtWidgets.QVBoxLayout, 'verticalLayout_3')

        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot()
        self.fig.patch.set_facecolor(face_color)

        self.ax.set_aspect(1. / self.ax.get_data_ratio())
        self.ax = col(self.ax)
        self.ax.grid()

        self.button_Bui.clicked.connect(self.draw)
        self.button_Anim.clicked.connect(self.anim)
        self.button_rot.clicked.connect(self.anim_rot)
        self.button_off.clicked.connect(self.anim_off)
        self.point.setRange(int(-5), int(5))
        self.point.valueChanged.connect(self.tn)
        self.layout.addWidget(self.canvas)

        self.i = 0

    def anim_decorator(func):
        def wrraper(self):
            self.ax.cla()
            self.ax = col(self.ax)
            self.ax.grid()

            self.l, a = func(self)
            self.canvas.draw()
            if self.i < self.l:
                self.i += 1
            else:
                print(self.i)

                self.i = 0
                self.timer.stop()

                return

            self.timer = QtCore.QTimer()
            self.timer.setInterval(1)
            self.timer.timeout.connect(a)
            self.timer.start()

        return wrraper

    def draw(self):
        self.ax.cla()
        print('work')
        self.ax.grid()
        x, y = start_main(self.a.value(),self.doubleSpinBox_2.value(),self.horizontalSlider.value())

        self.set_lim(x, y)
        self.ax.plot(x, y, color=curva_color, linewidth=3)
        self.canvas.draw()

    @anim_decorator
    def anim(self):
        x, y = start_main(self.a.value(),self.doubleSpinBox_2.value(),self.horizontalSlider.value())

        self.set_lim(x, y)
        self.ax.plot(x[0:self.i], y[0:self.i], color=curva_color, linewidth=3)
        return len(x), self.anim

    def anim_rot(self):
        if int(self.angle.text()) >= 0:
            grad = np.arange(0, int(self.angle.value()) + 1, 1)
        else:

            grad = np.arange(0, int(self.angle.value()) - 1, -1)
        R_point = [self.spinBox_X.value(), self.spinBox_Y.value()]

        self.matrices = np.array([[[np.cos(np.radians(angle)), np.sin(np.radians(angle)), 0],
                                   [-(np.sin(np.radians(angle))), np.cos(np.radians(angle)), 0],
                                   [(-(R_point[0] * (np.cos(np.radians(angle)) - 1)) + R_point[1] * (
                                       np.sin(np.radians(angle)))),
                                    (-(R_point[1] * (np.cos(np.radians(angle)) - 1)) - R_point[0] * (
                                        np.sin(np.radians(angle)))),
                                    1]] for angle in grad])

        self.x, self.y, self.yn = start_tnn(self.point.value(), self.a.value(),self.doubleSpinBox_2.value())
        self.xt, self.yt = start_main(self.a.value(),self.doubleSpinBox_2.value(),self.horizontalSlider.value())
        self.transform_start()

    def anim_off(self):

        off_x = np.linspace(0, self.spinBox_dx.value())
        off_y = np.linspace(0, self.spinBox_dy.value())

        self.matrices = np.array([[[1, 0, 0],
                                   [0, 1, 0],
                                   [off_x[o], off_y[o], 1]] for o in range(len(off_x))])

        self.x, self.y, self.yn = start_tnn(self.point.value(), self.a.value(),self.doubleSpinBox_2.value())
        self.xt, self.yt = start_main(self.a.value(),self.doubleSpinBox_2.value(),self.horizontalSlider.value())
        self.transform_start()

    def tn(self):

        x, y, yn = start_tnn(self.point.value(), self.a.value(),self.doubleSpinBox_2.value())
        xt, yt = start_main(self.a.value(),self.doubleSpinBox_2.value(),self.horizontalSlider.value())
        self.ax.cla()
        self.ax = col(self.ax)
        self.ax.grid()
        self.set_lim(xt, yt)

        self.ax.plot(xt, yt, color=curva_color, linewidth=3)
        self.ax.plot(x, y, color=tick_color)
        self.ax.plot(x, yn, color=line_color)
        self.canvas.draw()

    @anim_decorator
    def transform_start(self):

        xt1, yt1 = multiply(self.xt, self.yt, self.matrices[self.i])
        x1, y1 = multiply(self.x, self.y, self.matrices[self.i])
        x2, yn2 = multiply(self.x, self.yn, self.matrices[self.i])

        self.set_lim(xt1, yt1)

        self.ax.plot(xt1, yt1, color=curva_color, linewidth=3)
        self.ax.plot(x1, y1, color=tick_color)
        self.ax.plot(x2, yn2, color=line_color)
        self.ax.plot(self.spinBox_X.value(), self.spinBox_Y.value(), "o", color=curva_color)
        return len(self.matrices) - 1, self.transform_start

    def set_lim(self, x, y):
        mxd = min(x)
        axd = max(x)
        myd = min(y)
        ayd = max(y)
        self.ax.set_xlim(mxd - 10, axd + 10)
        self.ax.set_ylim(myd - 10, ayd + 10)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    apply_stylesheet(app, theme='theme.xml')
    window.show()
    sys.exit(app.exec_())
