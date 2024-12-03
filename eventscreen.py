"""
eventscreen.py

This file contains widgets associated with individual events
"""

from PyQt5.QtWidgets import (QWidget, QGridLayout, QListWidgetItem, QVBoxLayout, QTableWidget,
                             QPushButton, QListWidget, QLabel, QLineEdit, QMessageBox, QScrollArea)
from PyQt5.QtGui import QWindow, QColor
from PyQt5.QtCore import Qt
import classes
import transactions
import split


class EventScreen(QWidget):
    """
    This is the main event screen that displays event details
    """

    curEvent = None
    eventList = []

    def __init__(self, originalwindow):
        """
        Create the screen with a reference to the parent
        """
        super().__init__()
        self.originalwindow = originalwindow
        self.selectedEvent = None
        self.init_gui()

    def init_gui(self):
        """
        Create all of the widgets on the screen
        """
        self.wlayout = QVBoxLayout()
        self.newEventButton = QPushButton("New Event")
        self.newEventButton.clicked.connect(lambda: self.createNewEventWindow(self.originalwindow))

        self.eventtable = QListWidget()

        if len(self.eventList) > 0:
            self.eventtable.insertItems(self.eventList)

        self.eventtable.itemDoubleClicked.connect(self.createEventTransactionsWindow)
        self.eventtable.itemClicked.connect(self.set_selected_event)

        self.calculatebutton = QPushButton("Calculate Event Payments")
        self.markaspaidbutton = QPushButton("Mark as Paid")
        self.markasunpaidbutton = QPushButton("Mark as Unpaid")
        
        self.calculatebutton.clicked.connect(self.calculate_event)
        self.markaspaidbutton.clicked.connect(self.markaspaid)
        self.markasunpaidbutton.clicked.connect(self.markasunpaid)

        self.wlayout.addWidget(self.newEventButton)
        self.wlayout.addWidget(self.eventtable)
        self.wlayout.addWidget(self.calculatebutton)
        self.wlayout.addWidget(self.markaspaidbutton)
        self.wlayout.addWidget(self.markasunpaidbutton)
        self.setLayout(self.wlayout)

    def refreshEventTable(self):
        self.eventtable.clear()
        for event in self.originalwindow.account.events:
            if not self.originalwindow.account.events[event].is_complete:
                item = QListWidgetItem(event)
                item.setBackground(QColor(0xFF0000))
                item.setForeground(QColor(0xFFFFFF))
                self.addEventtoTable(item)
            else:
                item = QListWidgetItem(event)
                item.setBackground(QColor(0x00FF00))
                self.addEventtoTable(item)

    def createNewEventWindow(self, originalwindow):
        """
        Create and show the new event window
        """
        self.newEventWin = NewEventWindow(self, originalwindow.account)
        self.newEventWin.show()

    def createEventTransactionsWindow(self, item):
        """
        Create and show the transactions window for the current event
        """
        selEvent = self.originalwindow.account.events[item.text()]
        self.curRow = self.eventtable.currentRow()
        self.eventTransWin = EventTransactionsWindow(self, selEvent)
        self.eventTransWin.show()

    def saveCurEvent(self, event):
        """
        Save the current event to the account
        """
        self.curEvent = event
        self.originalwindow.account.add_event(event)
        self.originalwindow.account.save()

    def addEventtoTable(self, event):
        """
        Add an event to the table to be displayed
        The default bg is red to mark the event as incomplete
        """
        self.eventtable.addItem(event)
        self.eventtable.update()

    def remove_event(self, event):
        """
        Remove an event from the screen and account
        """
        self.eventtable.takeItem(self.curRow)
        self.eventtable.update()
        self.originalwindow.account.remove_event(event.name)

    def set_selected_event(self, item):
        self.selectedEvent = item.text()

    def calculate_event(self):
        selEvent = self.originalwindow.account.events[self.selectedEvent]    
        
        results = split.calculate_split(selEvent, self.originalwindow.account)
        self.paymentwindow = EventPaymentsWindow(selEvent, results)
        self.paymentwindow.show()
            #selEvent.is_complete = True
            #self.refreshEventTable()
            #print(results)

    def markaspaid(self):
        self.originalwindow.account.events[self.selectedEvent].is_complete = True
        self.refreshEventTable()
        self.originalwindow.account.save()

    def markasunpaid(self):
        self.originalwindow.account.events[self.selectedEvent].is_complete = False
        self.refreshEventTable()
        self.originalwindow.account.save()

class EventPaymentsWindow(QWidget):
    """
    Window that displays the payments that need to be made
    """
    def __init__(self, event, payments):
        """
        Create the window with a reference to the
        parent and create all of the widgets
        """
        super().__init__()
        self.setWindowTitle(event.name + " Payments")
        self.setFixedWidth(1000)
        layout = QVBoxLayout()

        for payer, payment in payments.items():
            for paid in payment:
                label = QLabel(payer + " pays " + paid + " $" + str(payment[paid]))
                layout.addWidget(label)


        self.setLayout(layout)


class EventTransactionsWindow(QWidget):
    """
    Class that shows all of the transaction associated with the
    current event
    """

    def __init__(self, originalwindow, event):
        """
        Create the window with a reference to the
        parent and create all of the widgets
        """
        super().__init__()
        self.transEvent = event
        self.originalwindow = originalwindow
        self.resize(1200, 800)
        self.setWindowTitle(event.name + " Menu")

        layout = QVBoxLayout()

        self.addtransbutton = QPushButton("Add Transaction")
        self.addtransbutton.clicked.connect(self.createNewTransactionWindow)
        self.editeventbutton = QPushButton("Edit Event")
        self.deleventbutton = QPushButton("Delete Event")
        self.deleventbutton.setStyleSheet("background-color : red")
        self.deleventbutton.clicked.connect(self.removeEvent)
        self.transactionlabel = QLabel("Transactions")
        self.transactionlabel.setAlignment(Qt.AlignHCenter)

        self.transactionlist = QListWidget()
        for transaction in self.transEvent.transactions:
            self.transactionlist.addItem(transaction)

        self.transactionlist.itemDoubleClicked.connect(self.createTransactionMenu)

        self.editeventbutton.clicked.connect(self.createEditEventWindow)

        layout.addWidget(self.addtransbutton)
        layout.addWidget(self.editeventbutton)
        layout.addWidget(self.transactionlabel)
        layout.addWidget(self.transactionlist)
        layout.addWidget(self.deleventbutton)

        self.setLayout(layout)

    def createEditEventWindow(self):
        """
        Create a window to edit the current event
        """
        self.editEventWindow = EditEventWindow(self)
        self.editEventWindow.show()

    def removeEvent(self):
        """
        Function to remove the current event from the list
        """
        self.originalwindow.remove_event(self.transEvent)
        self.close()

    def createNewTransactionWindow(self):
        """
        Function to create the new transactions window
        which can add transactions to this event
        """
        if self.originalwindow.originalwindow.account.displayName.isspace():
            nameerror = QMessageBox.critical(self, "No Display Name", "Set a display name in account settings before adding a transaction",
                                             buttons=QMessageBox.Ok)
        else:
            self.newTransWin = transactions.NewTransactionWindow(self)
            self.newTransWin.show()

    def createTransactionMenu(self, item):
        """
        Function to create a transaction and add it to the event
        """
        selTrans = self.transEvent.transactions[item.text()]
        self.curRow = self.transactionlist.currentRow()
        self.transMenu = transactions.TransactionMenu(self, selTrans)
        self.transMenu.show()

    def editTransaction(self, transaction):
        """
        Function to open the edit transaction window
        """
        self.editTransWindow = transactions.EditTransactionWindow(self, transaction)
        self.editTransWindow.show()

    def submitTransactionEdit(self, oldTransaction):
        """
        Funtcion to submit a transaction edit to the event
        """
        name = self.editTransWindow.nameLineEdit.text()
        desc = self.editTransWindow.descLineEdit.text()
        debtorData = []
        rows = self.editTransWindow.debtorsTable.rowCount()
        # Gather all of the data from the table
        for r in range(rows):
            item = ["", -999]
            debtorname = self.editTransWindow.debtorsTable.item(r, 0)
            ammount = self.editTransWindow.debtorsTable.item(r, 1)

            # Validate the row
            if debtorname and debtorname.text():
                item[0] = debtorname.text()
            if ammount and ammount.text():
                try:
                    item[1] = float(ammount.text())
                except ValueError:
                    # Handle Error
                    print("Error: item is not a float")
                    return

            if item[0] != "" or item[1] != -999:
                debtorData.append(item)
            else:
                print("Invalid debtor. Not adding")

        # Create a new transaction
        newTransaction = classes.Transaction(name, desc)
        for i in range(len(debtorData)):
            newTransaction.add_debtor(debtorData[i])

        # Replace the old transaction with the new one
        self.removeTransaction(oldTransaction)
        self.addTransaction(newTransaction)
        self.editTransWindow.close()
        self.transEvent.is_complete = False
        self.originalwindow.refreshEventTable()

    def addTransaction(self, transaction):
        """
        Function to add a transaction to the event
        """
        self.transEvent.add_transaction(transaction)
        item = QListWidgetItem(transaction.name)
        self.transactionlist.addItem(item)
        self.transEvent.is_complete = False
        self.originalwindow.refreshEventTable()

    def removeTransaction(self, transaction):
        """
        Function to remove a transaction to the event
        """
        self.transactionlist.takeItem(self.curRow)
        self.transactionlist.update()
        self.transEvent.remove_transaction(transaction)
        self.transEvent.is_complete = False
        self.originalwindow.refreshEventTable()


class EditEventWindow(QWidget):
    """
    Window to edit an event
    An events name is currently the only part that can be changed as changing participants would affect all transactions
    in an undefined way
    """
    def __init__(self, originalwindow):
        """
        Create widgets for editing
        """
        super().__init__()
        self.originalwindow = originalwindow

        self.setWindowTitle("Edit Event")
        self.resize(800, 500)
        self.account = originalwindow.originalwindow.originalwindow.account

        self.container = QWidget()
        self.wlayout = QVBoxLayout()

        self.nameLabel = QLabel("Enter Name:")
        self.nameLabel.setAlignment(Qt.AlignHCenter)
        self.eventnameLineEdit = QLineEdit(self.originalwindow.transEvent.name)

        self.save_event_button = QPushButton("Save")
        self.save_event_button.clicked.connect(lambda: self.save_event_info())

        self.wlayout.addWidget(self.nameLabel)
        self.wlayout.addWidget(self.eventnameLineEdit)
        self.wlayout.addWidget(self.save_event_button)
        self.setLayout(self.wlayout)

    def save_event_info(self):
        """
        Copy event data, remove the old event, add the new one
        """
        event = classes.Event(self.eventnameLineEdit.text())
        event.transactions = self.originalwindow.transEvent.transactions
        event.people = self.originalwindow.transEvent.people
        event.num_transactions = self.originalwindow.transEvent.num_transactions
        event.is_complete = False
        self.originalwindow.originalwindow.remove_event(self.originalwindow.transEvent)
        self.originalwindow.originalwindow.saveCurEvent(event)
        self.originalwindow.originalwindow.refreshEventTable()
        self.originalwindow.close()
        self.close()
        

class NewEventWindow(QWidget):
    """
    This class represents the new event window that allows
    the createion of events
    """

    def __init__(self, originalwindow, account):
        """
        Create the widget and populate it
        """

        super().__init__()
        self.setWindowTitle("Create a New Event")
        self.resize(800, 500)
        self.account = account

        self.container = QWidget()
        self.wlayout = QVBoxLayout()

        self.nameLabel = QLabel("Enter event name:")
        self.nameLabel.setAlignment(Qt.AlignHCenter)
        self.eventnameLineEdit = QLineEdit()

        listlabel = QLabel("Select friends for event")
        self.eventfriendslist = QListWidget()
        self.eventfriendslist.setSelectionMode(QListWidget.ExtendedSelection)
        for friend in account.friends:
            self.eventfriendslist.addItem(friend)

        self.save_event_button = QPushButton("Save")
        self.save_event_button.clicked.connect(lambda: self.save_event_info(originalwindow))
        # self.add_event_button.clicked.connect(lambda: (self.addEvent()))

        self.wlayout.addWidget(self.nameLabel)
        self.wlayout.addWidget(self.eventnameLineEdit)
        self.wlayout.addWidget(listlabel)
        self.wlayout.addWidget(self.eventfriendslist)
        self.wlayout.addWidget(self.save_event_button)
        self.setLayout(self.wlayout)

    def set_size(self, length, width):
        """
        Resize the widget
        """
        self.resize(length, width)

    def save_event_info(self, originalwindow):
        """
        Save the event info and add the event to the list
        """

        # TODO: add else with a dialog box that says there was no name entered
        if self.eventnameLineEdit.text():
            self.savedEvent = classes.Event(self.eventnameLineEdit.text())
            friends = self.eventfriendslist.selectedItems()
            for friend in friends:
                friend_obj = self.account.friends[friend.text()]
                self.savedEvent.add_people(friend_obj)
            originalwindow.saveCurEvent(self.savedEvent)
            originalwindow.addEventtoTable(self.savedEvent.name)
        self.close()
