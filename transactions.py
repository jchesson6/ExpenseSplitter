from PyQt5.QtWidgets import (QWidget, QTableWidget, QTableWidgetItem, QGridLayout, QHeaderView, QVBoxLayout, QPushButton, QListWidget, 
                             QLabel, QLineEdit, QMainWindow, QScrollArea, QTextEdit, QAbstractItemView, QComboBox, QDoubleSpinBox , QHBoxLayout,
                             QSizePolicy
)
from PyQt5.QtGui import QWindow
from PyQt5.QtCore import Qt
import classes

class NewTransactionWindow(QWidget):
    def __init__(self, originalwindow):
        super().__init__()
        self.originalwindow = originalwindow
        self.resize(1000, 600)
        self.setWindowTitle("Add a New Transaction to " + originalwindow.transEvent.name)
        self.tlayout = QVBoxLayout()
        namelabel = QLabel("Enter Transaction name")
        self.transnamefield = QLineEdit()
        desclabel = QLabel("Enter a description for transaction")
        self.description = QTextEdit()
        self.description.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.savebutton = QPushButton("Save")
        self.savebutton.clicked.connect(self.saveTransaction)

        self.num_payers = 1
        self.num_debtors = 1
        self.payersel = QComboBox()
        self.payeramt = QDoubleSpinBox()
        self.debtorsel = QComboBox()
        self.debtoramt = QDoubleSpinBox()

        self.num_payers = 1
        self.num_debtors = 1

        for person in originalwindow.transEvent.people:
            self.payersel.addItem(person.name)
            self.debtorsel.addItem(person.name)

        self.payerlabel = QLabel("Payers:")
        self.payercontainer = QWidget()
        self.payercontainer.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.payerbutcont = QWidget()
        self.paycontlayout = QVBoxLayout()
        self.blayoutp = QHBoxLayout()
        self.blayoutp.addWidget(self.payersel)
        self.blayoutp.addWidget(self.payeramt)
        self.payerbutcont.setLayout(self.blayoutp)
        self.paycontlayout.addWidget(self.payerbutcont)
        self.payercontainer.setLayout(self.paycontlayout)

        self.debtorlabel = QLabel("Debtors:")
        self.debtorcontainer = QWidget()
        self.debtorcontainer.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.debtorbutcont = QWidget()
        self.debtorcontlayout = QVBoxLayout()
        self.blayoutd = QHBoxLayout()
        self.blayoutd.addWidget(self.debtorsel)
        self.blayoutd.addWidget(self.debtoramt)
        self.debtorbutcont.setLayout(self.blayoutd)
        self.debtorcontlayout.addWidget(self.debtorbutcont)
        self.debtorcontainer.setLayout(self.debtorcontlayout)
        
        self.newpayerbutton = QPushButton("Add a New Payer")
        self.newpayerbutton.clicked.connect(self.add_payer)
        self.newdebtorbutton = QPushButton("Add a New Debtor")
        self.newdebtorbutton.clicked.connect(self.add_debtor)

        self.tlayout.addWidget(namelabel)
        self.tlayout.addWidget(self.transnamefield)
        self.tlayout.addWidget(desclabel)
        self.tlayout.addWidget(self.description)
        self.tlayout.addWidget(self.payerlabel)
        self.tlayout.addWidget(self.payercontainer)
        self.tlayout.addWidget(self.newpayerbutton)
        self.tlayout.addWidget(self.debtorlabel)
        self.tlayout.addWidget(self.debtorcontainer)
        self.tlayout.addWidget(self.newdebtorbutton)
        self.tlayout.addWidget(self.savebutton)

        self.setLayout(self.tlayout)


    def add_payer(self):
        payersel = QComboBox()
        payeramt = QDoubleSpinBox()
        delbutton = QPushButton("Delete")
        delbutton.setFixedSize(100, 50)
        delbutton.clicked.connect(lambda: self.remove_payer(self.num_payers - 1))
        blayout = QHBoxLayout()
        cont = QWidget()
        blayout.addWidget(payersel)
        blayout.addWidget(payeramt)
        blayout.addWidget(delbutton)
        cont.setLayout(blayout)
        self.num_payers += 1
        self.paycontlayout.insertWidget(len(self.paycontlayout), cont)
        

    def remove_payer(self, payernum):
        self.num_payers -= 1
        self.paycontlayout.takeAt(payernum)


    def add_debtor(self):
        debtorsel = QComboBox()
        debtoramt = QDoubleSpinBox()
        delbutton = QPushButton("Delete")
        delbutton.setFixedSize(100, 50)
        delbutton.clicked.connect(lambda: self.remove_debtor(self.num_debtors - 1))
        blayout = QHBoxLayout()
        cont = QWidget()
        blayout.addWidget(debtorsel)
        blayout.addWidget(debtoramt)
        blayout.addWidget(delbutton)
        cont.setLayout(blayout)
        self.num_debtors += 1
        self.debtorcontlayout.insertWidget(len(self.debtorcontlayout), cont)

    def remove_debtor(self, debtornum):
        self.num_debtors -= 1
        self.debtorcontlayout.takeAt(debtornum)

    def saveTransaction(self):
        transaction = classes.Transaction(self.transnamefield.text(), self.description.toPlainText())
        print(transaction.debtors)
        self.originalwindow.addTransaction(transaction)
        self.close()


class TransactionMenu(QWidget):
    def __init__(self, originalwindow, transaction):
        super().__init__()
        self.originalwindow = originalwindow
        self.resize(800, 500)
        self.setWindowTitle(transaction.name + " Menu")
        self.transaction = transaction

        self.tlayout = QVBoxLayout()

        #TODO: add the transaction information so it can be viewed on this menu
        self.nameLabel = QLabel("Name: " + self.transaction.name)
        self.descLabel = QLabel("Description: " + self.transaction.description)
        self.debtorsTable = QTableWidget(len(self.transaction.debtors), 2)

        self.debtorsTable.setHorizontalHeaderLabels(["Debtor", "Ammount"])
        self.debtorsTable.horizontalHeader().setStretchLastSection(True)
        self.debtorsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for i in range(len(self.transaction.debtors)):
            self.debtorsTable.setItem(i, 0, QTableWidgetItem(self.transaction.debtors[i][0]))
            self.debtorsTable.setItem(i, 1, QTableWidgetItem(str(self.transaction.debtors[i][1])))

        self.debtorsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.setaspaidbutton = QPushButton("Mark As Paid")
        self.setaspaidbutton.clicked.connect(lambda: (
            self.originalwindow.markTransactionAsPaid(self.transaction)
        ))

        self.editeventbutton = QPushButton("Edit Transaction")
        self.editeventbutton.clicked.connect(self.edit_transaction)
        self.deleventbutton = QPushButton("Delete Transaction")
        self.deleventbutton.clicked.connect(self.remove_transaction)

        self.tlayout.addWidget(self.nameLabel)
        self.tlayout.addWidget(self.descLabel)
        self.tlayout.addWidget(self.debtorsTable)
        self.tlayout.addWidget(self.setaspaidbutton)
        self.tlayout.addWidget(self.editeventbutton)
        self.tlayout.addWidget(self.deleventbutton)
        self.setLayout(self.tlayout)


    def edit_transaction(self):
        self.originalwindow.editTransaction(self.transaction)
        self.close()


    def remove_transaction(self):
        self.originalwindow.removeTransaction(self.transaction)
        self.close()


class EditTransactionWindow(QWidget):
    def __init__(self, originalWindow, transaction):
        super().__init__()
        self.originalWindow = originalWindow
        self.transaction = transaction
        self.initGui()

    def initGui(self):
        self.nameLabel = QLabel("Name: ")
        self.nameLineEdit = QLineEdit(self.transaction.name)
        self.descLabel = QLabel("Description: ")
        self.descLineEdit = QLineEdit(self.transaction.description)
        self.debtorsLabel = QLabel("Debtors: ")
        self.addDebtorButton = QPushButton("Add Debtor")
        self.addDebtorButton.clicked.connect(lambda:
            self.debtorsTable.insertRow(self.debtorsTable.rowCount())
        )
        self.debtorsTable = QTableWidget(len(self.transaction.debtors), 2)
        self.debtorsTable.horizontalHeader().setStretchLastSection(True)
        self.debtorsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.debtorsTable.setHorizontalHeaderLabels(["Debtor", "Ammount"])
        self.debtorsTable.setEditTriggers(QTableWidget.AllEditTriggers)
        self.submitButton = QPushButton("Submit")
        self.submitButton.clicked.connect(lambda: self.originalWindow.submitTransactionEdit(self.transaction))

        self.tlayout = QVBoxLayout()
        gridLayout = QGridLayout()

        gridLayout.addWidget(self.nameLabel, 0, 0)
        gridLayout.addWidget(self.nameLineEdit, 0, 1)
        gridLayout.addWidget(self.descLabel, 1, 0)
        gridLayout.addWidget(self.descLineEdit, 1, 1)

        self.tlayout.addLayout(gridLayout)
        self.tlayout.addWidget(self.debtorsLabel)
        self.tlayout.addWidget(self.addDebtorButton)
        self.tlayout.addWidget(self.debtorsTable)
        self.tlayout.addWidget(self.submitButton)

        self.setLayout(self.tlayout)

        for i in range(len(self.transaction.debtors)):
            self.debtorsTable.setItem(i, 0, QTableWidgetItem(self.transaction.debtors[i][0]))
            self.debtorsTable.setItem(i, 1, QTableWidgetItem(str(self.transaction.debtors[i][1])))
