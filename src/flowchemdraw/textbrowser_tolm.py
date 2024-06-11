from PyQt5.QtWidgets import QTextBrowser, QMenu
from PyQt5.QtCore import Qt
from flowchemdraw.components import Edit_Setting_Window
import tomllib

class textbrowser_tolm(QTextBrowser):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.Edit_Setting_Window = None

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            ...
        elif event.button() == Qt.RightButton:
            menu = QMenu()
            action = menu.addAction("Edit")
            action.triggered.connect(self.edit_toml_file)
            menu.exec_(self.viewport().mapToGlobal(event.pos()))

        super(textbrowser_tolm, self).mousePressEvent(event)


    def add_tolm_file(self, file, adress):

        self.adress = adress

        self.adress_file = file

        with open(file, 'r') as file:
            self.content = file.read()

        self.setPlainText(self.content)



    def edit_toml_file(self):

        self.Edit_Setting_Window = Edit_Setting_Window(self, adress=self.adress, adress_file=self.adress_file, text=self.content)

        self.Edit_Setting_Window.show()

