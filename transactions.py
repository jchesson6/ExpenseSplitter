"""
transactions.py

This file contains all functionalitty for interaction with transactions
"""

from PyQt5.QtWidgets import (QWidget, QTableWidget, QTableWidgetItem, QGridLayout, QHeaderView, QVBoxLayout, QPushButton, QListWidget,
                             QLabel, QLineEdit, QMainWindow, QScrollArea, QTextEdit, QAbstractItemView, QComboBox, QHBoxLayout,
                             QSizePolicy, QMessageBox
)
from PyQt5.QtGui import QWindow, QDoubleValidator
from PyQt5.QtCore import Qt
import classes


class NewTransactionWindow(QWidget):
    """
    Window to create a new transaction in an event
    """
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
        self.setequalbutton = QPushButton("Split Equally Amongst Everyone")
        self.setequalbutton.setCheckable(True)
        self.setequalbutton.clicked.connect(self.set_equal_split)
        self.savebutton = QPushButton("Save")
        self.savebutton.clicked.connect(self.saveTransaction)

        # Create empty deptor and payer widgets 
        self.validator = QDoubleValidator()
        self.num_payers = 1
        self.num_debtors = 1
        self.payersel = QComboBox()
        self.payeramt = QLineEdit()
        self.payeramt.setValidator(self.validator)
        self.payeramt.setPlaceholderText("00.00")
        self.debtorsel = QComboBox()
        self.debtoramt = QLineEdit()
        self.debtoramt.setValidator(self.validator)
        self.debtoramt.setPlaceholderText("00.00")
        self.num_payers = 1
        self.num_debtors = 1

        # add user to list of payers and debtors
        self.payersel.addItem(originalwindow.originalwindow.originalwindow.account.displayName.strip())
        self.debtorsel.addItem(originalwindow.originalwindow.originalwindow.account.displayName.strip())

        # add friends on event to transaction list
        for person in originalwindow.transEvent.people:
            self.payersel.addItem(person.name.strip())
            self.debtorsel.addItem(person.name.strip())

        # Create list of payers
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

        # Create list of debtors
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

        # Buttons to add debtors and payers
        self.newpayerbutton = QPushButton("Add a New Payer")
        self.newpayerbutton.clicked.connect(self.add_payer)
        self.newdebtorbutton = QPushButton("Add a New Debtor")
        self.newdebtorbutton.clicked.connect(self.add_debtor)

        # Create window layout
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
        self.tlayout.addWidget(self.setequalbutton)
        self.tlayout.addWidget(self.savebutton)

        self.setLayout(self.tlayout)

    def add_payer(self):
        """
        Add a payer to the transaction
        """
        if self.num_debtors + self.num_payers == self.originalwindow.transEvent.num_people:
            QMessageBox.critical(self, "Error", "Number of people on transaction cannot exceed the number of people on the event", buttons=QMessageBox.Ok)
            return

        payersel = QComboBox()
        payersel.addItem(self.originalwindow.originalwindow.originalwindow.account.displayName)
        for person in self.originalwindow.transEvent.people:
            payersel.addItem(person.name.strip())
        payeramt = QLineEdit()
        payeramt.textChanged.connect(self.set_equal_split)
        payeramt.setValidator(self.validator)
        payeramt.setPlaceholderText("00.00")

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
        self.set_equal_split()
        
    def remove_payer(self, payernum):
        """
        Remove a payer
        """
        self.num_payers -= 1
        self.paycontlayout.takeAt(payernum)
        self.set_equal_split()

    def add_debtor(self):
        """
        Add a debtor to the transaction
        """
        if self.num_debtors + self.num_payers == self.originalwindow.transEvent.num_people:
            QMessageBox.critical(self, "Error", "Number of people on transaction cannot exceed the number of people on the event", buttons=QMessageBox.Ok)
            return

        debtorsel = QComboBox()
        debtorsel.addItem(self.originalwindow.originalwindow.originalwindow.account.displayName)
        for person in self.originalwindow.transEvent.people:
            debtorsel.addItem(person.name.strip())
        debtoramt = QLineEdit()
        debtoramt.setValidator(self.validator)
        debtoramt.setPlaceholderText("00.00")
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
        self.set_equal_split()

    def remove_debtor(self, debtornum):
        """
        Remove a debtor
        """
        self.num_debtors -= 1
        self.debtorcontlayout.takeAt(debtornum)
        self.set_equal_split()

    def set_equal_split(self):

        if self.setequalbutton.isChecked():

            # loop through payer field items
            paywidgets = (self.paycontlayout.itemAt(i) for i in range(self.paycontlayout.count()))
            debwidgets = (self.debtorcontlayout.itemAt(i) for i in range(self.debtorcontlayout.count()))
            num_split = self.paycontlayout.count() + self.debtorcontlayout.count()
            totalpaid = 0.0

            for item in paywidgets:
                widget = item.widget()
        
                for lineedit in widget.findChildren(QLineEdit):
                    if lineedit.text():
                        amt = float(lineedit.text())
                        totalpaid += amt
            
            amtperperson = totalpaid / num_split

            for item in debwidgets:     
                widget = item.widget()      
                
                for lineedit in widget.findChildren(QLineEdit):
                    lineedit.setText(str(amtperperson))


    def saveTransaction(self):
        """
        Save the transaction in the parent event
        """
        transaction = classes.Transaction(self.transnamefield.text(), self.description.toPlainText())

        # loop through payer field items
        paywidgets = (self.paycontlayout.itemAt(i) for i in range(self.paycontlayout.count()))
        debwidgets = (self.debtorcontlayout.itemAt(i) for i in range(self.debtorcontlayout.count()))

        # Get all payer widgets and extract data
        for item in paywidgets:
            widget = item.widget()
            payer = ""
            amt = 0
            for combobox in widget.findChildren(QComboBox):
                payer = combobox.currentText()
            for lineedit in widget.findChildren(QLineEdit):
                if lineedit.text() != "":
                    amt = float(lineedit.text())
                else:
                    QMessageBox.critical(self, "No Value", "Enter a value for the payer before saving", buttons=QMessageBox.Ok)
                    return
            transaction.add_payer(payer, amt)

        # Get all debtor widgets and extract data
        for item in debwidgets:
            widget = item.widget()
            debtor = ""
            amt = 0
            for combobox in widget.findChildren(QComboBox):
                debtor = combobox.currentText()
            for lineedit in widget.findChildren(QLineEdit):
                if lineedit.text() != "":
                    amt = float(lineedit.text())
                else:
                    QMessageBox.critical(self, "No Value", "Enter a value for the debtor before saving", buttons=QMessageBox.Ok)
                    return
            transaction.add_debtor(debtor,amt)

        #check if any duplicate names and warn user
        #check if any payers are in the debtors and warn user
        for payer in transaction.payers:
            for debtor in transaction.debtors:
                if payer == debtor:
                    QMessageBox.critical(self, "Name in both fields",payer + " is listed as both a payer and debtor", buttons=QMessageBox.Ok)
                    return
        
        print(transaction)
        self.originalwindow.addTransaction(transaction)
        self.close()

    # def load_transaction(self, transaction):


class TransactionMenu(QWidget):
    """
    The menu that shows when a transaction is viewed
    """
    def __init__(self, originalwindow, transaction):
        """
        Initialize widgets and transaction info
        """
        super().__init__()
        self.originalwindow = originalwindow
        self.resize(800, 800)
        self.setWindowTitle(transaction.name + " Menu")
        self.transaction = transaction

        self.tlayout = QVBoxLayout()

        self.nameLabel = QLabel("Name: " + self.transaction.name)
        self.descLabel = QLabel("Description: " + self.transaction.description)
        self.debtorsTable = QTableWidget(len(self.transaction.debtors), 2)

        # Populate payers list
        payerlabel = QLabel("Payer(s):")
        payerlist = []
        for payer in transaction.payers:
            label = QLabel(payer + " paid " + str(transaction.payers[payer]))
            payerlist.append(label)

        self.debtorsTable.setHorizontalHeaderLabels(["Debtor", "Owes"])
        self.debtorsTable.horizontalHeader().setStretchLastSection(True)
        self.debtorsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Populate debtors table
        i = 0
        for debtor in transaction.debtors:
            self.debtorsTable.setItem(i, 0, QTableWidgetItem(debtor))
            self.debtorsTable.setItem(i, 1, QTableWidgetItem(str(self.transaction.debtors[debtor])))
            i += 1

        self.debtorsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Create edit and delete buttons
        self.editeventbutton = QPushButton("Edit Transaction")
        self.editeventbutton.clicked.connect(self.edit_transaction)
        self.deleventbutton = QPushButton("Delete Transaction")
        self.deleventbutton.clicked.connect(self.remove_transaction)

        # Set layout
        self.tlayout.addWidget(self.nameLabel)
        self.tlayout.addWidget(self.descLabel)
        self.tlayout.addWidget(payerlabel)
        for label in payerlist:
            self.tlayout.addWidget(label)
        self.tlayout.addWidget(self.debtorsTable)
        self.tlayout.addWidget(self.editeventbutton)
        self.tlayout.addWidget(self.deleventbutton)
        self.setLayout(self.tlayout)

    def edit_transaction(self):
        """
        Edit the transaction
        """
        self.originalwindow.editTransaction(self.transaction)
        self.close()

    def remove_transaction(self):
        """
        Delete the transaction
        """
        self.originalwindow.removeTransaction(self.transaction)
        self.close()


class EditTransactionWindow(QWidget):
    """
    Window to edit transaction details
    """
    def __init__(self, originalWindow, transaction):
        """
        Set the parent window the create the gui
        """
        super().__init__()
        self.originalwindow = originalWindow
        self.transaction = transaction
        self.initGui()

    def initGui(self):
        """
        Create a window similar to the new transaction window but will details filled out
        """
        self.resize(1000, 600)
        self.setWindowTitle("Edit Transaction")
        self.tlayout = QVBoxLayout()
        namelabel = QLabel("Enter Transaction name")
        self.transnamefield = QLineEdit(self.transaction.name)
        desclabel = QLabel("Enter a description for transaction")
        self.description = QTextEdit(self.transaction.description)
        self.description.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.savebutton = QPushButton("Save")
        self.savebutton.clicked.connect(self.saveTransaction)

        self.validator = QDoubleValidator()
        self.num_payers = 0
        self.num_debtors = 0

        self.payerlabel = QLabel("Payers:")

        self.payercontainer = QWidget()
        self.payercontainer.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.paycontlayout = QVBoxLayout()
        self.payercontainer.setLayout(self.paycontlayout)

        # Create payer list
        for i, payer in enumerate(self.transaction.payers):
            payersel = QComboBox()
            payersel.addItem(self.originalwindow.originalwindow.originalwindow.account.displayName.strip())
            print(self.originalwindow.transEvent.people)
            for j, person in enumerate(self.originalwindow.transEvent.people):
                payersel.addItem(person.name.strip())
                if payer.strip() == person.name.strip():
                    payersel.setCurrentIndex(j + 1)

            payeramt = QLineEdit(str(self.transaction.payers[payer]))
            payeramt.setValidator(self.validator)
            payeramt.setPlaceholderText("00.00")

            delbutton = QPushButton("Delete")
            delbutton.setFixedSize(100, 50)
            delbutton.clicked.connect(lambda: self.remove_payer(i))
            blayout = QHBoxLayout()
            cont = QWidget()
            blayout.addWidget(payersel)
            blayout.addWidget(payeramt)
            blayout.addWidget(delbutton)
            cont.setLayout(blayout)
            self.num_payers += 1
            self.paycontlayout.insertWidget(len(self.paycontlayout), cont)

        self.debtorlabel = QLabel("Debtors:")
        self.debtorcontainer = QWidget()
        self.debtorcontainer.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.debtorcontlayout = QVBoxLayout()
        self.debtorcontainer.setLayout(self.debtorcontlayout)

        # Create debtor list
        for i, debtor in enumerate(self.transaction.debtors): 
            debtorsel = QComboBox()
            debtorsel.addItem(self.originalwindow.originalwindow.originalwindow.account.displayName)
            for j, person in enumerate(self.originalwindow.transEvent.people):
                debtorsel.addItem(person.name.strip())
                if debtor.strip() == person.name.strip():
                    debtorsel.setCurrentIndex(j + 1)
            debtoramt = QLineEdit(str(self.transaction.debtors[debtor]))
            debtoramt.setValidator(self.validator)
            debtoramt.setPlaceholderText("00.00")
            delbutton = QPushButton("Delete")
            delbutton.setFixedSize(100, 50)
            delbutton.clicked.connect(lambda: self.remove_debtor(i))
            blayout = QHBoxLayout()
            cont = QWidget()
            blayout.addWidget(debtorsel)
            blayout.addWidget(debtoramt)
            blayout.addWidget(delbutton)
            cont.setLayout(blayout)
            self.num_debtors += 1
            self.debtorcontlayout.insertWidget(len(self.debtorcontlayout), cont)

        self.newpayerbutton = QPushButton("Add a New Payer")
        self.newpayerbutton.clicked.connect(self.add_payer)
        self.newdebtorbutton = QPushButton("Add a New Debtor")
        self.newdebtorbutton.clicked.connect(self.add_debtor)

        # Set layout
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

    def saveTransaction(self):
        """
        Delete the old transaction and save the current one
        """
        transaction = classes.Transaction(self.transnamefield.text(), self.description.toPlainText())

        # loop through payer field items
        paywidgets = (self.paycontlayout.itemAt(i) for i in range(self.paycontlayout.count()))
        debwidgets = (self.debtorcontlayout.itemAt(i) for i in range(self.debtorcontlayout.count()))

        # Get all data for payers
        for item in paywidgets:
            widget = item.widget()
            payer = ""
            amt = 0
            for combobox in widget.findChildren(QComboBox):
                payer = combobox.currentText()
            for lineedit in widget.findChildren(QLineEdit):
                if lineedit.text() != "":
                    amt = float(lineedit.text())
                else:
                    QMessageBox.critical(self, "No Value", "Enter a value for the payer before saving", buttons=QMessageBox.Ok)
                    return
            transaction.add_payer(payer, amt)

        # Get all data for debtors
        for item in debwidgets:
            widget = item.widget()
            debtor = ""
            amt = 0
            for combobox in widget.findChildren(QComboBox):
                debtor = combobox.currentText()
            for lineedit in widget.findChildren(QLineEdit):
                if lineedit.text() != "":
                    amt = float(lineedit.text())
                else:
                    QMessageBox.critical(self, "No Value", "Enter a value for the debtor before saving", buttons=QMessageBox.Ok)
                    return
            transaction.add_debtor(debtor,amt)
        
        #check if any payers are in the debtors and warn user
        for payer in transaction.payers:
            for debtor in transaction.debtors:
                if payer == debtor:
                    QMessageBox.critical(self, "Name in both fields",payer + " is listed as both a payer and debtor", buttons=QMessageBox.Ok)
                    return
        
        self.originalwindow.removeTransaction(self.transaction)
        self.originalwindow.addTransaction(transaction)
        self.close()

    def add_payer(self):
        """
        Add a payer to the transaction
        """
        if self.num_debtors + self.num_payers == self.originalwindow.transEvent.num_people:
            QMessageBox.critical(self, "Error", "Number of people on transaction cannot exceed the number of people on the event", buttons=QMessageBox.Ok)
            return
        
        payersel = QComboBox()
        payersel.addItem(self.originalwindow.originalwindow.originalwindow.account.displayName)
        for person in self.originalwindow.transEvent.people:
            payersel.addItem(person.name)
        payeramt = QLineEdit()
        payeramt.setValidator(self.validator)
        payeramt.setPlaceholderText("00.00")

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

    def add_debtor(self):
        """
        Add a debtor to the transaction
        """
        if self.num_debtors + self.num_payers == self.originalwindow.transEvent.num_people:
            QMessageBox.critical(self, "Error", "Number of people on transaction cannot exceed the number of people on the event", buttons=QMessageBox.Ok)
            return

        debtorsel = QComboBox()
        debtorsel.addItem(self.originalwindow.originalwindow.originalwindow.account.displayName)
        for person in self.originalwindow.transEvent.people:
            debtorsel.addItem(person.name)
        debtoramt = QLineEdit()
        debtoramt.setValidator(self.validator)
        debtoramt.setPlaceholderText("00.00")
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
        """
        Remove a debtor
        """
        if debtornum != 0:
            self.num_debtors -= 1
            self.debtorcontlayout.takeAt(debtornum)

    def remove_payer(self, payernum):
        """
        Remove a payer
        """
        if payernum != 0:
            self.num_payers -= 1
            self.paycontlayout.takeAt(payernum)
