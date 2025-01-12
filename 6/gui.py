import sys

import numpy as np
from PyQt5 import QtWidgets, uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from qt_material import apply_stylesheet

from projection import projection_start
from read import pxc, pyc

face_color = "#2F323A"
curva_color = "#01F0A8"
tick_color = '#F7ACCF'
line_color = "#5B6A75"


def col(ax):
    ax.set_facecolor(face_color)
    ax.tick_params(labelcolor=tick_color)

    return ax


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('untitled1.ui', self)

        self.X = self.findChild(QtWidgets.QDial, 'dial')
        self.Y = self.findChild(QtWidgets.QDial, 'dial_2')
        self.d = self.findChild(QtWidgets.QSlider, 'horizontalSlider')

        self.layout = self.findChild(QtWidgets.QVBoxLayout, 'verticalLayout_3')

        self.Reset = self.findChild(QtWidgets.QPushButton, 'pushButton_2')

        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.ax1 = self.fig.add_subplot(121, projection='3d')
        self.ax2 = self.fig.add_subplot(122, aspect="equal")
        self.ax1.view_init(45, 60)
        self.fig.patch.set_facecolor(face_color)
        self.ax1 = col(self.ax1)
        self.ax2 = col(self.ax2)

        self.X.valueChanged.connect(self.draw)
        self.Y.valueChanged.connect(self.draw)

        self.d.valueChanged.connect(self.draw)
        self.horizontalSlider_2.valueChanged.connect(self.draw)

        self.u = np.linspace(0, 1, 10)
        self.v = self.u
        self.P00 = np.array([0, 0, 1])
        self.P01 = np.array([0, 1, 0])
        self.P10 = np.array([1, 0, 0])
        self.P11 = np.array([1, 1, 1])
        self.Reset.clicked.connect(self.reset)
        self.draw()
        self.layout.addWidget(self.canvas)


    def sur(self, u, v):
        R = self.d.value() / 10
        x =  R * np.cos(u)
        y =  R * np.sin(u)
        z = v
        return x, y, z

    def draw(self):
        self.ax1.cla()
        self.ax2.cla()
        h = self.horizontalSlider_2.value() / 10
        self.X.setMinimum(int((0 - min(pxc)) * 1000))
        self.X.setMaximum(int((np.pi/2 - max(pxc)) * 1000))
        self.Y.setMinimum(int(0 * 1000))
        self.Y.setMaximum(int((h-max(pyc)) * 1000))
        shift_text_X = self.X.value() / 1000
        shift_text_Y = self.Y.value() / 1000


        self.ax1.scatter(0, 0, 0, color=curva_color)
        self.ax2.plot(0, 0, 'o', color=curva_color)
        u = np.linspace(0,  np.pi/2, len(pxc))
        v = np.linspace(0,  h, len(pyc))
        U, V = np.meshgrid(u, v)

        Xe, Ye, Ze = self.sur(U, V)
        sh = Xe.shape

        self.ax1.plot_wireframe(Xe, Ye, Ze, color="black",
                                alpha=0.3)

        surface = np.c_[Xe.flatten(), Ye.flatten(), Ze.flatten()]
        Xe, Ye, Ze = projection_start(surface,self.horizontalSlider_2.value())
        Xe = Xe.reshape(sh)
        Ye = Ye.reshape(sh)
        for i, j in zip(Xe.T[::5], Ye.T[::5]):
            self.ax2.plot(i, j, color=tick_color, alpha=0.3)
        for i, j in zip(Xe[::10], Ye[::10]):
            self.ax2.plot(i, j, color=tick_color, alpha=0.3)

        Xp, Yp, Zp = self.sur(pxc + shift_text_X, pyc + shift_text_Y)

        self.ax1.plot_wireframe(Xp, Yp, np.array([Zp]),
                                linewidth=3, color=curva_color)
        text = np.c_[Xp, Yp, Zp]
        Xp, Yp, Zp = projection_start(text,self.horizontalSlider_2.value())

        self.ax2.plot(Xp, Yp, linewidth=3, color=curva_color)

        self.ax1.set_box_aspect([ub - lb for lb, ub in (getattr(self.ax1, f'get_{a}lim')() for a in 'xyz')])

        self.ax1.set_xlabel("X", color=tick_color)
        self.ax1.set_ylabel("Y", color=tick_color)
        self.ax1.set_zlabel("Z", color=tick_color)

        self.canvas.draw()

    def reset(self):
        self.X.setValue(0)
        self.Y.setValue(0)
        self.d.setValue(0)
        self.horizontalSlider_2.setValue(10)
        self.ax1.view_init(45, 60)
        self.canvas.draw()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    apply_stylesheet(app, theme='theme.xml')

    window.show()
    sys.exit(app.exec_())
