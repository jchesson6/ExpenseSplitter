from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QLabel, QLineEdit, QMainWindow
from PyQt5.QtGui import QWindow
from PyQt5.QtCore import Qt
import classes

class NewEventWindow(QMainWindow):
    def __init__(self, originalwindow):
        super().__init__()
        self.setWindowTitle("Create a New Event")
        self.resize(500, 300)

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
        self.container.setLayout(self.wlayout)
        self.setCentralWidget(self.container)

    def set_size(self, length, width):
        self.resize(length,width)

    def save_event_info(self, originalwindow):
        #TODO: add else with a dialog box that says there was no name entered
        if self.eventnameLineEdit.text():
            self.savedEvent = classes.Event(self.eventnameLineEdit.text())
            originalwindow.saveCurEvent(self.savedEvent)
            originalwindow.addEventtoTable(self.savedEvent)
        self.close()

class EventScreen(QWidget):
    
    curEvent = None
    eventList = []
    
    def __init__(self):
        super().__init__()
        self.init_gui()

    def init_gui(self):
        self.wlayout = QVBoxLayout()
        self.newEventButton = QPushButton("New Event")
        self.newEventButton.clicked.connect(self.createNewEventWindow)
        # eventcontainer = QWidget()

        self.eventtable = QListWidget()
        
        self.wlayout.addWidget(self.newEventButton)
        self.wlayout.addWidget(self.eventtable)
        self.setLayout(self.wlayout)

    def createNewEventWindow(self):
        self.newEventWin = NewEventWindow(self)
        self.newEventWin.show()

    def saveCurEvent(self, event):
        self.curEvent = event

    def addEventtoTable(self, event):
        self.eventList.append(event)
        self.eventtable.addItem(event.name)
        self.eventtable.update()
