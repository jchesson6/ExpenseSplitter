from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QHeaderView, QPushButton, QLineEdit, QDoubleSpinBox
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
        self.addFriendButton = QPushButton("Add Friend")
        self.addFriendButton.clicked.connect(self.createNewFriendWindow)
        self.friendslist = QTableWidget()
        self.friendslist.setColumnCount(3)
        self.friendslist.setHorizontalHeaderLabels(["Name", "Amount They Owe You", "Amount You Owe Them"])
        self.friendslist.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.friendslist.setStyleSheet("""
            QHeaderView::section {
                border: 1px solid black;
            }
        """)
        layout.addWidget(self.addFriendButton)
        layout.addWidget(self.friendslist)
        self.setLayout(layout)

    def createNewFriendWindow(self):
        self.newFriendWin = NewFriendWindow(self)
        self.newFriendWin.show()

    def add_friend(self, friend):
        self.originalwindow.account.add_friend(friend)
        newrow = self.friendslist.rowCount()
        self.friendslist.insertRow(newrow)
        self.friendslist.setItem(newrow, 0, QTableWidgetItem(friend.name))
        self.friendslist.setItem(newrow, 1, QTableWidgetItem(str(friend.amount_owed_by_user)))
        self.friendslist.setItem(newrow, 2, QTableWidgetItem(str(friend.amount_owed_to_user)))



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