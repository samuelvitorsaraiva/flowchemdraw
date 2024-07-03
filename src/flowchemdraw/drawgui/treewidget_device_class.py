from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidget, QMenu, QTreeWidgetItem, QMessageBox, QTreeWidgetItemIterator, QDialog

from flowchemdraw.utils.manage_class import import_class
from flowchemdraw.utils.constantes import *
from flowchemdraw.components import CustomMessageBox

class treewidget_device_class(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.Main_Window = None

        self.component_selected = None

        self.treeWidget_parents = {}
        for name in ITENS_GROUPS:
            self.treeWidget_parents[name] = QTreeWidgetItem(self, [name, 'Folder'])
            self.expandItem(self.treeWidget_parents[name])



    def add_new_item_Qtree(self, head, name):
        parent = QTreeWidgetItem(self.treeWidget_parents[head], [name, 'Folder'])
        self.expandItem(parent)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.remove_item_p1()


    def remove_item_p1(self):

            selected_item = self.currentItem()

            name = selected_item.text(0)

            if not name in ITENS_GROUPS:
                itens = [name]
                if name in self.Main_Window.manage.connection.keys():
                    itens = [name]
                    self.Main_Window.manage._dell_connection(name)
                else:
                    itens += self.Main_Window.manage._dell_component(name)

                self.Main_Window.textBrowser.write_toml_file(self.Main_Window.manage.components)

                for it in itens:
                    self.remove_item(it)

                self.Main_Window.widget_drawing.draw()


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

        if self.component_selected != None:
            if self.component_selected in self.Main_Window.manage.components.keys():
                self.Main_Window.manage.components[self.component_selected].draw.active_draw(False)
            elif self.component_selected in self.Main_Window.manage.connection.keys():
                self.Main_Window.manage.connection[self.component_selected].draw.active_draw(False)


        self.item_clicked = self.itemAt(event.pos())
        if self.item_clicked:

            if not self.item_clicked.text(0) in ITENS_GROUPS:

                if event.button() == Qt.LeftButton:

                    self.component_selected = self.item_clicked.text(0)

                    if self.component_selected in self.Main_Window.manage.components.keys():
                        self.Main_Window.manage.components[self.component_selected].draw.active_draw(True)
                    else:
                        self.Main_Window.manage.connection[self.component_selected].draw.active_draw(True)

                elif event.button() == Qt.RightButton:
                    menu = QMenu()
                    action = menu.addAction("Settings")
                    action2 = menu.addAction("Delete")
                    action.triggered.connect(self.setting_file)
                    action2.triggered.connect(self.remove_item_p1)
                    menu.exec_(self.viewport().mapToGlobal(event.pos()))

        self.Main_Window.widget_drawing.draw()

        super(treewidget_device_class, self).mousePressEvent(event)

    def setting_file(self):

        if self.item_clicked.parent().text(0) == 'devices':

            name = self.item_clicked.text(0)

            cfg = self.Main_Window.manage.components[name].configuration_block

            dialog = CustomMessageBox(name=name, class_name=name.split('/')[0], configuration_file=cfg)
            if dialog.exec_() == QDialog.Accepted:
                [name, config_dict] = dialog.get_input_device()

                if len(name.split('/')) > 1:
                    for key, comp in self.Main_Window.manage.components.items():
                        if len(key.split('/')) > 1 and key.split('/')[0] == name.split('/')[0]:
                            comp.update_configuration_file(config_dict)
                else:
                    self.Main_Window.manage.components[name].update_configuration_file(config_dict)

            self.Main_Window.textBrowser.write_toml_file(self.Main_Window.manage.components)




