"""
homescreen.py

This file contains the widget that displays the home screen
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, 
                             QLabel, QHeaderView, QPushButton, QLineEdit, QDoubleSpinBox, QComboBox,
                             QMessageBox
                             )
from PyQt5.QtGui import QDoubleValidator
import classes

# Create and return a QWidget that represents the home screen
# TODO: Fill out transaction table
class HomeScreen(QWidget):
    """
    Class that represent the home screen widget
    """
    def __init__(self, originalwindow):
        """
        Save the parent window then create the widgets
        """
        self.originalwindow = originalwindow
        super().__init__()
        self.init_gui()
        

    def init_gui(self):
        """
        Create all of the widgets on the screen
        """
        layout = QVBoxLayout()
        buttonlayout = QHBoxLayout()
        buttoncontainer = QWidget()
        self.addFriendButton = QPushButton("Add Friend")
        self.remFriendButton = QPushButton("Remove Friend")
        self.inputamtpaidbutton = QPushButton("Input Amount Paid to Friend")
        self.addFriendButton.clicked.connect(self.createNewFriendWindow)
        self.remFriendButton.clicked.connect(self.createRemoveFriendWindow)
        self.inputamtpaidbutton.clicked.connect(self.createInputAmountWindow)
        self.friendslist = QTableWidget()
        self.friendslist.setColumnCount(3)
        self.friendslist.setHorizontalHeaderLabels(["Name", "Amount They Owe You", "Amount You Owe Them"])
        self.friendslist.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.friendslist.setStyleSheet("""
            QHeaderView::section {
                border: 1px solid black;
            }
        """)
        buttonlayout.addWidget(self.addFriendButton)
        buttonlayout.addWidget(self.remFriendButton)
        buttoncontainer.setLayout(buttonlayout)
        layout.addWidget(buttoncontainer)
        layout.addWidget(self.friendslist)
        layout.addWidget(self.inputamtpaidbutton)
        self.setLayout(layout)


    def createNewFriendWindow(self):
        """
        Create a window to add a friend
        """
        self.newFriendWin = NewFriendWindow(self)
        self.newFriendWin.show()

    def createRemoveFriendWindow(self):
        """
        Create a window to remove a friend
        """
        self.removefriendwin = removeFriendWindow(self)
        self.removefriendwin.show()

    def createInputAmountWindow(self):
        """
        Create a window to input amounts paid to friends and update friendslist
        """
        self.inputamtpaidwin = inputAmountPaidWindow(self)
        self.inputamtpaidwin.show()

    #TODO: dont allow duplicates
    def add_friend(self, friend):
        """
        Add a friend to the account
        """
        self.originalwindow.account.add_friend(friend)
        self.originalwindow.accDetailsScreen.load_account(self.originalwindow.account)
        newrow = self.friendslist.rowCount()
        self.friendslist.insertRow(newrow)
        self.friendslist.setItem(newrow, 0, QTableWidgetItem(friend.name))
        self.friendslist.setItem(newrow, 1, QTableWidgetItem(str(friend.amount_owed_to_user)))
        self.friendslist.setItem(newrow, 2, QTableWidgetItem(str(friend.amount_owed_by_user)))
        
    
    def remove_friend(self, name):
        """
        Remove a friend from the account
        """
        friendslist = list(self.originalwindow.account.friends.keys())
        if name in friendslist:
            tableindex = friendslist.index(name)
            self.friendslist.removeRow(tableindex)
            self.originalwindow.account.remove_friend(name)
        

    def updateList(self, account):
        """
        Update the frinds list
        """
        self.friendslist.clearContents()
        self.friendslist.setRowCount(0)
        
        for friend in account.friends:
            newrow = self.friendslist.rowCount()
            self.friendslist.insertRow(newrow)
            self.friendslist.setItem(newrow, 0, QTableWidgetItem(friend))
            self.friendslist.setItem(newrow, 1, QTableWidgetItem(str(account.friends[friend].amount_owed_to_user)))
            self.friendslist.setItem(newrow, 2, QTableWidgetItem(str(account.friends[friend].amount_owed_by_user)))
        

class NewFriendWindow(QWidget):
    """
    Window to add a new friend
    """
    def __init__(self, originalwindow):
        """
        Create widgets so user can enter friend information
        """
        super().__init__()
        self.originalwindow = originalwindow
        layout = QVBoxLayout()

        self.resize(500, 800)
        self.setWindowTitle("Add Friend")

        namelabel = QLabel("Enter friend's name")
        self.friendnamefield = QLineEdit()
        amountowedtolabel = QLabel("Enter any previous amount owed to friend by you")
        self.amountowedtofriendfield = QDoubleSpinBox()
        amountowedbylabel = QLabel("Enter any previous amount owed by friend to you")
        self.amountowedbyfriendfield = QDoubleSpinBox()
        self.savefriendbutton = QPushButton("Save Friend")
        self.savefriendbutton.clicked.connect(self.addFriend)

        layout.addWidget(namelabel)
        layout.addWidget(self.friendnamefield)
        layout.addWidget(amountowedtolabel)
        layout.addWidget(self.amountowedtofriendfield)
        layout.addWidget(amountowedbylabel)
        layout.addWidget(self.amountowedbyfriendfield)
        layout.addWidget(self.savefriendbutton)
        self.setLayout(layout)

    def addFriend(self):
        """
        Add the frined to the account
        """
        newfriend = classes.Friend(self.friendnamefield.text())
        newfriend.amount_owed_by_user = self.amountowedtofriendfield.value()
        newfriend.amount_owed_to_user = self.amountowedbyfriendfield.value()
        self.originalwindow.add_friend(newfriend)
        self.close()


class removeFriendWindow(QWidget):
    """
    Window to remove a friend
    """
    def __init__(self, originalwindow):
        """
        Create widgets to remove the friend
        """
        super().__init__()

        layout = QVBoxLayout()
        self.desc = QLabel("Enter friends name to remove")
        self.friendnamefield = QLineEdit()
        self.delbutton = QPushButton("Delete")
        self.delbutton.clicked.connect(lambda: self.removeFriend(originalwindow))

        layout.addWidget(self.desc) 
        layout.addWidget(self.friendnamefield)
        layout.addWidget(self.delbutton)
        self.setLayout(layout)

    def removeFriend(self, originalwindow):
        """
        Remove the friend from the account
        """
        originalwindow.remove_friend(self.friendnamefield.text())
        self.close()


class inputAmountPaidWindow(QWidget):
    def __init__(self, originalwindow):
        """
        Create widgets to input amounts paid and add friends to drop down box
        """
        super().__init__()
        self.originalwindow = originalwindow
        layout = QVBoxLayout()

        payerlabel = QLabel("Select who paid")
        self.payersel = QComboBox()

        paidlabel = QLabel("Select who was paid")
        self.paidsel = QComboBox()

        self.payersel.addItem("Me")
        self.paidsel.addItem("Me")

        for friend in self.originalwindow.originalwindow.account.friends:
            self.payersel.addItem(friend)
            self.paidsel.addItem(friend)

        amtlabel = QLabel("Enter amount paid")
        self.validator = QDoubleValidator()
        self.paidamt = QLineEdit()
        self.paidamt.setValidator(self.validator)
        self.paidamt.setPlaceholderText("00.00")

        self.donebutton = QPushButton("Done")
        self.donebutton.clicked.connect(self.done_clicked)

        layout.addWidget(payerlabel)
        layout.addWidget(self.payersel)
        layout.addWidget(paidlabel)
        layout.addWidget(self.paidsel)
        layout.addWidget(amtlabel)
        layout.addWidget(self.paidamt)
        layout.addWidget(self.donebutton)
        self.setLayout(layout)

    def done_clicked(self):
        """
        Reduce amount owed to friend and update friends list
        """
        amt = float(self.paidamt.text())
        if self.payersel.currentText() == self.paidsel.currentText():
            QMessageBox.critical(self, "Selection Error", "Person paid and person paying cannot match", buttons=QMessageBox.Ok)
            return
        elif self.payersel.currentText() != "Me" and self.paidsel.currentText() != "Me":
            QMessageBox.critical(self, "Selection Error", "User must be one of the selections", buttons=QMessageBox.Ok)
        elif self.payersel.currentText() == "Me" and self.originalwindow.originalwindow.account.friends[self.paidsel.currentText()].amount_owed_by_user >= amt:
            self.originalwindow.originalwindow.account.friends[self.paidsel.currentText()].amount_owed_by_user -= amt
            self.originalwindow.originalwindow.account.friends[self.paidsel.currentText()].amount_owed_to_user += amt
        elif self.payersel.currentText() == "Me" and self.originalwindow.originalwindow.account.friends[self.paidsel.currentText()].amount_owed_by_user < amt:
            newowedtouser = amt - self.originalwindow.originalwindow.account.friends[self.paidsel.currentText()].amount_owed_by_user
            self.originalwindow.originalwindow.account.friends[self.paidsel.currentText()].amount_owed_by_user -= amt
            self.originalwindow.originalwindow.account.friends[self.paidsel.currentText()].amount_owed_to_user = newowedtouser
        elif self.paidsel.currentText() == "Me" and self.originalwindow.originalwindow.account.friends[self.payersel.currentText()].amount_owed_to_user >= amt:
            self.originalwindow.originalwindow.account.friends[self.payersel.currentText()].amount_owed_to_user -= amt
            self.originalwindow.originalwindow.account.friends[self.payersel.currentText()].amount_owed_by_user += amt
        elif self.paidsel.currentText() == "Me" and self.originalwindow.originalwindow.account.friends[self.payersel.currentText()].amount_owed_to_user < amt:
            newowedbyuser = amt - self.originalwindow.originalwindow.account.friends[self.payersel.currentText()].amount_owed_to_user
            self.originalwindow.originalwindow.account.friends[self.payersel.currentText()].amount_owed_by_user = newowedbyuser
            self.originalwindow.originalwindow.account.friends[self.payersel.currentText()].amount_owed_to_user -= amt

        self.originalwindow.originalwindow.account.save()
        self.originalwindow.updateList(self.originalwindow.originalwindow.account)
        self.close()
