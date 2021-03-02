from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtSql import *
import sys
import ctypes
import os



class Customer(QDialog):
    def __init__(self, *args, **kwargs):
        super(Customer, self).__init__(*args, **kwargs)
        self.setWindowTitle("Customer")
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
        self.model.setTable('customer')
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)

        self.model.setHeaderData(0, Qt.Horizontal, "customer_id")
        self.model.setHeaderData(1, Qt.Horizontal, "name")
        self.model.setHeaderData(2, Qt.Horizontal, "phone")
        self.model.setHeaderData(3, Qt.Horizontal, "address")
        self.model.setHeaderData(4, Qt.Horizontal, "contact_name")
        self.model.setHeaderData(5, Qt.Horizontal, "contact_phone")
        self.model.setHeaderData(6, Qt.Horizontal, "contact_email")
        self.model.setHeaderData(7, Qt.Horizontal, "contact_relation")

        self.tableWidget.setModel(self.model)
        self.tableWidget.setItemDelegate(QSqlRelationalDelegate(self.tableWidget))

        self.customer_id_label = QLabel("customer_id")
        self.customer_id_edit = QLineEdit()

        self.name_label = QLabel("name")
        self.name_edit = QLineEdit()

        self.phone_label = QLabel("phone")
        self.phone_edit = QLineEdit()

        self.address_label = QLabel("address")
        self.address_edit = QLineEdit()

        self.contact_name_label = QLabel("contact_name")
        self.contact_name_edit = QLineEdit()

        self.contact_phone_label = QLabel("contact_phone")
        self.contact_phone_edit = QLineEdit()

        self.contact_email_label = QLabel("contact_email")
        self.contact_email_edit = QLineEdit()

        self.contact_relation_label = QLabel("contact_relation")
        self.contact_relation_edit = QLineEdit()

        self.query_button = QPushButton("query")
        self.query_button.clicked.connect(self.query_event)
        self.update_button = QPushButton("update")
        self.update_button.clicked.connect(self.update_event)
        self.add_button = QPushButton("add")
        self.add_button.clicked.connect(self.add_event)
        self.delete_button = QPushButton("delete")
        self.delete_button.clicked.connect(self.delete_event)

        self.head_layout = QGridLayout()
        self.head_layout.addWidget(self.customer_id_label, 0, 0)
        self.head_layout.addWidget(self.customer_id_edit, 0, 1)
        self.head_layout.addWidget(self.name_label, 0, 2)
        self.head_layout.addWidget(self.name_edit, 0, 3)
        self.head_layout.addWidget(self.phone_label, 1, 0)
        self.head_layout.addWidget(self.phone_edit, 1, 1)
        self.head_layout.addWidget(self.address_label, 1, 2)
        self.head_layout.addWidget(self.address_edit, 1, 3)
        self.head_layout.addWidget(self.contact_name_label, 2, 0)
        self.head_layout.addWidget(self.contact_name_edit, 2, 1)
        self.head_layout.addWidget(self.contact_phone_label, 2, 2)
        self.head_layout.addWidget(self.contact_phone_edit, 2, 3)
        self.head_layout.addWidget(self.contact_email_label, 3, 0)
        self.head_layout.addWidget(self.contact_email_edit, 3, 1)
        self.head_layout.addWidget(self.contact_relation_label, 3, 2)
        self.head_layout.addWidget(self.contact_relation_edit, 3, 3)

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
        self.setMinimumSize(900, 600)

        self.model.select()

    def query_event(self):
        select_string = ""

        if self.customer_id_edit.text() != "":
            select_string += "customer_id=" + "'" + self.customer_id_edit.text() + "'"

        if self.name_edit.text() != "":
            if select_string != "":
                select_string += " and name=" + "'" + self.name_edit.text() + "'"
            else:
                select_string += "name=" + "'" + self.name_edit.text() + "'"

        if self.phone_edit.text() != "":
            if select_string != "":
                select_string += " and phone=" + "'" + self.phone_edit.text() + "'"
            else:
                select_string += "phone=" + "'" + self.phone_edit.text() + "'"

        if self.address_edit.text() != "":
            if select_string != "":
                select_string += " and address=" + "'" + self.address_edit.text() + "'"
            else:
                select_string += "address=" + "'" + self.address_edit.text() + "'"

        if self.contact_name_edit.text() != "":
            if select_string != "":
                select_string += " and contact_name=" + "'" + self.contact_name_edit.text() + "'"
            else:
                select_string += "contact_name=" + "'" + self.contact_name_edit.text() + "'"

        if self.contact_phone_edit.text() != "":
            if select_string != "":
                select_string += " and contact_phone=" + "'" + self.contact_phone_edit.text() + "'"
            else:
                select_string += "contact_phone=" + "'" + self.contact_phone_edit.text() + "'"

        if self.contact_email_edit.text() != "":
            if select_string != "":
                select_string += " and contact_email=" + "'" + self.contact_email_edit.text() + "'"
            else:
                select_string += "contact_email=" + "'" + self.contact_email_edit.text() + "'"

        if self.contact_relation_edit.text() != "":
            if select_string != "":
                select_string += " and contact_relation=" + "'" + self.contact_relation_edit.text() + "'"
            else:
                select_string += "contact_relation=" + "'" + self.contact_relation_edit.text() + "'"

        self.model.setFilter(select_string)
        self.model.select()

    def update_event(self):
        if self.tableWidget.currentIndex().row() > -1:
            record = self.model.record(self.tableWidget.currentIndex().row())
            record.setValue("customer_id", self.customer_id_edit.text())
            record.setValue("name", self.name_edit.text())
            record.setValue("phone", self.phone_edit.text())
            record.setValue("address", self.address_edit.text())
            record.setValue("contact_name", self.contact_name_edit.text())
            record.setValue("contact_phone", self.contact_phone_edit.text())
            record.setValue("contact_email", self.contact_email_edit.text())
            record.setValue("contact_relation", self.contact_relation_edit.text())

            if not self.model.setRecord(self.tableWidget.currentIndex().row(), record):
                QMessageBox.warning(QMessageBox(), 'Error', self.model.lastError().text())
        else:
            QMessageBox.question(self, 'Message', "Please select a row would you like to update.", QMessageBox.Ok)
            self.show()
        self.model.select()

    def add_event(self):
        row = self.model.rowCount()
        self.model.insertRows(row, 1)
        self.model.setData(self.model.index(row, 0), self.customer_id_edit.text())
        self.model.setData(self.model.index(row, 1), self.name_edit.text())
        self.model.setData(self.model.index(row, 2), self.phone_edit.text())
        self.model.setData(self.model.index(row, 3), self.address_edit.text())
        self.model.setData(self.model.index(row, 4), self.contact_name_edit.text())
        self.model.setData(self.model.index(row, 5), self.contact_phone_edit.text())
        self.model.setData(self.model.index(row, 6), self.contact_email_edit.text())
        self.model.setData(self.model.index(row, 7), self.contact_relation_edit.text())

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