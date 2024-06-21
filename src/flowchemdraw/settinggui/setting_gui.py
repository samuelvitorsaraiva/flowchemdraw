from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import sys

from flowchemdraw.utils.constantes import ADRESS

class main_widget(QMainWindow):

    def __init__(self):
        super().__init__()

        loadUi(ADRESS + "/settinggui/setting_draw.ui", self)

        self.setWindowTitle("Flowchem plugin - Drawing platform system")

        self.setWindowIcon(QtGui.QIcon(ADRESS + '/figures/icon_window.png'))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = app.screens()[0]
    window = main_widget()
    window.show()
    sys.exit(app.exec_())