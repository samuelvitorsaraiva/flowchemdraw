from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
import sys
import os

import pickle
from flowchemdraw.utils.manage_class import import_class, get_package_directory
from flowchemdraw.utils.drawclass import drawobject
from flowchemdraw.utils.devices_flowchem import devices_flowchem
from flowchemdraw.manage import manage
from flowchemdraw.utils.constantes import *

from flowchemdraw.figures import __all__ as ilustrations

adress = os.getcwd()

class main_widget(QMainWindow):

    def __init__(self):
        super().__init__()

        loadUi(adress + "/flowchem_draw.ui", self)

        self.setWindowTitle("Flowchem plugin - Drawing platform system")

        self.setWindowIcon(QtGui.QIcon(adress + '/figures/icon_window.png'))

        self.actionSave_Project.triggered.connect(self.save)

        self.actionLoad_Project.triggered.connect(self.load)

        self.radioButton_toml_available.toggled.connect(self.options_connections)

        self.radioButton_toml_not_available.toggled.connect(self.options_connections)

        self.build()

    def build(self):

        self.widget_drawing.Main_Window = self

        self.treeWidget_device.setHeaderLabels(['components'])

        self.treeWidget_device.setColumnCount(1)

        self.treeWidget_device.Main_Window = self

        self.manage = manage(ax=self.widget_drawing.axes)

        ilustratio_tree = dict()
        for fig in ilustrations:
            ilustratio_tree[fig] = None

        self.treeWidget_add_others.build_qtree(ilustratio_tree)

        self.treeWidget_add_others.Main_Window = self

        self.treeWidget_add_devices.Main_Window = self

        #self.devices_flowchem = devices_flowchem()

    def save(self):
        if not self.components:
            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setText("There is nothing to be saved.")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
            return

        option = QFileDialog.Options()
        option |= QFileDialog.DontUseNativeDialog
        name = QFileDialog.getSaveFileName(self, "Save the project", "Project.p",
                                           "pickle Files (*.p)",
                                           options=option)

        if name[0]:
            with open(name[0], 'wb') as f:
                pickle.dump(self.components, f)

    def load(self):


        option = QFileDialog.Options()
        option |= QFileDialog.DontUseNativeDialog
        name = QFileDialog.getOpenFileName(self, "Load the project", " ", "pickle Files (*.p)",
                                           options=option)
        if name[0]:

            if self.components:
                qm = QMessageBox()
                ret = qm.question(self, '', "Are you sure you want to remove the current project in order "
                                            "to load a new one? Please ensure that you save it before doing so if you "
                                            "want to keep it.?", qm.Yes | qm.No)
                if ret == qm.Yes:
                    iterator = QTreeWidgetItemIterator(self.treeWidget_device)
                    while iterator.value():
                        self.treeWidget_device.setCurrentItem(iterator.value())
                        self.remove_selected_item()
                        iterator += 1
                else:
                    return

            with open(name[0], 'rb') as f:
                data = pickle.load(f)
                for name in data.keys():
                    if data[name]['draw_class'].type_object == 'devices':
                        dev = import_class('flowchemdraw.figures', name.split('_')[0])
                        self.components[name] = {'draw_class': dev(self.widget_drawing.axes,
                                                                   pos=data[name]['draw_class'].position),
                                                 'type': name.split('_')[0]}
                        self.add_new_item_Qtree('devices', name)
                    else:
                        x = data[name]['draw_class'].parts[0].get_xdata()
                        y = data[name]['draw_class'].parts[0].get_ydata()
                        obj = drawobject(type_object='connections')
                        obj.add_part(self.widget_drawing.axes.plot(x, y, alpha=1, color='k')[0])
                        self.components[name] = {'draw_class': obj}
                        self.add_new_item_Qtree('connections', name)

                self.widget_drawing.draw()

    def options_connections(self):
        if self.radioButton_toml_available.isChecked():

            dirctory_flowchem = get_package_directory('flowchem')[:-12]

            option = QFileDialog.Options()
            option |= QFileDialog.DontUseNativeDialog
            name = QFileDialog.getOpenFileName(self, "Load flowchem (toml) file", dirctory_flowchem, "toml Files (*.toml)",
                                               options=option)
            if name[0]:
                self.devices_flowchem.read_toml_file(name[0])
            else:
                return

        elif self.radioButton_toml_not_available.isChecked():

            self.devices_flowchem.devices = self.devices_flowchem.all_devices_available


        self.treeWidget_add_devices.build_qtree(self.devices_flowchem.devices)

        self.treeWidget_add_devices.type = 'devices'

        self.treeWidget_add_devices.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = app.screens()[0]
    window = main_widget()
    window.show()
    sys.exit(app.exec_())