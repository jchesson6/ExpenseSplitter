from PyQt5.QtWidgets import QApplication, QHeaderView, QTextEdit, QLabel, QLineEdit, QTableWidgetItem, QTableWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QStackedWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
import sys


class InfoWindow(QMainWindow):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)

    def set_size(self, length, width):
        self.resize(length,width)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

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
        accDetailsScreen = self.createAccDetailsScreen()
        homeScreen = self.createHomeScreen()
        eventScreen = self.createEventScreen()

        # The stacked widget holds all of the separate screens that the app can display
        # None are displayed at the same time so changing the current widget changes the screen
        self.stackedWidget = QStackedWidget()

        self.stackedWidget.addWidget(accDetailsScreen)
        accDetails.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(accDetailsScreen))

        self.stackedWidget.addWidget(homeScreen)
        home.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(homeScreen))

        self.stackedWidget.addWidget(eventScreen)
        events.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(eventScreen))

        # Add stacked widget to the mainlayout
        mainLayout.addWidget(self.stackedWidget)
        
        container = QWidget()
        container.setLayout(mainLayout)
        self.setCentralWidget(container)

        # Set screen to home
        self.stackedWidget.setCurrentWidget(homeScreen)

    # Create and return a QWidget that represents the account details screen
    def createAccDetailsScreen(self):
        screen = QWidget()
        layout = QVBoxLayout()
        label1 = QLabel("{Name}")
        label2 = QLabel("{NumFriends}")
        label3 = QLabel("{TotalAmmountOwed}")
        label1.setAlignment(Qt.AlignHCenter)
        label2.setAlignment(Qt.AlignHCenter)
        label3.setAlignment(Qt.AlignHCenter)
        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(label3)
        screen.setLayout(layout)
        return screen

    # Create and return a QWidget that represents the home screen
    # TODO: Fill out transaction table
    def createHomeScreen(self):
        screen = QWidget()
        layout = QVBoxLayout()
        transactionTable = QTableWidget()
        transactionTable.setRowCount(1)
        transactionTable.setColumnCount(2)
        transactionTable.setItem(0, 0, QTableWidgetItem("Name"))
        transactionTable.setItem(0, 1, QTableWidgetItem("Amount Owed"))
        transactionTable.horizontalHeader().setVisible(False)
        transactionTable.verticalHeader().setVisible(False)
        transactionTable.horizontalHeader().setStretchLastSection(True)
        transactionTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(transactionTable)
        screen.setLayout(layout)
        return screen
    
    def createEventScreen(self):
        screen = QWidget()
        layout = QVBoxLayout()
        newEventButton = QPushButton("Create a New Event")
        newEventButton.clicked.connect(self.createNewEventWindow)
        eventcontainer = QWidget()
        
        layout.addWidget(newEventButton)
        layout.addWidget(eventcontainer)
        screen.setLayout(layout)

        return screen
    
    def createNewEventWindow(self):
        self.NewEventWindow = InfoWindow("New Event")
        self.NewEventWindow.set_size(800, 600)
        self.NewEventWindow.show() 
        # will need to add modal dialog options to disable input on main window

    # Create and return a QWidget that represents a new transaction screen
    def createNewTransScreen(self):
        screen = QWidget()
        layout = QVBoxLayout()

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
