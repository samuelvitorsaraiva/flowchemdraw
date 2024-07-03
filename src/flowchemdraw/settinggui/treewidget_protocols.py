import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QLineEdit, QAbstractItemView
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from flowchemdraw.utils.constantes import ADRESS


class treewidget_protocols(QTreeWidget):
    def __init__(self, parent=None):

        super().__init__(parent)

        # Set the number of columns and headers
        self.setColumnCount(1)
        self.setHeaderLabels(["Protocols"])

        self.Main_Window = None

    def update_protocols(self):

        self.clear()

        stage = []

        for key, values in self.Main_Window.manage_protocol.commands.items():
            stage.append(QTreeWidgetItem(self, [key]))
            for key, order in values.items():
                description = f"{key} {order['component'].name}: {order['command']}"
                QTreeWidgetItem(stage[-1], [description])


            # Connecting signals
            self.itemClicked.connect(self.on_item_clicked)

    def on_item_clicked(self, item, column):

        name = item.text(column)

        if name in self.Main_Window.manage_protocol.commands.keys():

            self.Main_Window.tableWidget._update_stage(name)

        else:

            stage = item.parent().text(column)

            self.Main_Window.tableWidget._update_command(stage, name)

            self.Main_Window.manage_protocol.actived_protocol(stage, name)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create QTreeWidget
        self.tree_widget = QTreeWidget()
        self.setCentralWidget(self.tree_widget)

        # Set the number of columns and headers
        self.tree_widget.setColumnCount(2)
        self.tree_widget.setHeaderLabels(["Column 1", "Column 2"])

        # Populate the tree with items
        root = QTreeWidgetItem(self.tree_widget, ["Root", "Root Data"])
        child1 = QTreeWidgetItem(root, ["Child 1", "Child 1 Data"])
        child2 = QTreeWidgetItem(root, ["Child 2", "Child 2 Data"])
        subchild1 = QTreeWidgetItem(child1, ["Subchild 1", "Subchild 1 Data"])

        # Adding icons to items
        root.setIcon(0, QIcon(ADRESS + "/figures/Icons/alert.jpg"))
        child1.setIcon(0, QIcon(ADRESS + "/figures/Icons/alert.jpg"))
        child2.setIcon(0, QIcon(ADRESS + "/figures/Icons/alert.jpg"))
        subchild1.setIcon(0, QIcon(ADRESS + "/figures/Icons/alert.jpg"))

        # Adding tooltips to items
        child1.setToolTip(0, "This is Child 1")
        subchild1.setToolTip(1, "This is Subchild 1 Data")

        # Making an item non-editable
        child1.setFlags(child1.flags() & ~Qt.ItemIsEditable)

        # Customizing headers
        self.tree_widget.header().setDefaultSectionSize(150)
        self.tree_widget.header().setStretchLastSection(True)

        # Expanding and collapsing items
        root.setExpanded(True)
        child1.setExpanded(False)

        # Adding a custom widget to an item
        line_edit = QLineEdit("Editable")
        self.tree_widget.setItemWidget(child1, 1, line_edit)

        # Adding a checkbox to an item
        child1.setCheckState(0, Qt.Checked)

        # Enabling alternating row colors
        self.tree_widget.setAlternatingRowColors(True)

        # Enabling sorting
        self.tree_widget.setSortingEnabled(True)

        # Enabling drag and drop
        self.tree_widget.setDragDropMode(QAbstractItemView.InternalMove)

        # Connecting signals
        self.tree_widget.itemClicked.connect(self.on_item_clicked)
        self.tree_widget.itemChanged.connect(self.on_item_changed)

        # Set window properties
        self.setWindowTitle("QTreeWidget Example")
        self.setGeometry(300, 300, 600, 400)

    def on_item_clicked(self, item, column):
        print(f"Item '{item.text(column)}' in column {column} clicked")

    def on_item_changed(self, item, column):
        print(f"Item '{item.text(column)}' in column {column} changed")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())



