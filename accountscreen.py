from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit
from PyQt5.QtCore import Qt

# not sure if we should allow username to be changed since you would have to reset the account login
class editAccWindow(QWidget):
    def __init__(self, originalwindow, name):
        super().__init__()

        layout = QVBoxLayout()
        self.desc = QLabel("Display Name")
        self.displaynamefield = QLineEdit(name)
        self.savebutton = QPushButton("Save")
        self.savebutton.clicked.connect(lambda: self.set_acc_name(originalwindow, self.displaynamefield.text()))

        layout.addWidget(self.desc) 
        layout.addWidget(self.displaynamefield)
        layout.addWidget(self.savebutton)
        self.setLayout(layout)


    def set_acc_name(self, originalwindow, name):
        originalwindow.set_acc_name(name)
        self.close()


class AccountScreen(QWidget):
    
    def __init__(self, originalwindow):
        self.originalwindow = originalwindow
        super().__init__()
        self.init_gui()

    def init_gui(self):
        layout = QVBoxLayout()
        self.label0 = QLabel("{Username}")
        self.label1 = QLabel("{DisplayName}")
        self.label2 = QLabel("{NumFriends}")
        self.label3 = QLabel("{TotalAmmountOwed}")
        buttoncontainer = QWidget()
        buttonlayout = QHBoxLayout()
        self.editaccbutton = QPushButton("Edit Account")
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
        self.label0.setText("Username: " + account.username)
        self.label1.setText("Display Name: " + account.displayName)
        self.label2.setText("Number of friends: " + str(account.num_friends))
        self.label3.setText("Total Owed to Other Account: " + str(account.amt_owed_total))

    def createEditAccWindow(self):
        self.editAccWin = editAccWindow(self, self.originalwindow.account.displayName)
        self.editAccWin.show()

    def set_acc_name(self, name):
        self.originalwindow.account.displayName = name
        self.originalwindow.account.save()
        self.load_account(self.originalwindow.account)

    def delete_account(self):
        #TODO: add a confirmation pop up box
        self.originalwindow.account.deleteAcc()
        self.originalwindow.close()
        self.close()
