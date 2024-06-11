from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidget, QMenu, QTreeWidgetItem, QMessageBox

from flowchemdraw.utils.manage_class import import_class
from flowchemdraw.utils.constantes import *

class qtreewidget_add_component_class(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.Main_Window = None

        self.type: str = 'others'

    def build_qtree(self, components):
        self.clear()
        for c in components.keys():
            if components[c] == None:
                self.expandItem(QTreeWidgetItem(self, [c, 'Folder']))
            elif components[c]['components'] != None:
                item = QTreeWidgetItem(self, [c, 'Folder'])
                for key in components[c]['components'].keys():
                    item.addChild(QTreeWidgetItem(item, [key, 'Folder']))
                    self.expandItem(item)
            else:
                self.expandItem(QTreeWidgetItem(self, [c, 'Folder']))

    def mousePressEvent(self, event):
        self.item_clicked = self.itemAt(event.pos())
        if self.item_clicked:
            if event.button() == Qt.LeftButton:
                name = self.item_clicked.text(0)
                if self.item_clicked.parent() is not None:
                    name = self.item_clicked.parent().text(0) + '/' + name
                self.Main_Window.widget_components.draw_component(name)
            elif event.button() == Qt.RightButton:
                menu = QMenu()
                action = menu.addAction("Add")
                action.triggered.connect(self.addition_component)
                menu.exec_(self.viewport().mapToGlobal(event.pos()))

        super(qtreewidget_add_component_class, self).mousePressEvent(event)

    def addition_component(self):
        name = self.item_clicked.text(0)

        if self.item_clicked.parent() is not None:
            name = self.item_clicked.parent().text(0)+'/'+name

        name = self.Main_Window.manage._add_component(name)

        if name != '-':

            self.Main_Window.treeWidget_device.add_new_item_Qtree(self.type, name)

            self.Main_Window.widget_drawing.draw()

