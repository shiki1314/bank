from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtSql import *
from db import db_login,db_showtable


class Login(QDialog):
    def __init__(self, *args, **kwargs):
        super(Login, self).__init__(*args, **kwargs)

        self.setFixedWidth(300)
        self.setFixedHeight(180)

        layout = QVBoxLayout()

        self.userinput= QLineEdit()
        self.userinput.setPlaceholderText("Enter Username.")
        self.passinput = QLineEdit()
        self.passinput.setEchoMode(QLineEdit.Password)
        self.passinput.setPlaceholderText("Enter Password.")
        self.QBtn = QPushButton()
        self.QBtn.setText("Login")
        self.setWindowTitle('Login')
        self.QBtn.clicked.connect(self.login)

        title = QLabel("Login")
        font = title.font()
        font.setPointSize(16)
        title.setFont(font)

        layout.addWidget(title)
        layout.addWidget(self.userinput)
        layout.addWidget(self.passinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def login(self):
        user = self.userinput.text()
        psd  = self.passinput.text()
        ipaddr = '127.0.0.1'
        dbname = 'bank'
        db = db_login(user,psd,ipaddr,dbname)
        tables = db_showtable(db)

        if db == None:
            QMessageBox.information(self,'提示','登录失败!',QMessageBox.Close,QMessageBox.Close)

