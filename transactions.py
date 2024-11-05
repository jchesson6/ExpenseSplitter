from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QLabel, QLineEdit, QMainWindow, QScrollArea, QTextEdit
from PyQt5.QtGui import QWindow
from PyQt5.QtCore import Qt
import classes

class NewTransactionWindow(QWidget):
    def __init__(self, originalwindow):
        super().__init__()
        self.originalwindow = originalwindow
        self.resize(800, 500)
        self.setWindowTitle("Add a New Transaction to " + originalwindow.transEvent.name)
        layout = QVBoxLayout()
        namelabel = QLabel("Enter Transaction name")
        self.transnamefield = QLineEdit()
        desclabel = QLabel("Enter a description for transaction")
        self.description = QTextEdit()
        self.savebutton = QPushButton("Save")
        self.savebutton.clicked.connect(self.saveTransaction)

        layout.addWidget(namelabel)
        layout.addWidget(self.transnamefield)
        layout.addWidget(desclabel)
        layout.addWidget(self.description)
        layout.addWidget(self.savebutton)

        self.setLayout(layout)


    def saveTransaction(self):
        transaction = classes.Transaction(self.transnamefield.text(), self.description.toPlainText())
        self.originalwindow.addTransaction(transaction)
        self.close()


class TransactionMenu(QWidget):
    def __init__(self, originalwindow, transaction):
        super().__init__()
        self.originalwindow = originalwindow
        self.resize(800, 500)
        self.setWindowTitle(transaction.name + " Menu")
        self.transaction = transaction

        layout = QVBoxLayout()

        #TODO: add the transaction information so it can be viewed on this menu

        self.editeventbutton = QPushButton("Edit Transaction")
        self.deleventbutton = QPushButton("Delete Transaction")
        self.deleventbutton.clicked.connect(self.remove_transaction)

        layout.addWidget(self.editeventbutton)
        layout.addWidget(self.deleventbutton)
        self.setLayout(layout)

    def remove_transaction(self):
        self.originalwindow.removeTransaction(self.transaction)
        self.close()