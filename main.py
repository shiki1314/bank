import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtSql import *
from PyQt5.QtChart import *
import sys
from Login import Login
from Branch import  Branch
from Employee import  Employee
from Depart import Depart
from Customer import Customer
from Responsible import Responsible
from Saving import Saving
from Check import Check
from Depositor import  Depositor
from Payment import Payment
from Loan import Loan
from Borrow import Borrow
class Main_window(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(Main_window,self).__init__(*args, **kwargs)
        self.setWindowTitle("bank system")
        self.setFixedWidth(800)
        self.setFixedHeight(400)

        # menu
        bank_info_menu = self.menuBar().addMenu("&bank_info")
        transaction_menu = self.menuBar().addMenu("&transaction")
        account_menu = transaction_menu.addMenu("&account")
        debt_menu = transaction_menu.addMenu("&debt")
        statistics_menu = self.menuBar().addMenu("&statistics")
        # menu action
        branch_action = QAction("branch",self)
        branch_action.setStatusTip("branch basic infomation")
        branch_action.triggered.connect(self.branch)
        bank_info_menu.addAction(branch_action)

        employee_action = QAction("employee", self)
        employee_action.setStatusTip("employee basic information ")
        employee_action.triggered.connect(self.employee)
        bank_info_menu.addAction(employee_action)

        depart_action = QAction("depart",self)
        depart_action.setStatusTip("depart basic information")
        depart_action.triggered.connect(self.depart)
        bank_info_menu.addAction(depart_action)

        customer_acction = QAction("customer",self)
        customer_acction.setStatusTip("customer basic information")
        customer_acction.triggered.connect(self.customer)
        bank_info_menu.addAction(customer_acction)

        responsible_action = QAction("responsible",self)
        responsible_action.setStatusTip("employee responsible for customer")
        responsible_action.triggered.connect(self.responsible)
        bank_info_menu.addAction(responsible_action)

        saving_action = QAction("saving", self)
        saving_action.setStatusTip("saving account")
        saving_action.triggered.connect(self.saving)
        account_menu.addAction(saving_action)

        check_action=QAction("check",self)
        check_action.setStatusTip("check account")
        check_action.triggered.connect(self.check)
        account_menu.addAction(check_action)

        depositor_action = QAction("depositor", self)
        depositor_action.setStatusTip("customer owns account")
        depositor_action.triggered.connect(self.depositor)
        account_menu.addAction(depositor_action)

        loan_action=QAction("loan",self)
        loan_action.setStatusTip("branch give loan")
        loan_action.triggered.connect(self.loan)
        debt_menu.addAction(loan_action)

        payment_action=QAction("payment",self)
        payment_action.setStatusTip("payment for loan")
        payment_action.triggered.connect(self.payment)
        debt_menu.addAction(payment_action)

        borrow_action=QAction("borrow",self)
        borrow_action.setStatusTip("customer borrow loan")
        borrow_action.triggered.connect(self.borrow)
        debt_menu.addAction(borrow_action)

        statistics_overall_action = QAction("yearly", self)
        statistics_overall_action.setStatusTip("yearly statistics")
        statistics_overall_action.triggered.connect(self.statistics_yearly)
        statistics_menu.addAction(statistics_overall_action)

        statistics_seasonly_action = QAction("seasonly", self)
        statistics_seasonly_action.setStatusTip("seasonly statistics")
        statistics_seasonly_action.triggered.connect(self.statistics_seasonly)
        statistics_menu.addAction(statistics_seasonly_action)

        statistics_monthly_action = QAction("monthly", self)
        statistics_monthly_action.setStatusTip("montly statistics")
        statistics_monthly_action.triggered.connect(self.statistics_monthly)
        statistics_menu.addAction(statistics_monthly_action)


        left_layout = QVBoxLayout()
        title = QLabel("Bank System")
        title_font = title.font()
        title_font.setPointSize(16)
        title.setFont(title_font)
        version = QLabel("(v3.0)")

        # left_layout.addStretch(1)
        title_version_layout = QHBoxLayout()
        title_version_layout.addWidget(title)
        title_version_layout.addWidget(version)
        title_version_layout.addStretch()
        left_layout.addLayout(title_version_layout)
        left_layout.addStretch()

        # right_layout=QVBoxLayout()

        self.p = QPalette()
        self.pixmap = QPixmap("img1.png").scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.p.setBrush(QPalette.Background, QBrush(self.pixmap))
        self.setPalette(self.p)


        layout = QHBoxLayout()
        layout.addLayout(left_layout)
        # layout.addLayout(right_layout)
        layout.addStretch(2)
        widget = QWidget()
        self.setCentralWidget(widget)
        widget.setLayout(layout)

    def branch(self):
        dlg = Branch()
        dlg.exec_()

    def employee(self):
        dlg = Employee()
        dlg.exec_()

    def depart(self):
        dlg = Depart()
        dlg.exec_()

    def customer(self):
        dlg = Customer()
        dlg.exec_()

    def responsible(self):
        dlg = Responsible()
        dlg.exec_()

    def saving(self):
        dlg = Saving()
        dlg.exec_()

    def check(self):
        dlg = Check()
        dlg.exec_()

    def depositor(self):
        dlg = Depositor()
        dlg.exec_()
    #
    def loan(self):
        dlg = Loan()
        dlg.exec_()

    def payment(self):
        dlg = Payment()
        dlg.exec_()

    def borrow(self):
        dlg = Borrow()
        dlg.exec_()
    #
    def statistics_yearly(self):
        # dlg = Statistics_Overall_Dialog()
        os.system("python Yearly.py")

    def statistics_seasonly(self):
        os.system("python Seasonly.py")

    def statistics_monthly(self):
        os.system("python Monthly.py")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    passdlg = Login()
    if(passdlg != None):
        window = Main_window()
        window.show()
    sys.exit(app.exec_())