"""
NOTE: Put transaction creation code in the createNewTransaction function

There are 2 available buttons that can be used which are newButton1 and newButton2
each button has functions for creating the widgets that will appear and enabling
the pages widgets and disableing other pages widgets

Look at correcponding HomeScreen and NewTransactionScreen functions as a reference

Also the documentation for python and c++ are very similar for PyQt5 so
if something how up under the c++ docs there is a good chance it will be in the python
version too
"""

import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450


# Class for nav buttons which are visible on every page
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.centralwidget = QtWidgets.QWidget(MainWindow)

        # adding navbuttons
        self.createNavigationButtons()

        self.createNewTransactionScreenWidgets()

        self.createHomeScreenWidgets()

        self.createNewButton1ScreenWidgets()
        self.createNewButton2ScreenWidgets()

        self.screen = "home"

        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.goToHomeScreen()

    def createNavigationButtons(self):
        self.homeButton = QtWidgets.QPushButton(self.centralwidget)
        self.homeButton.setGeometry(
            QtCore.QRect(
                int(SCREEN_WIDTH * (2 / 5)),
                0,
                SCREEN_WIDTH // 5,
                32
            )
        )
        self.homeButton.setText("Home")

        self.createTransactionButton = QtWidgets.QPushButton(
            self.centralwidget
        )
        self.createTransactionButton.setText("New Transaction")
        self.createTransactionButton.setGeometry(
            QtCore.QRect(
                int(SCREEN_WIDTH * 3 / 5),
                0,
                SCREEN_WIDTH // 5,
                32
            )
        )

        self.accountDetailsButton = QtWidgets.QPushButton(self.centralwidget)
        self.accountDetailsButton.setGeometry(
            QtCore.QRect(
                int(SCREEN_WIDTH * 1 / 5),
                0,
                SCREEN_WIDTH // 5,
                32
            )
        )
        self.accountDetailsButton.setText("Account Details")

        self.newButton1 = QtWidgets.QPushButton(self.centralwidget)
        self.newButton1.setGeometry(
            QtCore.QRect(
                0,
                0,
                SCREEN_WIDTH // 5,
                32
            )
        )
        self.newButton1.setText("1")

        self.newButton2 = QtWidgets.QPushButton(self.centralwidget)
        self.newButton2.setGeometry(
            QtCore.QRect(
                int(SCREEN_WIDTH * 4 / 5),
                0,
                SCREEN_WIDTH // 5,
                32
            )
        )
        self.newButton2.setText("2")

        # adding signals and slots
        self.homeButton.clicked.connect(self.goToHomeScreen)
        self.accountDetailsButton.clicked.connect(self.goToDetailsScreen)
        self.createTransactionButton.clicked.connect(
            self.goToNewTransactionScreen
        )
        self.newButton1.clicked.connect(self.goToNewButton1Screen)
        self.newButton2.clicked.connect(self.goToNewButton2Screen)

    def createNewButton1ScreenWidgets(self):
        pass

    def createNewButton2ScreenWidgets(self):
        pass

    def setNewButton1ScreenWidgets(self):
        # Disable widgets for other screens
        self.transactionScreenNameBox.setVisible(False)
        self.transactionScreenNameBoxLabel.setVisible(False)
        self.transactionScreenValueBox.setVisible(False)
        self.transactionScreenValueBoxLabel.setVisible(False)
        self.transactionScreenSubmitButton.setVisible(False)

        self.homeScreenTransactionTable.setVisible(False)

        # Enable widgets for this screen here

    def setNewButton2ScreenWidgets(self):
        # Disable widgets for other screens
        self.transactionScreenNameBox.setVisible(False)
        self.transactionScreenNameBoxLabel.setVisible(False)
        self.transactionScreenValueBox.setVisible(False)
        self.transactionScreenValueBoxLabel.setVisible(False)
        self.transactionScreenSubmitButton.setVisible(False)

        self.homeScreenTransactionTable.setVisible(False)

        # Enable widgets for this screen here

    def goToNewButton1Screen(self):
        self.setNewButton1ScreenWidgets()
        # Add data to widgets here

    def goToNewButton2Screen(self):
        self.setNewButton2ScreenWidgets()
        # Add data to widgets here

    def createNewTransactionScreenWidgets(self):
        self.transactionScreenNameBox = QtWidgets.QLineEdit(self.centralwidget)
        self.transactionScreenNameBox.setGeometry(
            QtCore.QRect(
                SCREEN_WIDTH // 4,
                SCREEN_HEIGHT // 4,
                SCREEN_WIDTH // 2,
                40
            )
        )

        self.transactionScreenNameBoxLabel = QtWidgets.QLabel(
            self.centralwidget
        )
        self.transactionScreenNameBoxLabel.setGeometry(
            QtCore.QRect(
                SCREEN_WIDTH // 4,
                SCREEN_HEIGHT // 4 - 40,
                SCREEN_WIDTH // 2,
                40
            )
        )
        self.transactionScreenNameBoxLabel.setText(
            "Enter A Name For Transaction:"
        )
        self.transactionScreenNameBoxLabel.setAlignment(QtCore.Qt.AlignHCenter)

        self.transactionScreenValueBox = QtWidgets.QLineEdit(self.centralwidget)
        self.transactionScreenValueBox.setGeometry(
            QtCore.QRect(
                SCREEN_WIDTH // 4,
                SCREEN_HEIGHT // 2,
                SCREEN_WIDTH // 2,
                40
            )
        )
        self.transactionScreenValueBox.setValidator(
            QtGui.QDoubleValidator(0, 9999, 2)
        )

        self.transactionScreenValueBoxLabel = QtWidgets.QLabel(
            self.centralwidget
        )
        self.transactionScreenValueBoxLabel.setGeometry(
            QtCore.QRect(
                SCREEN_WIDTH // 4,
                SCREEN_HEIGHT // 2 - 40,
                SCREEN_WIDTH // 2,
                40
            )
        )
        self.transactionScreenValueBoxLabel.setText(
            "Enter Value For Transaction:"
        )
        self.transactionScreenValueBoxLabel.setAlignment(QtCore.Qt.AlignHCenter)

        self.transactionScreenSubmitButton = QtWidgets.QPushButton(
            self.centralwidget
        )
        self.transactionScreenSubmitButton.setGeometry(
            QtCore.QRect(
                SCREEN_WIDTH // 4,
                int(SCREEN_HEIGHT * (3 / 4)),
                SCREEN_WIDTH // 2,
                40
            )
        )
        self.transactionScreenSubmitButton.setText("Submit")
        self.transactionScreenSubmitButton.clicked.connect(
            self.createNewTransaction
        )

    def createNewTransaction(self):

        if self.transactionScreenValueBox.text() == ''   \
            or self.transactionScreenNameBox.text() == '':
            return

        ammount = float(self.transactionScreenValueBox.text())
        name = self.transactionScreenNameBox.text()

        # NOTE: Handle Backend transaction logic here, or call into it from here
        # TODO: Create popup when events are created or there are errors

        # Clear text boxes
        self.transactionScreenValueBox.setText('')
        self.transactionScreenNameBox.setText('')

    def setNewTransactionScreenWidgets(self):
        self.transactionScreenNameBox.setVisible(True)
        self.transactionScreenNameBoxLabel.setVisible(True)
        self.transactionScreenValueBox.setVisible(True)
        self.transactionScreenValueBoxLabel.setVisible(True)
        self.transactionScreenSubmitButton.setVisible(True)

        self.homeScreenTransactionTable.setVisible(False)

    def createHomeScreenWidgets(self):
        self.homeScreenTransactionTable = QtWidgets.QTableWidget(
            self.centralwidget
        )
        self.homeScreenTransactionTable.setGeometry(
            QtCore.QRect(
                0,
                40,
                SCREEN_WIDTH,
                SCREEN_HEIGHT - 40
            )
        )
        self.homeScreenTransactionTable.setRowCount(1)
        self.homeScreenTransactionTable.setColumnCount(2)
        self.homeScreenTransactionTable.setItem(
            0,
            0,
            QtWidgets.QTableWidgetItem("Name")
        )
        self.homeScreenTransactionTable.setItem(
            0,
            1,
            QtWidgets.QTableWidgetItem("Ammount Owed")
        )
        self.homeScreenTransactionTable.horizontalHeader().setStretchLastSection(
            True
        )
        self.homeScreenTransactionTable.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        self.homeScreenTransactionTable.horizontalHeader().setVisible(False)
        self.homeScreenTransactionTable.verticalHeader().setVisible(False)

    def setHomeScreenWidgets(self):
        self.transactionScreenNameBox.setVisible(False)
        self.transactionScreenNameBoxLabel.setVisible(False)
        self.transactionScreenValueBox.setVisible(False)
        self.transactionScreenValueBoxLabel.setVisible(False)
        self.transactionScreenSubmitButton.setVisible(False)

        self.homeScreenTransactionTable.setVisible(True)

    def createDetailsScreenWidgets(self):
        pass

    def setDetailsScreenWidgets(self):
        self.transactionScreenNameBox.setVisible(False)
        self.transactionScreenNameBoxLabel.setVisible(False)
        self.transactionScreenValueBox.setVisible(False)
        self.transactionScreenValueBoxLabel.setVisible(False)
        self.transactionScreenSubmitButton.setVisible(False)

        self.homeScreenTransactionTable.setVisible(False)

    def goToHomeScreen(self):
        self.screen = "home"
        self.setHomeScreenWidgets()

    def goToNewTransactionScreen(self):
        self.screen = "new_transaction"
        self.setNewTransactionScreenWidgets()

    def goToDetailsScreen(self):
        self.screen = "details"
        self.setDetailsScreenWidgets()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())
