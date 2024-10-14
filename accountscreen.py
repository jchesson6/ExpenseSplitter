from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt


class AccountScreen(QWidget):
    
    def __init__(self):
        super().__init__()
        self.init_gui()

    def init_gui(self):
        self.wlayout = QVBoxLayout()
        self.label1 = QLabel("{Name}")
        self.label2 = QLabel("{NumFriends}")
        self.label3 = QLabel("{TotalAmmountOwed}")
        self.label1.setAlignment(Qt.AlignHCenter)
        self.label2.setAlignment(Qt.AlignHCenter)
        self.label3.setAlignment(Qt.AlignHCenter)
        self.wlayout.addWidget(self.label1)
        self.wlayout.addWidget(self.label2)
        self.wlayout.addWidget(self.label3)
        self.setLayout(self.wlayout)