from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtSql import *
import sys
import ctypes
import os
class Check(QDialog):
    def __init__(self, *args, **kwargs):
        super(Check, self).__init__(*args, **kwargs)
        self.setWindowTitle("Check Account")
        # ui
        self.tableWidget = QTableView()

        self.db = QSqlDatabase.addDatabase('QMYSQL')
        self.db.setHostName("127.0.0.1")
        self.db.setPort(3306)
        self.db.setUserName("root")
        self.db.setPassword("l9254866486")
        self.db.setDatabaseName("bank")
        # print(QSqlDatabase.drivers())
        if self.db.open():
            print("ok")
        else:
            print(self.db.lastError().text())

        self.model = QSqlRelationalTableModel()
        self.model.setTable('check_account')
        # self.model.setRelation(1, QSqlRelation("branch", "branch_name", "branch_name"))
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)

        self.model.setHeaderData(0, Qt.Horizontal, "account_id")
        self.model.setHeaderData(1, Qt.Horizontal, "branch_name")
        self.model.setHeaderData(2, Qt.Horizontal, "balance")
        self.model.setHeaderData(3, Qt.Horizontal, "open_date")
        self.model.setHeaderData(4, Qt.Horizontal, "overdraft")

        self.tableWidget.setModel(self.model)
        self.tableWidget.setItemDelegate(QSqlRelationalDelegate(self.tableWidget))

        self.account_id_label = QLabel("account_id")
        self.account_id_edit = QLineEdit()

        self.branch_name_label = QLabel("branch_name")
        self.branch_name_edit = QLineEdit()

        self.balance_label = QLabel("balance")
        self.balanceL_edit = QLineEdit()
        self.balanceL_edit.setPlaceholderText("lower")
        self.balanceU_edit = QLineEdit()
        self.balanceU_edit.setPlaceholderText("upper")

        self.open_date_label = QLabel("open_date")
        self.open_date_edit = QLineEdit()

        self.overdraft_label = QLabel("overdraft")
        self.overdraftL_edit = QLineEdit()
        self.overdraftL_edit.setPlaceholderText("lower")
        self.overdraftU_edit = QLineEdit()
        self.overdraftU_edit.setPlaceholderText("upper")

        self.view_button = QPushButton("query")
        self.view_button.clicked.connect(self.query_event)
        self.update_button = QPushButton("update")
        self.update_button.clicked.connect(self.update_event)
        self.add_button = QPushButton("add")
        self.add_button.clicked.connect(self.add_event)
        self.delete_button = QPushButton("delete")
        self.delete_button.clicked.connect(self.delete_event)

        self.head_layout = QGridLayout()
        self.head_layout.addWidget(self.account_id_label, 0, 0)
        self.head_layout.addWidget(self.account_id_edit, 0, 1)
        self.head_layout.addWidget(self.branch_name_label, 0, 2)
        self.head_layout.addWidget(self.branch_name_edit, 0, 3)
        self.head_layout.addWidget(self.balance_label, 1, 0)
        self.head_layout.addWidget(self.balanceL_edit, 1, 1)
        self.head_layout.addWidget(self.balanceU_edit, 1, 3)
        self.head_layout.addWidget(self.open_date_label, 2, 0)
        self.head_layout.addWidget(self.open_date_edit, 2, 1)
        self.head_layout.addWidget(self.overdraft_label, 3, 0)
        self.head_layout.addWidget(self.overdraftL_edit, 3, 1)
        self.head_layout.addWidget(self.overdraftU_edit, 3, 3)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.view_button)
        self.button_layout.addWidget(self.update_button)
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.delete_button)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.head_layout)
        self.layout.addLayout(self.button_layout)
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)
        self.setMinimumSize(800, 600)

        self.model.select()

    def query_event(self):
        select_string = ""

        if self.account_id_edit.text() != "":
            select_string += "account_id=" + "'" + self.account_id_edit.text() + "'"

        if self.branch_name_edit.text() != "":
            if select_string != "":
                select_string += " and branch_name=" + "'" + self.branch_name_edit.text() + "'"
            else:
                select_string += "branch_name=" + "'" + self.branch_name_edit.text() + "'"

        if self.balanceL_edit.text() != "":
            if select_string != "":
                select_string += " and balance >= " + self.balanceL_edit.text()
            else:
                select_string += "balance >= " + self.balanceL_edit.text()

        if self.balanceU_edit.text() != "":
            if select_string != "":
                select_string += " and balance <= " + self.balanceU_edit.text()
            else:
                select_string += "balance <= " + self.balanceU_edit.text()

        if self.open_date_edit.text() != "":
            if select_string != "":
                select_string += " and open_date=" + "'" + self.open_date_edit.text() + "'"
            else:
                select_string += "open_date=" + "'" + self.open_date_edit.text() + "'"

        if self.overdraftL_edit.text() != "":
            if select_string != "":
                select_string += " and overdraft >= " + self.overdraftL_edit.text()
            else:
                select_string += "overdraft >= " + self.overdraftL_edit.text()

        if self.overdraftU_edit.text() != "":
            if select_string != "":
                select_string += " and overdraft <= " + self.overdraftU_edit.text()
            else:
                select_string += "overdraft <= " + self.overdraftU_edit.text()

        self.model.setFilter(select_string)
        self.model.select()

    def update_event(self):
        if self.tableWidget.currentIndex().row() > -1:
            record = self.model.record(self.tableWidget.currentIndex().row())
            record.setValue("account_id", self.account_id_edit.text())
            record.setValue("branch_name", self.branch_name_edit.text())
            record.setValue("balance", self.balanceL_edit.text())
            record.setValue("open_date", self.open_date_edit.text())
            record.setValue("overdraft", self.overdraftL_edit.text())

            if not self.model.setRecord(self.tableWidget.currentIndex().row(), record):
                QMessageBox.warning(QMessageBox(), 'Error', self.model.lastError().text())
        else:
            QMessageBox.question(self, 'Message', "Please select a row would you like to update.", QMessageBox.Ok)
            self.show()
        self.model.select()

    def add_event(self):
        row = self.model.rowCount()
        self.model.insertRows(row, 1)
        self.model.setData(self.model.index(row, 0), self.account_id_edit.text())
        self.model.setData(self.model.index(row, 1), self.branch_name_edit.text())
        self.model.setData(self.model.index(row, 2), self.balanceL_edit.text())
        self.model.setData(self.model.index(row, 3), self.open_date_edit.text())
        self.model.setData(self.model.index(row, 4), self.overdraftL_edit.text())

        if not self.model.submitAll():
            QMessageBox.warning(QMessageBox(), 'Error', self.model.lastError().text())
        self.model.select()


    def delete_event(self):
        if self.tableWidget.currentIndex().row() > -1:
            if not self.model.removeRow(self.tableWidget.currentIndex().row()):
                QMessageBox.warning(QMessageBox(), 'Error', self.model.lastError().text())
            self.model.select()
        else:
            QMessageBox.question(self, 'Message', "Please select a row would you like to delete", QMessageBox.Ok)
            self.show()