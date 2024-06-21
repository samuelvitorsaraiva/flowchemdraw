from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
import sys
import os

import pickle
from flowchemdraw.utils.manage_class import import_class, get_package_directory
from flowchemdraw.utils.drawclass import drawobject
from flowchemdraw.manage import manage
from flowchemdraw.utils.constantes import *



class Edit_Setting_Window(QMainWindow):

    def __init__(self, MainWindow, text=''):
        super().__init__()

        loadUi("./components/Edit_Setting_Files.ui", self)

        self.pushButton_cancel.clicked.connect(self.click_cancel)

        self.pushButton_save.clicked.connect(self.click_save)

        self.textEdit.append(text)

        self.MainWindow = MainWindow


    def click_save(self):

        self.new_text = self.textEdit.toPlainText()

        self.MainWindow.content = self.new_text

        self.MainWindow.setPlainText(self.new_text)

        self.MainWindow.write_temporary_file()

        self.MainWindow.edit_configuration_file()

        self.close()

    def click_cancel(self):
        self.close()


if __name__ == '__main__':
    adress = os.getcwd()
    app = QApplication(sys.argv)
    screen = app.screens()[0]
    window = Edit_Setting_Window(adress)
    window.show()
    sys.exit(app.exec_())