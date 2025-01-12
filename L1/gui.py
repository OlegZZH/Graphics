import sys

from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from qt_material import apply_stylesheet

from aff import aff_start
from main import *
from offset import off_start
from pro import pro_start
from rot import rot_start


def col(axis):
    axis.set_facecolor(face_color)
    axis.tick_params(labelcolor=tick_color)

    return axis


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('untitled1.ui', self)

        self.pushButton_2.clicked.connect(self.reset)

        self.doubleSpinBox.valueChanged.connect(self.gen)
        self.doubleSpinBox_2.valueChanged.connect(self.gen)
        self.doubleSpinBox_3.valueChanged.connect(self.gen)
        self.doubleSpinBox_4.valueChanged.connect(self.gen)
        self.doubleSpinBox_5.valueChanged.connect(self.gen)


        self.spinBox.valueChanged.connect(self.rotate)
        self.spinBox_2.valueChanged.connect(self.rotate)
        self.spinBox_10.valueChanged.connect(self.rotate)

        self.spinBox_3.valueChanged.connect(self.offset)
        self.spinBox_4.valueChanged.connect(self.offset)

        self.pushButton_4.clicked.connect(self.aff)
        self.pushButton_3.clicked.connect(self.pro)

        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)

        self.ax = self.fig.add_subplot()
        self.fig.patch.set_facecolor(face_color)
        self.ax.tick_params(axis="x", colors=tick_color)
        self.ax.tick_params(axis="y", colors=tick_color)
        self.ax.spines['bottom'].set_color('w')
        self.ax.spines['top'].set_color('w')
        self.ax.spines['right'].set_color('w')
        self.ax.spines['left'].set_color('w')
        plt.gca().set_aspect("equal")
        self.ax.set_aspect(1. / self.ax.get_data_ratio())
        self.ax = col(self.ax)
        self.grid()
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.verticalLayout_4.addWidget(self.canvas)
        # self.show()

    def draw_decorator(func):
        def wrapper(self):
            self.ax.cla()
            obj = func(self)
            self.grid()
            for i in obj:
                self.ax.plot(*i, linewidth=3, color=main_color)
            self.canvas.draw()

        return wrapper

    def draw_decorator_for_grid_transformation(func):
        def wrapper(self):
            self.ax.cla()
            obj, transform_line = func(self)
            for n, i in enumerate(transform_line):
                h, v = i
                if n == 10:
                    self.ax.plot(*h, linewidth=2.5, color=axis_color)
                    self.ax.plot(*v, linewidth=2.5, color=axis_color)
                else:
                    self.ax.plot(*h, linewidth=0.5, color=axis_color)
                    self.ax.plot(*v, linewidth=0.5, color=axis_color)

            for i in obj:
                self.ax.plot(*i, linewidth=3, color=main_color)
            self.canvas.draw()

        return wrapper

    @draw_decorator
    def gen(self):
        return self._get_object()
    @draw_decorator
    def rotate(self):
        self.ax.plot(self.spinBox.value(), self.spinBox_2.value(), 'o', color=main_color)
        return rot_start(self.spinBox.value(), self.spinBox_2.value(), self.spinBox_10.value(),self._get_object())

    @draw_decorator
    def offset(self):
        return off_start(self.spinBox_3.value(), self.spinBox_4.value(),self._get_object())

    @draw_decorator_for_grid_transformation
    def aff(self):

        return aff_start(x111=self.doubleSpinBox_8.value(), x121=self.doubleSpinBox_9.value(),
                         x211=self.doubleSpinBox_10.value(), x221=self.doubleSpinBox_11.value(),
                         x311=self.doubleSpinBox_6.value(), x321=self.doubleSpinBox_7.value(),obj=self._get_object())

    @draw_decorator_for_grid_transformation
    def pro(self):

        return pro_start(
            self.doubleSpinBox_15.value(), self.doubleSpinBox_16.value(),
            self.doubleSpinBox_17.value(), self.doubleSpinBox_18.value(),
            self.doubleSpinBox_19.value(), self.doubleSpinBox_20.value(), self.doubleSpinBox_12.value(),
            self.doubleSpinBox_13.value(),
            self.doubleSpinBox_14.value(),self._get_object())

    def _get_object(self):
        return start_main(self.doubleSpinBox.value(), self.doubleSpinBox_2.value(), self.doubleSpinBox_3.value(),
                          self.doubleSpinBox_4.value(),self.doubleSpinBox_5.value())
    def reset(self):
        self.doubleSpinBox.setValue(1)
        self.doubleSpinBox_2.setValue(2)
        self.doubleSpinBox_3.setValue(5)
        self.doubleSpinBox_4.setValue(3)
        self.doubleSpinBox_5.setValue(2)


        self.spinBox_10.setValue(0)

        self.spinBox.setValue(0)
        self.spinBox_2.setValue(0)
        self.spinBox_3.setValue(0)
        self.spinBox_4.setValue(0)
        self.doubleSpinBox_6.setValue(0)
        self.doubleSpinBox_7.setValue(0)
        self.doubleSpinBox_8.setValue(1)
        self.doubleSpinBox_9.setValue(0)
        self.doubleSpinBox_10.setValue(0)
        self.doubleSpinBox_11.setValue(1)
        self.doubleSpinBox_12.setValue(0)
        self.doubleSpinBox_13.setValue(0)
        self.doubleSpinBox_14.setValue(25)
        self.doubleSpinBox_15.setValue(80)
        self.doubleSpinBox_16.setValue(5)
        self.doubleSpinBox_17.setValue(1)
        self.doubleSpinBox_18.setValue(9)
        self.doubleSpinBox_19.setValue(80)
        self.doubleSpinBox_20.setValue(1)
        self.gen()

    def grid(self):
        h = np.linspace(-20,20, 2)
        hx = np.array([])
        hy = np.array([])

        for i in range(40):
            hx = np.append(hx, h)
        for i in range(-20, 20, 1):
            hy = np.append(hy, [i, i])
        for i in range(0, 80, 2):
            if i == 40:
                self.ax.plot((hx[i], hx[i + 1]), (hy[i], hy[i + 1]), linewidth=2.5, color=axis_color)
                self.ax.plot((hy[i], hy[i + 1]), (hx[i], hx[i + 1]), linewidth=2.5, color=axis_color)
            else:
                self.ax.plot((hx[i], hx[i + 1]), (hy[i], hy[i + 1]), linewidth=0.5, color=axis_color)
                self.ax.plot((hy[i], hy[i + 1]), (hx[i], hx[i + 1]), linewidth=0.5, color=axis_color)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    apply_stylesheet(app, theme='theme.xml')
    window.show()
    sys.exit(app.exec_())
