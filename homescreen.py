from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView

# Create and return a QWidget that represents the home screen
# TODO: Fill out transaction table
class HomeScreen(QWidget):
    
    def __init__(self):
        super().__init__()
        self.init_gui()

    def init_gui(self):
        self.wlayout = QVBoxLayout()
        self.transactionTable = QTableWidget()
        self.transactionTable.setRowCount(1)
        self.transactionTable.setColumnCount(2)
        self.transactionTable.setItem(0, 0, QTableWidgetItem("Name"))
        self.transactionTable.setItem(0, 1, QTableWidgetItem("Amount Owed"))
        self.transactionTable.horizontalHeader().setVisible(False)
        self.transactionTable.verticalHeader().setVisible(False)
        self.transactionTable.horizontalHeader().setStretchLastSection(True)
        self.transactionTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.wlayout.addWidget(self.transactionTable)
        self.setLayout(self.wlayout)