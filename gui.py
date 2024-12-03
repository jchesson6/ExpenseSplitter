"""
gui.py

This file contains the main function and defines the main windows behavior
"""

from PyQt5.QtWidgets import QApplication, QListWidgetItem, QHeaderView, QTextEdit, QLabel, QLineEdit, QTableWidgetItem, QTableWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QStackedWidget, QListWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator, QColor, QFont
import sys
import os
import classes, homescreen, accountscreen, eventscreen

# TODO: Remember to write event/transacton.friend changes to the account.txt file

class InfoWindow(QMainWindow):
    """
    This class is a simple resizeable blak window
    """
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)

    def set_size(self, length, width):
        """
        Resize the window
        """
        self.resize(length,width)


class MainWindow(QMainWindow):
    """
    The main window for the applciation
    """
    def __init__(self):
        """
        Populate the window with navigation buttons and create main screens
        Also prompt the user to login and register before accessing the rest of the app
        """
        super().__init__()

        # Create account so the close callback has a value to check
        self.account = None

        # create variables
        self.event_list = [] # should probably turn this into a dictionary
        self.event_names = []

        self.setWindowTitle("Expenses Splitter")
        self.resize(2000,1200)

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
        self.accDetailsScreen = accountscreen.AccountScreen(self)
        self.homeScreen = homescreen.HomeScreen(self)
        self.eventScreen = eventscreen.EventScreen(self)

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

        # Widget for main app and register screen
        stackedContainer = QStackedWidget()

        # create app title
        applabel = QLabel("Group Expense Splitter")
        applabel.setAlignment(Qt.AlignHCenter)
        titlefont = applabel.font()
        titlefont.setPointSize(40)
        titlefont.setCapitalization(QFont.AllUppercase)
        titlefont.setBold(True)
        applabel.setFont(titlefont)

        # Create registerscreen
        registerLayout = QVBoxLayout()
        usernameLabel = QLabel("Username")
        usernameLabel.setAlignment(Qt.AlignHCenter)
        usernameBox = QLineEdit()
        passwordLabel = QLabel("Password")
        passwordLabel.setAlignment(Qt.AlignHCenter)
        passwordBox = QLineEdit()
        submitRegister = QPushButton("Register")

        # Create layout for register screen
        registerLayout.addWidget(applabel)
        registerLayout.addWidget(usernameLabel)
        registerLayout.addWidget(usernameBox)
        registerLayout.addWidget(passwordLabel)
        registerLayout.addWidget(passwordBox)
        registerLayout.addWidget(submitRegister)

        registerWidget = QWidget()
        registerWidget.setLayout(registerLayout)

        # Create widgets for login
        passwordlayout = QHBoxLayout()
        passwordcontainer = QWidget()
        loginlayout = QVBoxLayout()
        passwordLabel2 = QLabel("Enter Password")
        #passwordLabel2.setAlignment(Qt.AlignHCenter)
        passwordBox2 = QLineEdit()
        passwordBox2.setEchoMode(QLineEdit.Password)
        submitLogin = QPushButton("Login")
        passwordBox2.returnPressed.connect(submitLogin.click)

        # Create layout for login
        passwordlayout.addWidget(passwordLabel2)
        passwordlayout.addWidget(passwordBox2)
        passwordcontainer.setLayout(passwordlayout)

        loginlayout.addWidget(applabel)
        loginlayout.addWidget(passwordcontainer)
        #loginlayout.addWidget(passwordBox2)
        loginlayout.addWidget(submitLogin)
        loginWidget = QWidget()
        loginWidget.setLayout(loginlayout)

        # Create a container that can switch the active widget
        stackedContainer.addWidget(mainWidget)
        stackedContainer.addWidget(registerWidget)
        stackedContainer.addWidget(loginWidget)
        stackedContainer.setCurrentWidget(registerWidget)
        submitRegister.clicked.connect(
            lambda: (
                stackedContainer.setCurrentWidget(mainWidget),
                self.register(usernameBox.text(), passwordBox.text())
            )
        )
        submitLogin.clicked.connect(
            lambda: (
                self.verifyPassword(passwordBox2.text(), stackedContainer, mainWidget)
            )
        )

        self.setCentralWidget(stackedContainer)

        # Set screen to home
        # TODO: change to log in screen or account creation screen
        self.stackedWidget.setCurrentWidget(self.homeScreen)

        if not os.path.isfile("account.txt"):
            stackedContainer.setCurrentWidget(registerWidget)
        else:
            self.loadAccountData()
            stackedContainer.setCurrentWidget(loginWidget)

    def verifyPassword(self, password, stackedWidget, targetWidget):
        """
        Check that the entered password matches the saved password
        """
        if (password == self.account.password):
            stackedWidget.setCurrentWidget(targetWidget)

    def loadAccountData(self):
        """
        Load the account data from a file
        """
        self.account = classes.Account.load()
        self.accDetailsScreen.load_account(self.account)
        self.homeScreen.updateList(self.account)

        for event in self.account.events:
            if not self.account.events[event].is_complete:
                item = QListWidgetItem(event)
                item.setBackground(QColor(0xFF0000))
                item.setForeground(QColor(0xFFFFFF))
                self.eventScreen.addEventtoTable(item)
            else:
                item = QListWidgetItem(event)
                item.setBackground(QColor(0x00FF00))
                self.eventScreen.addEventtoTable(item)

        print(f"Loaded account: {self.account.username}")

    def register(self, username, password):
        """
        Save new account info to a file
        """
        dataFile = open("account.txt", "w+")
        dataFile.write("Username: " + username + "\n")
        self.account = classes.Account(username, password)
        self.accDetailsScreen.load_account(self.account)
        self.account.save()
        print(f"Created account: {username}")
        dataFile.close()

    # TODO: create ability to add friends to event
    def createNewEventWindow(self):
        """
        Create a window used to create events
        """
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

    def addEvent(self):
        """
        Function to add an event from the new event window
        """
        curevent = classes.Event(self.eventnameLineEdit.text())
        self.event_list.append(curevent)
        self.event_names.append(curevent.name)
        self.eventScreen.update()
        self.NewEventWindow.close()

    def closeEvent(self, event):
        """
        Function to save the account when the app closes
        """
        if self.account is not None:
            self.account.save()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
