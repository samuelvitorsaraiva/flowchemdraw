from flowchemdraw.utils.constantes import *
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5 import QtGui

class CustomMessageBox(QDialog):
    def __init__(self, parent=None, name='', class_name='', configuration_file=None, type='device'):
        super().__init__(parent)
        self.setWindowTitle("Component details")

        self.setWindowIcon(QtGui.QIcon(ADRESS + '/figures/Icons/icon_window.png'))

        # Create layout
        layout = QVBoxLayout(self)

        # Create label
        self.label = QLabel("Confirm the name:")
        layout.addWidget(self.label)

        # Create QLineEdit
        self.line_edit = QLineEdit(self)
        layout.addWidget(self.line_edit)
        self.line_edit.setText(name)

        if type=='device':
            self.line_edit.setEnabled(False)
            if configuration_file == None:
                configuration_file = CONFIGURATION_FILE_COMPLETE
                self.line_edit.setEnabled(True)
                self.class_name = class_name
            else:
                self.class_name = configuration_file['device'][name.split('/')[0]]['type']

            self.new_line_edits = []; self.new_line_labels = [];

            if class_name in configuration_file['device'].keys():
                for key, value in configuration_file['device'][class_name].items():
                    self.new_line_labels.append(QLabel(f'Confirm the {key}:'))
                    layout.addWidget(self.new_line_labels[-1])
                    self.new_line_edits.append(QLineEdit(self))
                    layout.addWidget(self.new_line_edits[-1])
                    self.new_line_edits[-1].setText(str(value))


        # Create buttons
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")

        # Connect buttons
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

        self.configuration_file_adress: str | None = None

    def get_input_device(self):

        answer = {'type': self.class_name}

        for i in range(len(self.new_line_edits)):
            key = self.new_line_labels[i].text()[12:-1]
            try:
                value = int(self.new_line_edits[i].text())
            except:
                value = self.new_line_edits[i].text()

            answer[key] = value

        return [self.line_edit.text(), answer]

    def get_input_utensils(self):
        return self.line_edit.text()



