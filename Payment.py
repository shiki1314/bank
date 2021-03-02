from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtSql import *
import sys
import ctypes
import os
from tkinter import messagebox
class Payment(QDialog):
    def __init__(self, *args, **kwargs):
        super(Payment, self).__init__(*args, **kwargs)
        self.setWindowTitle("Payment")
        # ui
        self.tableWidget = QTableView()

        self.db = QSqlDatabase.addDatabase('QMYSQL')
        self.db.setHostName("127.0.0.1")
        self.db.setPort(3306)
        self.db.setUserName("root")
        self.db.setPassword("l9254866486")
        self.db.setDatabaseName("bank")
        print("0")
        print(QSqlDatabase.drivers())
        if self.db.open():
            print("ok")
        else:
            print(self.db.lastError().text())

        self.model = QSqlRelationalTableModel()
        self.model.setTable('payment')
        # self.model.setRelation(0, QSqlRelation("loan", "loan_id", "loan_id"))
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)

        self.model.setHeaderData(0, Qt.Horizontal, "loan_id")
        self.model.setHeaderData(1, Qt.Horizontal, "payment_id")
        self.model.setHeaderData(2, Qt.Horizontal, "payment_date")
        self.model.setHeaderData(3, Qt.Horizontal, "amount")
        self.model.setHeaderData(4, Qt.Horizontal, "total")

        self.tableWidget.setModel(self.model)
        self.tableWidget.setItemDelegate(QSqlRelationalDelegate(self.tableWidget))

        self.loan_id_label = QLabel("loan_id")
        self.loan_id_edit = QLineEdit()

        self.payment_id_label = QLabel("payment_id")
        self.payment_id_edit = QLineEdit()

        self.payment_date_label = QLabel("payment_date")
        self.payment_date_edit = QLineEdit()

        self.amount_label = QLabel("amount")
        self.amountL_edit = QLineEdit()
        self.amountL_edit.setPlaceholderText("lower")
        self.amountU_edit = QLineEdit()
        self.amountU_edit.setPlaceholderText("upper")

        self.query_button = QPushButton("query")
        self.query_button.clicked.connect(self.query_event)
        self.update_button = QPushButton("update")
        self.update_button.clicked.connect(self.update_event)
        self.add_button = QPushButton("add")
        self.add_button.clicked.connect(self.add_event)
        self.delete_button = QPushButton("delete")
        self.delete_button.clicked.connect(self.delete_event)

        self.head_layout = QGridLayout()
        self.head_layout.addWidget(self.loan_id_label, 0, 0)
        self.head_layout.addWidget(self.loan_id_edit, 0, 1)
        self.head_layout.addWidget(self.payment_id_label, 0, 2)
        self.head_layout.addWidget(self.payment_id_edit, 0, 3)
        self.head_layout.addWidget(self.payment_date_label, 1, 0)
        self.head_layout.addWidget(self.payment_date_edit, 1, 1)
        self.head_layout.addWidget(self.amount_label, 2, 0)
        self.head_layout.addWidget(self.amountL_edit, 2, 1)
        self.head_layout.addWidget(self.amountU_edit, 2, 3)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.query_button)
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

        if self.loan_id_edit.text() != "":
            select_string += "loan_id=" + "'" + self.loan_id_edit.text() + "'"

        if self.payment_id_edit.text() != "":
            if select_string != "":
                select_string += " and payment_id=" + "'" + self.payment_id_edit.text() + "'"
            else:
                select_string += "payment_id=" + "'" + self.payment_id_edit.text() + "'"

        if self.payment_date_edit.text() != "":
            if select_string != "":
                select_string += " and payment_date=" + "'" + self.payment_date_edit.text() + "'"
            else:
                select_string += "payment_date=" + "'" + self.payment_date_edit.text() + "'"

        if self.amountL_edit.text() != "":
            if select_string != "":
                select_string += " and amount >= " + self.amountL_edit.text()
            else:
                select_string += "amount >= " + self.amountL_edit.text()

        if self.amountU_edit.text() != "":
            if select_string != "":
                select_string += " and amount <= " + self.amountU_edit.text()
            else:
                select_string += "amount <= " + self.amountU_edit.text()

        self.model.setFilter(select_string)
        self.model.select()

    def update_event(self):
        if self.tableWidget.currentIndex().row() > -1:
            query = QSqlQuery()
            query.exec("select amount,total from loan where loan_id =" + self.loan_id_edit.text()+";")
            query_update = QSqlQuery()
            query_update.exec("select amount from payment where loan_id = {} and payment_id = {};".format(self.loan_id_edit.text(),self.payment_id_edit.text()))
            amount = 0
            pay_amount = 0
            total = 0
            # print(query_update)
            while query_update.next():
                pay_amount = query_update.value(0)
                print(pay_amount)
            while query.next():
                amount = query.value(0)
                total = query.value(1)
                print(amount,total)
            if amount < (total+float(self.amountL_edit.text())-pay_amount):
                messagebox.showerror("error","修改后的还款总额多于借款")
                os.system("pause")
                exit()
            record = self.model.record(self.tableWidget.currentIndex().row())
            record.setValue("loan_id", self.loan_id_edit.text())
            record.setValue("payment_id", self.payment_id_edit.text())
            record.setValue("payment_date", self.payment_date_edit.text())
            record.setValue("amount", self.amountL_edit.text())

            if not self.model.setRecord(self.tableWidget.currentIndex().row(), record):
                QMessageBox.warning(QMessageBox(), 'Error', self.model.lastError().text())
        else:
            QMessageBox.question(self, 'Message', "Please select a row would you like to update.", QMessageBox.Ok)
            self.show()
        self.model.select()

    def add_event(self):
        query = QSqlQuery()
        query.exec("select amount,total from loan where loan_id =" + self.loan_id_edit.text()+";")
        print("select total from loan where loan_id =" + self.loan_id_edit.text())
        while query.next():
            if query.value(0) < (query.value(1) + float(self.amountL_edit.text())):
                messagebox.showinfo("Error","还款总额大于借款")
                os.system("pause")
                exit()
        row = self.model.rowCount()
        self.model.insertRows(row, 1)
        self.model.setData(self.model.index(row, 0), self.loan_id_edit.text())
        self.model.setData(self.model.index(row, 1), self.payment_id_edit.text())
        self.model.setData(self.model.index(row, 2), self.payment_date_edit.text())
        self.model.setData(self.model.index(row, 3), self.amountL_edit.text())


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