import time

from PyQt5.QtWidgets import QTextBrowser, QMenu
from PyQt5.QtCore import Qt
from flowchemdraw.manage.manage import manage
from flowchemdraw.utils.constantes import *
import tomllib

class textbrowser_tolm(QTextBrowser):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.Edit_Setting_Window = None

        self.configuration_file_adress: str | None = None

        self.content: str = ''

        self.MainWindow = None

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            ...
        elif event.button() == Qt.RightButton:
            ...

        super(textbrowser_tolm, self).mousePressEvent(event)


    def write_toml_file(self, mc: dict()):

        text = str()
        components = []
        for comp in mc.values():
            if comp.draw.type_object == 'others':
                continue
            if not comp.class_name_device in CLASS_DEVICE_AVAILABLE_FLOWCHEM.keys() or comp.name_device in components:
                continue

            text += f'[device.{comp.name_device}]\n'
            dic_arg = comp.configuration_block['device'][comp.name_device]
            for key in dic_arg.keys():
                if isinstance(dic_arg[key], str):
                    text += f'{key} = "{dic_arg[key]}"\n'
                elif dic_arg[key] == None:
                    text += f'{key} = " "\n'
                else:
                    text += f'{key} = {dic_arg[key]}\n'
            text += '\n'

            components.append(comp.name_device)

        self.content = text
        self.setPlainText(self.content)
        self.write_temporary_file()


    def write_temporary_file(self):

        with open('../components/temporary.toml', 'w') as file:
            file.write(self.content)

        time.sleep(0.5)


    def edit_configuration_file(self):

        with open('../components/temporary.toml', "rb") as f:
            data = tomllib.load(f)

        for key in data['device']:
            self.MainWindow.manage.components[key].update_configuration_file(data['device'][key])

