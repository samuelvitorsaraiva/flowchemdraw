from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidget, QMenu, QTreeWidgetItem, QMessageBox, QTreeWidgetItemIterator

from flowchemdraw.utils.manage_class import import_class
from flowchemdraw.utils.constantes import *

class treewidget_device_class(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.Main_Window = None

        self.treeWidget_parents = {}
        for name in ITENS_GROUPS:
            self.treeWidget_parents[name] = QTreeWidgetItem(self, [name, 'Folder'])
            self.expandItem(self.treeWidget_parents[name])

    def add_new_item_Qtree(self, head, name):
        parent = QTreeWidgetItem(self.treeWidget_parents[head], [name, 'Folder'])
        self.expandItem(parent)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:

            selected_item = self.currentItem()

            name = selected_item.text(0)

            if not name in ITENS_GROUPS:
                itens = [name]
                if name in self.Main_Window.manage.connection.keys():
                    itens = [name]
                    self.Main_Window.manage._dell_connection(name)
                else:
                    itens += self.Main_Window.manage._dell_component(name)
                    itens = [name]

                for it in itens:
                    self.remove_item(it)


    def remove_item(self, name):
        selected_item = self.select_item(name)
        parent = selected_item.parent()
        if parent is None:
            # It's a top-level item
            index = self.treeWidget_device.indexOfTopLevelItem(selected_item)
            self.treeWidget_device.takeTopLevelItem(index)
        else:
            # It's a child item
            parent.takeChild(parent.indexOfChild(selected_item))



    def select_item(self, text):
        # Iterate through all items in the tree to find the matching item
        iterator = QTreeWidgetItemIterator(self)
        while iterator.value():
            item = iterator.value()
            if item.text(0) == text:
                # Select the item
                self.setCurrentItem(item)
                item.setSelected(True)
                return item
            iterator += 1

    def mousePressEvent(self, event):
        self.item_clicked = self.itemAt(event.pos())
        if self.item_clicked:
            if event.button() == Qt.LeftButton:
                ...
            elif event.button() == Qt.RightButton:
                ...

        super(treewidget_device_class, self).mousePressEvent(event)


