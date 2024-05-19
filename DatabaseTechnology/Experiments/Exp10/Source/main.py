import sys

from pyqt5_plugins.examplebutton import QtWidgets

from control import Controller

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Controller()
    window.show()
    sys.exit(app.exec_())
