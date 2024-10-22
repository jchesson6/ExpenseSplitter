from PyQt5.QtWidgets import QApplication, QHeaderView, QTextEdit, QLabel, QLineEdit, QTableWidgetItem, QTableWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QStackedWidget, QListWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
import classes
import sys

class FriendsList(QWidget):
    # IMPORTANT: account is a reference to the main account variable so dont change it here
    def __init__(self, account):
        super().__init__()
        self.initGui(account)

    def initGui(self, account):
        self.account = account
        layout = QVBoxLayout()
        self.table = QTableWidget()

        self.updateList()

        layout.addWidget(self.table)
        self.setLayout(layout)

    # Visually update the list
    # This should be called when the app updates the main account variable
    def updateList(self):
        self.table.clear()
        self.table.setRowCount(len(self.account.friends) + 1)
        self.table.setColumnCount(2)
        self.table.setItem(0, 0, QTableWidgetItem("Name"))
        self.table.setItem(0, 1, QTableWidgetItem("Total Ammount Owed"))
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for i in range(len(self.account.friends)):
            self.table.setItem(i + 1, 0, QTableWidgetItem(self.account.friends[i].name))
            self.table.setItem(i + 1, 1, QTableWidgetItem(str(self.account.friends[i].amount_owed_by_user)))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWindow = QMainWindow()

    account = classes.Account("name")
    friend1 = classes.Friend("friend1")
    friend1.amount_owed_by_user = 0.0
    account.add_friend(friend1)

    friendsList = FriendsList(account)

    friend2 = classes.Friend("friend2")
    friend2.amount_owed_by_user = 0.0
    account.add_friend(friend2)

    friendsList.updateList()

    mainWindow.setCentralWidget(friendsList)
    mainWindow.show()

    sys.exit(app.exec_())
