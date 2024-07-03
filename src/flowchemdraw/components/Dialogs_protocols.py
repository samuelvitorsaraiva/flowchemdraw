from flowchemdraw.utils.constantes import *
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5 import QtGui

class setup_protocol(QDialog):
    def __init__(self, parent=None, configuration: dict={}):
        super().__init__(parent)
        self.setWindowTitle("Protocol details")

        self.setWindowIcon(QtGui.QIcon(ADRESS + '/figures/Icons/icon_window.png'))

        # Create layout
        layout = QVBoxLayout(self)

        self.new_line_edits = []; self.new_line_labels = []
        for key, value in configuration.items():
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

    def answer(self):
        ans = dict()
        for i in range(len(self.new_line_edits)):
            key = self.new_line_labels[i].text()[12:-1]
            value = self.new_line_edits[i].text()

            ans[key] = value

        return ans

