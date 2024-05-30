from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget, QMenu, QTreeWidgetItem, QMessageBox

from flowchemdraw.utils.manage_class import import_class
from flowchemdraw.mplwidget import LOCATION_NEW_DEVICES

class custom_listwidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.Main_Window = None

    def mousePressEvent(self, event):
        super().mousePressEvent(event)  # Call the base class implementation

        self.item_clicked = self.itemAt(event.pos())
        if self.item_clicked:
            if event.button() == Qt.RightButton:
                menu = QMenu()
                action = menu.addAction("Add")
                action.triggered.connect(self.addition_component)
                menu.exec_(self.viewport().mapToGlobal(event.pos()))

    def addition_component(self):
        name = self.item_clicked.text()

        k = 1
        for dev in self.Main_Window.components.keys():
            if dev.split('_')[0] == name:
                k += 1

        name = name + '_' + str(k)

        for dev in self.Main_Window.components.keys():
            x = self.Main_Window.components[dev]['draw_class'].position[0]
            y = self.Main_Window.components[dev]['draw_class'].position[1]
            if LOCATION_NEW_DEVICES[0] == x and LOCATION_NEW_DEVICES[0] == y:
                msg = QMessageBox()
                msg.setWindowTitle("Warning")
                msg.setText("There is a device placed in the designated area to new ones. "
                            "Please move away its device of this area before add new one.")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
                return

        dev = import_class('flowchemdraw.figures', name.split('_')[0])
        self.Main_Window.components[name] = {'draw_class': dev(self.Main_Window.widget_drawing.axes,
                                                            pos=LOCATION_NEW_DEVICES), 'type': name.split('_')[0]}

        parent = QTreeWidgetItem(self.Main_Window.treeWidget_parents['devices'], [name, 'Folder'])
        self.Main_Window.treeWidget_device.expandItem(parent)

        self.Main_Window.widget_drawing.draw()

