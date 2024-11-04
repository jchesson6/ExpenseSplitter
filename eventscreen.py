from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QLabel, QLineEdit, QMainWindow, QScrollArea
from PyQt5.QtGui import QWindow
from PyQt5.QtCore import Qt
import classes


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
        self.newEventButton.clicked.connect(self.createNewEventWindow)
        # eventcontainer = QWidget()

        self.eventtable = QListWidget()

        if len(self.eventList) > 0:
            self.eventtable.insertItems(self.eventList)

        self.eventtable.itemDoubleClicked.connect(self.createEventTransactionsWindow)
        
        self.wlayout.addWidget(self.newEventButton)
        self.wlayout.addWidget(self.eventtable)
        self.setLayout(self.wlayout)

    def createNewEventWindow(self):
        self.newEventWin = NewEventWindow(self)
        self.newEventWin.show()

    def createEventTransactionsWindow(self, item):
        selEvent = self.originalwindow.account.events[item.text()]
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
        self.eventList.append(event)
        self.eventtable.addItem(event)
        self.eventtable.update()


class EventTransactionsWindow(QWidget):

    def __init__(self, originalwindow, event):
        super().__init__()
        self.transEvent = event
        self.originalwindow = originalwindow
        self.resize(500, 300)
        self.setWindowTitle(event.name + " Menu")

        self.container = QWidget()
        layout = QVBoxLayout()

        self.addtransbutton = QPushButton("Add Transaction")
        self.editeventbutton = QPushButton("Edit Event")
        self.deleventbutton = QPushButton("Delete Event")
        transactionlabel = QLabel("Transactions")
        transactionlabel.setAlignment(Qt.AlignHCenter)

        self.transactionlist = QListWidget()

        layout.addWidget(self.addtransbutton)
        layout.addWidget(self.editeventbutton)
        layout.addWidget(self.deleventbutton)
        layout.addWidget(transactionlabel)
        layout.addWidget(self.transactionlist)

        self.setLayout(layout)


class NewEventWindow(QWidget):
    def __init__(self, originalwindow):
        super().__init__()
        self.setWindowTitle("Create a New Event")
        self.resize(800, 500)

        self.container = QWidget()
        self.wlayout = QVBoxLayout()

        self.nameLabel = QLabel("Enter event name:")
        self.nameLabel.setAlignment(Qt.AlignHCenter)
        self.eventnameLineEdit = QLineEdit()
        self.save_event_button = QPushButton("Save")
        self.save_event_button.clicked.connect(lambda: self.save_event_info(originalwindow))
        # self.add_event_button.clicked.connect(lambda: (self.addEvent()))

        self.wlayout.addWidget(self.nameLabel)
        self.wlayout.addWidget(self.eventnameLineEdit)
        self.wlayout.addWidget(self.save_event_button)
        self.setLayout(self.wlayout)

    def set_size(self, length, width):
        self.resize(length,width)

    def save_event_info(self, originalwindow):
        #TODO: add else with a dialog box that says there was no name entered
        if self.eventnameLineEdit.text():
            self.savedEvent = classes.Event(self.eventnameLineEdit.text())
            originalwindow.saveCurEvent(self.savedEvent)
            originalwindow.addEventtoTable(self.savedEvent)
        self.close()


class NewTransactionWindow(QWidget):
    def __init__(self, originalwindow):
        super().__init__()
        self.setWindowTitle("New Transaction")
        self.resize(800, 500)