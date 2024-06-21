from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import sys
import os
import tomllib
import pickle

from flowchemdraw.utils.manage_class import import_class, get_package_directory
from flowchemdraw.manage import manage, component
from flowchemdraw.utils.constantes import *

class main_widget(QMainWindow):

    def __init__(self):
        super().__init__()

        loadUi(ADRESS + "/drawgui/flowchem_draw.ui", self)

        self.setWindowTitle("Flowchem plugin - Drawing platform system")

        self.setWindowIcon(QtGui.QIcon(ADRESS + '/figures/icon_window.png'))

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
        for fig in COMPONENTS_NONELETRONIC:
            ilustratio_tree[fig] = None

        self.treeWidget_add_others.build_qtree(ilustratio_tree)

        self.treeWidget_add_others.Main_Window = self

        self.treeWidget_add_devices.Main_Window = self

        self.textBrowser.MainWindow = self

        self.treeWidget_add_devices.type = 'devices'

    def save(self):
        if not self.manage.components:
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
                pickle.dump(self.manage, f)

    def load(self):


        option = QFileDialog.Options()
        option |= QFileDialog.DontUseNativeDialog
        name = QFileDialog.getOpenFileName(self, "Load the project", " ", "pickle Files (*.p)",
                                           options=option)
        if name[0]:

            if self.manage.components:
                qm = QMessageBox()
                ret = qm.question(self, '', "Are you sure you want to remove the current project in order "
                                            "to load a new one? Please ensure that you save it before doing so if you "
                                            "want to keep it.?", qm.Yes | qm.No)
                if ret == qm.Yes:
                    iterator = QTreeWidgetItemIterator(self.treeWidget_device)
                    while iterator.value():
                        self.treeWidget_device.setCurrentItem(iterator.value())
                        self.treeWidget_device.remove_item_p1()
                        iterator += 1
                else:
                    return

            with open(name[0], 'rb') as f:
                data = pickle.load(f)

                for item in data.components.values():

                    figure_draw = item.class_name

                    if item.class_name in DRAW_DEVICES_CORRESPONDENT.keys():

                        figure_draw = DRAW_DEVICES_CORRESPONDENT[item.class_name]

                    dev = import_class('flowchemdraw.figures', figure_draw)

                    self.manage.components[item.name] = component(name=item.name,
                                                             class_name=item.class_name,
                                                              position=item.position,
                                                              draw=dev(self.widget_drawing.axes,
                                                                       pos=item.position, name=item.name))

                    self.treeWidget_device.add_new_item_Qtree(self.manage.components[item.name].draw.type_object,
                                                                          item.name)

                for item in data.connection.values():

                    X = item.draw.parts[0].get_xdata()

                    Y = item.draw.parts[0].get_ydata()

                    name = self.manage._add_connection(origin=item.origin, destiny=item.destiny, X=X, Y=Y)

                    self.treeWidget_device.add_new_item_Qtree('connections', name)

                self.widget_drawing.draw()

    def options_connections(self):
        if self.radioButton_toml_available.isChecked():

            dirctory_flowchem = get_package_directory('flowchem')[:-12]

            option = QFileDialog.Options()
            option |= QFileDialog.DontUseNativeDialog
            name = QFileDialog.getOpenFileName(self, "Load flowchem (toml) file", dirctory_flowchem, "toml Files (*.toml)",
                                               options=option)
            if name[0]:

                with open(name[0], "rb") as f:
                    data = tomllib.load(f)

                devices = dict(); devices_name = dict()
                for name in data['device']:
                    type = data['device'][name]['type']
                    if type in CLASS_DEVICE_AVAILABLE_FLOWCHEM.keys():
                        devices[type] = CLASS_COMPONENT_DEVICE_AVAILABLE_FLOWCHEM[type]
                        devices_name[type] = name
                    else:
                        logger.error(f'Device {type} is not found in the flowchem!')

                self.treeWidget_add_devices.setEnabled(False)

                for key in devices:
                    if devices[key]['components'] != None:
                        for comp in devices[key]['components'].keys():
                            class_name = key+'/'+comp
                            name = devices_name[key]+'/'+comp
                            self.manage._add_devices_auto(class_name, name, configuration_file=data['device'][devices_name[key]])
                            self.treeWidget_device.add_new_item_Qtree('devices', name)
                    else:
                        self.manage._add_devices_auto(key, devices_name[key], configuration_file=data['device'][devices_name[key]])
                        self.treeWidget_device.add_new_item_Qtree('devices', devices_name[key])

                self.widget_drawing.draw()

                self.textBrowser.write_toml_file(self.manage.components)

            else:
                return

        elif self.radioButton_toml_not_available.isChecked():

            self.treeWidget_add_devices.setEnabled(True)

            devices = CLASS_COMPONENT_DEVICE_AVAILABLE_FLOWCHEM

        self.treeWidget_add_devices.build_qtree(devices)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = app.screens()[0]
    window = main_widget()
    window.show()
    sys.exit(app.exec_())
