from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class CustomMessageBox(QDialog):
    def __init__(self, parent=None, name=''):
        super().__init__(parent)
        self.setWindowTitle("Component details")

        # Create layout
        layout = QVBoxLayout(self)

        # Create label
        self.label = QLabel("Confirm the name:")
        layout.addWidget(self.label)

        # Create QLineEdit
        self.line_edit = QLineEdit(self)
        layout.addWidget(self.line_edit)
        self.line_edit.setText(name)

        # Create buttons
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")

        # Connect buttons
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

    def get_input(self):
        return self.line_edit.text()