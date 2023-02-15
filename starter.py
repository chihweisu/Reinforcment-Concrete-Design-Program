from PyQt5 import QtWidgets
from menu_controller import MenuController

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    the_mainwindow = MenuController()
    the_mainwindow.show()
    sys.exit(app.exec_())