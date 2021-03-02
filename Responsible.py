from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtSql import *
import sys
import ctypes
import os

class Responsible(QDialog):
    def __init__(self, *args, **kwargs):
        super(Responsible, self).__init__(*args, **kwargs)
        self.setWindowTitle("Responsible")
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
        self.model.setTable('responsible')
        # self.model.setRelation(0, QSqlRelation("employee", "employee_id", "name"))
        # self.model.setRelation(1, QSqlRelation("customer", "customer_id", "name"))
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)

        self.model.setHeaderData(0, Qt.Horizontal, "employee_id")
        self.model.setHeaderData(1, Qt.Horizontal, "customer_id")
        self.model.setHeaderData(2, Qt.Horizontal, "type")

        self.tableWidget.setModel(self.model)
        self.tableWidget.setItemDelegate(QSqlRelationalDelegate(self.tableWidget))

        self.employee_id_label = QLabel("employee_id")
        self.employee_id_edit = QLineEdit()

        self.customer_id_label = QLabel("customer_id")
        self.customer_id_edit = QLineEdit()

        self.type_label = QLabel("type")
        self.type_edit = QLineEdit()

        self.query_button = QPushButton("query")
        self.query_button.clicked.connect(self.query_event)
        self.update_button = QPushButton("update")
        self.update_button.clicked.connect(self.update_event)
        self.add_button = QPushButton("add")
        self.add_button.clicked.connect(self.add_event)
        self.delete_button = QPushButton("delete")
        self.delete_button.clicked.connect(self.delete_event)

        self.head_layout = QGridLayout()
        self.head_layout.addWidget(self.employee_id_label, 0, 0)
        self.head_layout.addWidget(self.employee_id_edit, 0, 1)
        self.head_layout.addWidget(self.customer_id_label, 0, 2)
        self.head_layout.addWidget(self.customer_id_edit, 0, 3)
        self.head_layout.addWidget(self.type_label, 1, 0)
        self.head_layout.addWidget(self.type_edit, 1, 1)

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

        if self.employee_id_edit.text() != "":
            select_string += "employee_id=" + "'" + self.employee_id_edit.text() + "'"

        if self.customer_id_edit.text() != "":
            if select_string != "":
                select_string += " and customer_id=" + "'" + self.customer_id_edit.text() + "'"
            else:
                select_string += "customer_id=" + "'" + self.customer_id_edit.text() + "'"

        if self.type_edit.text() != "":
            if select_string != "":
                select_string += " and type=" + "'" + self.type_edit.text() + "'"
            else:
                select_string += "type=" + "'" + self.type_edit.text() + "'"

        self.model.setFilter(select_string)
        self.model.select()

    def update_event(self):
        if self.tableWidget.currentIndex().row() > -1:
            record = self.model.record(self.tableWidget.currentIndex().row())
            record.setValue("employee_id", self.employee_id_edit.text())
            record.setValue("customer_id", self.customer_id_edit.text())
            record.setValue("type", self.type_edit.text())

            if not self.model.setRecord(self.tableWidget.currentIndex().row(), record):
                QMessageBox.warning(QMessageBox(), 'Error', self.model.lastError().text())
        else:
            QMessageBox.question(self, 'Message', "Please select a row would you like to update.", QMessageBox.Ok)
            self.show()
        self.model.select()

    def add_event(self):
        row = self.model.rowCount()
        self.model.insertRows(row, 1)
        self.model.setData(self.model.index(row, 0), self.employee_id_edit.text())
        self.model.setData(self.model.index(row, 1), self.customer_id_edit.text())
        self.model.setData(self.model.index(row, 2), self.type_edit.text())

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