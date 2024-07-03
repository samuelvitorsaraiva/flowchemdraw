from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import sys
import pickle
import time

from flowchemdraw.manage import manage
from flowchemdraw.utils.constantes import ADRESS, SIMULATION_VELOCITY
from flowchemdraw.manage import manage_protocols


class main_widget(QMainWindow):

    def __init__(self):
        super().__init__()

        loadUi(ADRESS + "/settinggui/setting_draw.ui", self)

        self.setWindowTitle("Flowchem plugin - Drawing platform system")

        self.setWindowIcon(QtGui.QIcon(ADRESS + '/figures/Icons/icon_window.png'))

        self.actionLoad_Project.triggered.connect(self.load)

        self.pushButton_run.clicked.connect(self.main_loop)

        self.build()

    def build(self):

        self.widget.Main_Window = self

        self.tableWidget.Main_Window = self

        self.treeView.Main_Window = self

        self.manage = manage(self.widget.axes)

        self.event_loop = True

        self.manage_protocol = manage_protocols(self.manage)

    def load(self):

        option = QFileDialog.Options()
        option |= QFileDialog.DontUseNativeDialog
        name = QFileDialog.getOpenFileName(self, "Load the project", " ", "pickle Files (*.p)",
                                           options=option)
        if name[0]:

            with open(name[0], 'rb') as f:

                data = pickle.load(f)

                self.manage._update(data)

                self.widget.draw()

    def main_loop(self):

        tic = time.perf_counter()

        while self.event_loop:

            toc = time.perf_counter()

            if (toc - tic) > SIMULATION_VELOCITY/10:

                for c in self.manage.connection.values():
                    c.operation_draw()

                for c in self.manage.components.values():
                    c.operation_draw()

                self.widget.draw()

                tic = time.perf_counter()

            QApplication.processEvents()

    def closeEvent(self, event):

        self.event_loop = False



if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = app.screens()[0]
    window = main_widget()
    window.show()
    sys.exit(app.exec_())