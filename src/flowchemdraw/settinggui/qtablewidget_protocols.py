import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from flowchemdraw.utils.constantes import ADRESS


class qtablewidget_protocols(QTableWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.Main_Window = None

        self.item_detailed: None | dict = None

        self.item_clicked = None

        # Connect signals
        self.cellClicked.connect(self.on_cell_clicked)

        self.itemChanged.connect(self.on_item_changed)

    def _update_device(self, name):

        infor = dict()

        infor['object:'] = 'component'

        infor['name:'] = name

        infor['class name:'] = self.Main_Window.manage.components[name].class_name

        infor['figure name:'] = self.Main_Window.manage.components[name].figure_class

        for key, value in self.Main_Window.manage.components[name].draw.additional_configuration.items():

            infor[key] = value['value']

        self.item_detailed = infor

        self.build(infor)

    def _uptade_connection(self, name):

        infor = dict()

        infor['object:'] = 'connection'

        infor['name:'] = name

        infor['Origin:'] = self.Main_Window.manage.connection[name].origin

        infor['Destiny:'] = self.Main_Window.manage.connection[name].destiny

        for key, value in self.Main_Window.manage.connection[name].draw.additional_configuration.items():

            infor[key] = value

        self.item_detailed = infor

        self.build(infor)

    def _update_command(self, stage: str, command: str):

        self.clear_table()

        command = int(command.split()[0])

        dic = {'object:': 'protocol'}

        dic = dic | self.Main_Window.manage_protocol.commands[stage][command]

        self.item_detailed = dic

        # Set the dimensions of the table
        n = len(dic.keys())
        self.setRowCount(n)
        self.setColumnCount(1)

        # Set headers
        self.setHorizontalHeaderLabels(["Values"])
        self.setVerticalHeaderLabels(dic.keys())

        k = 0
        for item in dic.values():
            if item == None:
                # Adding an icon to a specific cell regarding missing information
                item_table = QTableWidgetItem("None")
                item_table.setIcon(QIcon(ADRESS + "/figures/Icons/alert.jpg"))
                self.setItem(k, 0, item_table)
            else:
                item_table = QTableWidgetItem(str(item))
                self.setItem(k, 0, item_table)

            if k < 3:
                item_table.setFlags(item_table.flags() & ~Qt.ItemIsEditable)
            k += 1

        self.item_clicked = None

    def _update_stage(self, stage):
        ...

    def clear_table(self):

        self.clear()

    def build(self, dic: dict):

        self.clear_table()

        # Set the dimensions of the table
        n = len(dic.keys())
        self.setRowCount(n)
        self.setColumnCount(1)

        # Set headers
        self.setHorizontalHeaderLabels(["Values"])
        self.setVerticalHeaderLabels(dic.keys())

        k = 0
        for item in dic.values():
            if item == None:
                # Adding an icon to a specific cell regarding missing information
                item_table = QTableWidgetItem("None")
                item_table.setIcon(QIcon(ADRESS + "/figures/Icons/alert.jpg"))
                self.setItem(k, 0, item_table)
            else:
                item_table = QTableWidgetItem(str(item))
                self.setItem(k, 0, item_table)

            if k < 4:
                item_table.setFlags(item_table.flags() & ~Qt.ItemIsEditable)
            k += 1

        self.item_clicked = None

    def on_cell_clicked(self, row, column):
        self.item_clicked = (row, column)

    def on_item_changed(self, item):
        if self.item_clicked != None:

            if self.item_detailed['object:'] == 'component' or self.item_detailed['object:'] == 'connection':
                name = self.item_detailed['name:']
                variavel = self.verticalHeaderItem(item.row()).text()
                class_v = self.Main_Window.manage.components[name].draw.additional_configuration[variavel]['class']
                self.Main_Window.manage.components[name].draw.additional_configuration[variavel]['value'] = class_v(item.text())

            else:
                stage = self.Main_Window.treeView.itemFromIndex(self.Main_Window.treeView.selectedIndexes()[0]).parent().text(0)
                id_ = int(self.Main_Window.treeView.itemFromIndex(self.Main_Window.treeView.selectedIndexes()[0]).text(0).split()[0])
                variavel = self.verticalHeaderItem(item.row()).text()
                self.Main_Window.manage_protocol.commands[stage][id_][variavel] = float(item.text())

        self.item_clicked = None


