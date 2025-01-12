import sys

import numpy as np
from PyQt5 import QtWidgets, uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from qt_material import apply_stylesheet

from obj import get_obj
from projection import projection_start
from rot import rot_start

face_color = "#1E212B"
curva_color = "#4D8B31"
tick_color = '#FFC800'
line_color = "#FF8427"

def col(ax):
    ax.set_facecolor(face_color)
    ax.tick_params(labelcolor=tick_color)

    return ax

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('untitled1.ui', self)
        self.button = self.findChild(QtWidgets.QPushButton, 'pushButton')
        self.sliderX = self.findChild(QtWidgets.QDial, 'dial')
        self.sliderY = self.findChild(QtWidgets.QDial, 'dial_2')
        self.sliderZ = self.findChild(QtWidgets.QDial, 'dial_3')
        self.labelX = self.findChild(QtWidgets.QLabel, 'label')
        self.labelY = self.findChild(QtWidgets.QLabel, 'label_2')
        self.labelZ = self.findChild(QtWidgets.QLabel, 'label_3')
        self.d = self.findChild(QtWidgets.QSlider, 'horizontalSlider')

        self.widget = self.findChild(QtWidgets.QWidget, 'widget')

        self.button.clicked.connect(self.reset)
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.ax1 = self.fig.add_subplot(211, projection='3d')
        self.ax2 = self.fig.add_subplot(212, aspect="equal")
        self.fig.patch.set_facecolor(face_color)
        self.ax1 = col(self.ax1)
        self.ax2 = col(self.ax2)
        self.ax1.set_xlabel('X', color=line_color)
        self.ax1.set_ylabel('Y', color=line_color)
        self.ax1.set_zlabel('Z', color=line_color)
        self.ax1.view_init(45, 60)
        self.point, self.faces = get_obj()
        self.default_point = self.point
        self.sliderX.valueChanged.connect(self.draw_rot)
        self.sliderY.valueChanged.connect(self.draw_rot)
        self.sliderZ.valueChanged.connect(self.draw_rot)
        self.Y.valueChanged.connect(self.draw_rot)
        self.Z.valueChanged.connect(self.draw_rot)

        self.draw()
        self.set_size()
        self.layout = self.findChild(QtWidgets.QHBoxLayout, 'horizontalLayout')
        self.layout.addWidget(self.canvas)

    def draw(self):

        self.ax1.cla()
        self.ax2.cla()

        self.face3d = np.array([[self.point[y] for y in x] for x in self.faces], dtype=object)
        for p in self.face3d:
            self.ax1.add_collection3d(
                Poly3DCollection([p], color=curva_color, edgecolor=tick_color, linewidths=1, alpha=0.3))

        point = projection_start(self.point,self.Y.value(),self.Z.value())

        face3d = np.array([[point[y] for y in x] for x in self.faces], dtype=object)
        self.ax2.plot(np.array(point[:, 0]), np.array(point[:, 1]), "o", color=line_color)
        for i in range(len(face3d)):
            self.ax1.plot(np.array(face3d[i])[:, 0], np.array(face3d[i])[:, 1], zs=-2, zdir='x', color=tick_color)
            self.ax2.plot(np.array(face3d[i])[:, 0], np.array(face3d[i])[:, 1], color=curva_color)

        self.set_size()
        self.canvas.draw()

    def draw_rot(self):
        self.point = rot_start(self.default_point, self.sliderX.value(), self.sliderY.value(), self.sliderZ.value())
        self.draw()

    def reset(self):
        self.sliderX.setValue(0)
        self.sliderY.setValue(0)
        self.sliderZ.setValue(0)
        self.ax1.view_init(45, 60)
        self.canvas.draw()

    def set_size(self):
        self.ax1.set_xlim(-2, 2)
        self.ax1.set_ylim(-2, 2)
        self.ax1.set_zlim(-2, 2)
        self.ax1.set_xlabel('X', color=line_color)
        self.ax1.set_ylabel('Y', color=line_color)
        self.ax1.set_zlabel('Z', color=line_color)
        self.ax1.set_box_aspect([ub - lb for lb, ub in (getattr(self.ax1, f'get_{a}lim')() for a in 'xyz')])

        self.ax2.set_xlim(-2, 2)
        self.ax2.set_ylim(-2, 2)
        self.ax2.set_xlabel('Y', color=line_color)
        self.ax2.set_ylabel('Z', color=line_color)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    apply_stylesheet(app, theme='theme.xml')
    window.show()
    sys.exit(app.exec_())
