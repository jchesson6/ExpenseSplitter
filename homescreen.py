from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QHeaderView, QPushButton, QLineEdit, QDoubleSpinBox
import classes

# Create and return a QWidget that represents the home screen
# TODO: Fill out transaction table
class HomeScreen(QWidget):
    
    def __init__(self, originalwindow):
        self.originalwindow = originalwindow
        super().__init__()
        self.init_gui()
        

    def init_gui(self):
        layout = QVBoxLayout()
        buttonlayout = QHBoxLayout()
        buttoncontainer = QWidget()
        self.addFriendButton = QPushButton("Add Friend")
        self.remFriendButton = QPushButton("Remove Friend")
        self.addFriendButton.clicked.connect(self.createNewFriendWindow)
        self.remFriendButton.clicked.connect(self.createRemoveFriendWindow)
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
        self.setLayout(layout)


    def createNewFriendWindow(self):
        self.newFriendWin = NewFriendWindow(self)
        self.newFriendWin.show()

    def createRemoveFriendWindow(self):
        self.removefriendwin = removeFriendWindow(self)
        self.removefriendwin.show()

    #TODO: dont allow duplicates
    def add_friend(self, friend):
        self.originalwindow.account.add_friend(friend)
        self.originalwindow.accDetailsScreen.load_account(self.originalwindow.account)
        newrow = self.friendslist.rowCount()
        self.friendslist.insertRow(newrow)
        self.friendslist.setItem(newrow, 0, QTableWidgetItem(friend.name))
        self.friendslist.setItem(newrow, 1, QTableWidgetItem(str(friend.amount_owed_by_user)))
        self.friendslist.setItem(newrow, 2, QTableWidgetItem(str(friend.amount_owed_to_user)))
        
    
    def remove_friend(self, name):
        friendslist = list(self.originalwindow.account.friends.keys())
        if name in friendslist:
            tableindex = friendslist.index(name)
            self.friendslist.removeRow(tableindex)
            self.originalwindow.account.remove_friend(name)
        

    def updateList(self, account):
        for friend in account.friends:
            newrow = self.friendslist.rowCount()
            self.friendslist.insertRow(newrow)
            self.friendslist.setItem(newrow, 0, QTableWidgetItem(friend))
            self.friendslist.setItem(newrow, 1, QTableWidgetItem(str(account.friends[friend].amount_owed_by_user)))
            self.friendslist.setItem(newrow, 2, QTableWidgetItem(str(account.friends[friend].amount_owed_to_user)))
        

class NewFriendWindow(QWidget):
    def __init__(self, originalwindow):
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
        newfriend = classes.Friend(self.friendnamefield.text())
        newfriend.amount_owed_by_user = self.amountowedtofriendfield.value()
        newfriend.amount_owed_to_user = self.amountowedbyfriendfield.value()
        self.originalwindow.add_friend(newfriend)
        self.close()


class removeFriendWindow(QWidget):
    def __init__(self, originalwindow):
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
        originalwindow.remove_friend(self.friendnamefield.text())
        self.close()