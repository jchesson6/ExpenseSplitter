from PyQt5.QtWidgets import QApplication, QHeaderView, QTextEdit, QLabel, QLineEdit, QTableWidgetItem, QTableWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QStackedWidget, QListWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
import sys
import os
import classes, homescreen, accountscreen, eventscreen

# TODO: Remember to write event/transacton.friend changes to the account.txt file

class InfoWindow(QMainWindow):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)

    def set_size(self, length, width):
        self.resize(length,width)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        ## create variables
        self.event_list = [] # should probably turn this into a dictionary
        self.event_names = []

        self.setWindowTitle("Expenses Splitter")
        self.resize(1200,800)

        mainLayout = QVBoxLayout()
        navLayout = QHBoxLayout()

        # Each navigation button calls changeScreen with the index of the appropriate
        # screen in the stackedWidget
        accDetails = QPushButton("Account Details")
        home = QPushButton("Home")
        events = QPushButton("Events")
        #newTrans.clicked.connect(lambda: self.changeScreen(2))
        navLayout.addWidget(accDetails)
        navLayout.addWidget(home)
        navLayout.addWidget(events)
        mainLayout.addLayout(navLayout)

        #create all separate screens
        self.accDetailsScreen = accountscreen.AccountScreen()
        self.homeScreen = homescreen.HomeScreen()
        self.eventScreen = eventscreen.EventScreen()

        # The stacked widget holds all of the separate screens that the app can display
        # None are displayed at the same time so changing the current widget changes the screen
        self.stackedWidget = QStackedWidget()

        self.stackedWidget.addWidget(self.accDetailsScreen)
        accDetails.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.accDetailsScreen))

        self.stackedWidget.addWidget(self.homeScreen)
        home.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.homeScreen))

        self.stackedWidget.addWidget(self.eventScreen)
        events.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.eventScreen))

        # Add stacked widget to the mainlayout
        mainLayout.addWidget(self.stackedWidget)

        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)

        # Widget for main app and login screen
        stackedContainer = QStackedWidget()

        # Create loginscreen
        loginLayout = QVBoxLayout()
        usernameLabel = QLabel("Username")
        usernameLabel.setAlignment(Qt.AlignHCenter)
        usernameBox = QLineEdit()
        submitLogin = QPushButton("Login")

        loginLayout.addWidget(usernameLabel)
        loginLayout.addWidget(usernameBox)
        loginLayout.addWidget(submitLogin)

        loginWidget = QWidget()
        loginWidget.setLayout(loginLayout)

        stackedContainer.addWidget(mainWidget)
        stackedContainer.addWidget(loginWidget)

        submitLogin.clicked.connect(
            lambda: (
                stackedContainer.setCurrentWidget(mainWidget),
                self.login(usernameBox.text())
            )
        )

        self.setCentralWidget(stackedContainer)

        # Set screen to home
        # TODO: change to log in screen or account creation screen
        self.stackedWidget.setCurrentWidget(self.homeScreen)

        if not os.path.isfile("account.txt"):
            stackedContainer.setCurrentWidget(loginWidget)
        else:
            self.loadAccountData()
            stackedContainer.setCurrentWidget(mainWidget)

    # TODO: Find a better way to store data in the file
    # Maybe json? and use pythons builtin json lib
    # Or find a way to directly load and store python class data
    def loadAccountData(self):
        dataFile = open("account.txt", "r")
        accountName = dataFile.read()
        self.account = classes.Account(accountName)
        print(f"Loaded account: {self.account.name}")
        dataFile.close()

    def login(self, username):
        dataFile = open("account.txt", "w+")
        dataFile.write("Username: " + username + "\n")
        self.account = classes.Account(username)
        print(f"Created account: {username}")
        dataFile.close()

    # TODO: create ability to add friends to event
    def createNewEventWindow(self):
        self.NewEventWindow = InfoWindow("New Event")
        self.NewEventWindow.set_size(300, 200)

        container = QWidget()
        layout = QVBoxLayout()

        nameLabel = QLabel("Enter event name:")
        nameLabel.setAlignment(Qt.AlignHCenter)
        self.eventnameLineEdit = QLineEdit()

        #add a drop down selection or some sort of menu to select friends to add

        add_event_button = QPushButton("Save")
        add_event_button.clicked.connect(lambda: (self.addEvent()))

        layout.addWidget(nameLabel)
        layout.addWidget(self.eventnameLineEdit)
        layout.addWidget(add_event_button)
        container.setLayout(layout)
        self.NewEventWindow.setCentralWidget(container)

        self.NewEventWindow.show()
        # will need to add modal dialog options to disable input on main window

    # Create and return a QWidget that represents a new transaction screen
    def createNewTransScreen(self):
        screen = QWidget()
        layout = QVBoxLayout()

        # TODO: Make this a drop down menu and use the Friend class
        # Also create a table to show all added friends
        # Don't allow duplicates
        nameLabel = QLabel("Names (Separated By Commas):")
        nameLabel.setAlignment(Qt.AlignHCenter)
        nameLineEdit = QLineEdit()

        ammountLabel = QLabel("Enter ammount:")
        ammountLabel.setAlignment(Qt.AlignHCenter)
        ammountLineEdit = QLineEdit()
        ammountLineEdit.setValidator(QDoubleValidator(0, 9999, 2))
        ammountLineEdit.setText("0.00")
        commentsLabel = QLabel("Comments:")
        commentsLabel.setAlignment(Qt.AlignHCenter)
        commentsTextEdit = QTextEdit()
        lineHeight = commentsTextEdit.fontMetrics().lineSpacing()
        commentsTextEdit.setMinimumHeight(lineHeight * 5)
        submitButton = QPushButton("Submit")
        submitButton.clicked.connect(
            lambda: (
                self.addTransaction(
                    [name.strip() for name in nameLineEdit.text().split(",")],
                    float(ammountLineEdit.text()),
                    commentsTextEdit.text()
                ),
                nameLineEdit.setText(""),
                ammountLineEdit.setText("0.00"),
                commentsTextEdit.setText("")
            )
        )

        layout.addWidget(nameLabel)
        layout.addWidget(nameLineEdit)
        layout.addWidget(ammountLabel)
        layout.addWidget(ammountLineEdit)
        layout.addWidget(commentsLabel)
        layout.addWidget(commentsTextEdit)
        layout.addWidget(submitButton)
        screen.setLayout(layout)
        return screen


    def addEvent(self):
        curevent = classes.Event(self.eventnameLineEdit.text())
        self.event_list.append(curevent)
        self.event_names.append(curevent.name)
        self.eventScreen.update()
        self.NewEventWindow.close()




    # Function used to create a transaction when the submit
    # button is pressed on the new transaction screen
    # TODO: Actually create transactions
    def addTransaction(self, names, ammount, comments):
        print(names)
        print(ammount)
        print(comments)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
