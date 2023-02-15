from PyQt5 import QtGui,QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import QThread

             


class MplCanvas(FigureCanvas,QThread):
    def __init__(self):
        self.fig = Figure(figsize=(2,2),facecolor='#191D24')
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.fig.set_size_inches(1,1)

class RcPmmWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.canvas.axes = self.canvas.figure.add_subplot(111,facecolor='white')
        self.canvas.axes.set_xlabel('\u03c6 Mn(tf-m)', fontsize=8, color='white')
        self.canvas.axes.set_ylabel('\u03c6 Pn(tf)', fontsize=8, color='white')
        self.canvas.axes.tick_params(axis='both', which='major', labelsize=8, labelcolor='white')
        self.canvas.axes.grid(True,linestyle='--', color='black')
        self.vbl = QtWidgets.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)

        


            

        
