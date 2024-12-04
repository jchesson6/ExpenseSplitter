"""
accountscreen.py

This file contains the account screen and associated widgets
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt


# not sure if we should allow username to be changed since you would have to reset the account login
class editAccWindow(QWidget):
    """
    This class is the edit account screen that allows users to
    change the display name of the account
    """

    def __init__(self, originalwindow, name):
        """
        Initialize the window with the parent window and the current display name
        """
        super().__init__()

        layout = QVBoxLayout()
        self.desc = QLabel("Display Name")
        self.displaynamefield = QLineEdit()
        self.savebutton = QPushButton("Save")
        self.savebutton.clicked.connect(lambda: self.set_acc_name(originalwindow, self.displaynamefield.text()))

        layout.addWidget(self.desc)
        layout.addWidget(self.displaynamefield)
        layout.addWidget(self.savebutton)
        self.setLayout(layout)

    def set_acc_name(self, originalwindow, name):
        """
        Set the accounts name
        """
        originalwindow.set_acc_name(name)
        self.close()


class AccountScreen(QWidget):
    """
    This class is the account screen that displays account information
    and an option to edit the account
    """

    def __init__(self, originalwindow):
        """
        Create the screen with a reference to the parent window
        """
        self.originalwindow = originalwindow
        super().__init__()
        self.init_gui()

    def init_gui(self):
        """
        Initialize the widgets on the screen and link functions to events
        """
        layout = QVBoxLayout()
        self.label0 = QLabel("{Username}")
        self.label1 = QLabel("{DisplayName}")
        self.label2 = QLabel("{NumFriends}")
        self.label3 = QLabel("{TotalAmmountOwed}")
        buttoncontainer = QWidget()
        buttonlayout = QHBoxLayout()
        self.editaccbutton = QPushButton("Set Display Name")
        self.delaccbutton = QPushButton("Delete Account")

        self.editaccbutton.clicked.connect(lambda: self.createEditAccWindow())
        self.delaccbutton.clicked.connect(lambda: self.delete_account())

        buttonlayout.addWidget(self.editaccbutton)
        buttonlayout.addWidget(self.delaccbutton)
        buttoncontainer.setLayout(buttonlayout)
        self.label0.setAlignment(Qt.AlignHCenter)
        self.label1.setAlignment(Qt.AlignHCenter)
        self.label2.setAlignment(Qt.AlignHCenter)
        self.label3.setAlignment(Qt.AlignHCenter)
        layout.addWidget(self.label0)
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
        layout.addWidget(self.label3)
        layout.addWidget(buttoncontainer)

        self.setLayout(layout)

    def load_account(self, account):
        """
        populate the screen with account data
        """
        self.label0.setText("Username: " + account.username)
        self.label1.setText("Display Name: " + account.displayName)
        self.label2.setText("Number of friends: " + str(account.num_friends))
        self.label3.setText("Total Owed to Other Account: " + str(account.amt_owed_total))

    def createEditAccWindow(self):
        """
        Function to create the edit account window
        """
        self.editAccWin = editAccWindow(self, self.originalwindow.account.displayName)
        self.editAccWin.show()

    def set_acc_name(self, name):
        """
        Function to set then display name of the account
        """
        for friend in self.originalwindow.account.friends:
            if name.strip() == friend.strip():
                QMessageBox.critical(self, "Name Error", name + " is already the name of a friend", buttons=QMessageBox.Ok)
                return

        self.originalwindow.account.displayName = name
        self.originalwindow.account.save()
        self.load_account(self.originalwindow.account)
        QMessageBox.warning(self, "Event Warning", 
                            "Events using previous display names must be remade or the display name must be changed back to access",
                            buttons=QMessageBox.Ok)

    def delete_account(self):
        """
        Function to delete the account
        """
        # TODO: add a confirmation pop up box
        reply = QMessageBox.warning(self, "Confirm account deletion", "Are you sure you want to delete your account?", 
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.originalwindow.account.deleteAcc()
            self.originalwindow.close()
            self.close()
