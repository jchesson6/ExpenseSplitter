from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QLabel, QLineEdit, QMainWindow, QScrollArea
from PyQt5.QtGui import QWindow
from PyQt5.QtCore import Qt
import classes
import transactions


class EventScreen(QWidget):
    
    curEvent = None
    eventList = []
    
    def __init__(self, originalwindow):
        super().__init__()
        self.init_gui()
        self.originalwindow = originalwindow

    def init_gui(self):
        self.wlayout = QVBoxLayout()
        self.newEventButton = QPushButton("New Event")
        self.newEventButton.clicked.connect(lambda: self.createNewEventWindow(self.originalwindow))
        # eventcontainer = QWidget()

        self.eventtable = QListWidget()

        if len(self.eventList) > 0:
            self.eventtable.insertItems(self.eventList)

        self.eventtable.itemDoubleClicked.connect(self.createEventTransactionsWindow)
        
        self.wlayout.addWidget(self.newEventButton)
        self.wlayout.addWidget(self.eventtable)
        self.setLayout(self.wlayout)

    def createNewEventWindow(self, originalwindow):
        self.newEventWin = NewEventWindow(self, originalwindow.account)
        self.newEventWin.show()

    def createEventTransactionsWindow(self, item):
        selEvent = self.originalwindow.account.events[item.text()]
        self.curRow = self.eventtable.currentRow()
        self.eventTransWin = EventTransactionsWindow(self, selEvent)
        self.eventTransWin.show()
        

    def saveCurEvent(self, event):
        self.curEvent = event
        self.originalwindow.account.add_event(event)
        self.originalwindow.account.save()

        print(self.originalwindow.account.num_events)

        for events in self.originalwindow.account.events:
            print(events)

    def addEventtoTable(self, event):
        self.eventtable.addItem(event)
        self.eventtable.update()

    def remove_event(self, event):
        self.eventtable.takeItem(self.curRow)
        self.eventtable.update()
        self.originalwindow.account.remove_event(event.name)


class EventTransactionsWindow(QWidget):

    def __init__(self, originalwindow, event):
        super().__init__()
        self.transEvent = event
        self.originalwindow = originalwindow
        self.resize(800, 500)
        self.setWindowTitle(event.name + " Menu")

        layout = QVBoxLayout()

        self.addtransbutton = QPushButton("Add Transaction")
        self.addtransbutton.clicked.connect(self.createNewTransactionWindow)
        self.editeventbutton = QPushButton("Edit Event")
        self.deleventbutton = QPushButton("Delete Event")
        self.deleventbutton.clicked.connect(self.removeEvent)
        transactionlabel = QLabel("Transactions")
        transactionlabel.setAlignment(Qt.AlignHCenter)

        self.transactionlist = QListWidget()
        for transaction in self.transEvent.transactions:
            self.transactionlist.addItem(transaction)

        self.transactionlist.itemDoubleClicked.connect(self.createTransactionMenu)

        layout.addWidget(self.addtransbutton)
        layout.addWidget(self.editeventbutton)
        layout.addWidget(self.deleventbutton)
        layout.addWidget(transactionlabel)
        layout.addWidget(self.transactionlist)

        self.setLayout(layout)

    def removeEvent(self):
        self.originalwindow.remove_event(self.transEvent)
        self.close()

    def createNewTransactionWindow(self):
        self.newTransWin = transactions.NewTransactionWindow(self)
        self.newTransWin.show()

    def createTransactionMenu(self, item):
        selTrans = self.transEvent.transactions[item.text()]
        self.curRow = self.transactionlist.currentRow()
        self.transMenu = transactions.TransactionMenu(self, selTrans)
        self.transMenu.show()

    def addTransaction(self, transaction):
        self.transEvent.add_transaction(transaction)
        self.transactionlist.addItem(transaction.name)

    def removeTransaction(self, transaction):
        self.transactionlist.takeItem(self.curRow)
        self.transactionlist.update()
        self.transEvent.remove_transaction(transaction)



class NewEventWindow(QWidget):
    def __init__(self, originalwindow, account):
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
        self.resize(length,width)

    def save_event_info(self, originalwindow):
        #TODO: add else with a dialog box that says there was no name entered
        if self.eventnameLineEdit.text():
            self.savedEvent = classes.Event(self.eventnameLineEdit.text())
            friends = self.eventfriendslist.selectedItems()
            for friend in friends:
                friend_obj = self.account.friends[friend.text()]
                self.savedEvent.add_people(friend_obj)
            originalwindow.saveCurEvent(self.savedEvent)
            originalwindow.addEventtoTable(self.savedEvent.name)
        self.close()


