from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtSql import *
import sys
import ctypes
import os


class Depart(QDialog):
    def __init__(self, *args, **kwargs):
        super(Depart, self).__init__(*args, **kwargs)
        self.setWindowTitle("Depart")
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
        self.model.setTable('depart')

        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)

        self.model.setHeaderData(0, Qt.Horizontal, "depart_id")
        self.model.setHeaderData(1, Qt.Horizontal, "depart_name")
        self.model.setHeaderData(2, Qt.Horizontal, "depart_type")
        self.model.setHeaderData(3, Qt.Horizontal, "manager_id")
        self.tableWidget.setModel(self.model)
        self.tableWidget.setItemDelegate(QSqlRelationalDelegate(self.tableWidget))

        self.depart_id_label = QLabel("depart_id")
        self.depart_id_edit = QLineEdit()

        self.depart_name_label = QLabel("depart_name")
        self.depart_name_edit = QLineEdit()

        self.depart_type_label = QLabel("depart_type")
        self.depart_type_edit = QLineEdit()

        self.manager_id_label = QLabel("manager_id")
        self.manager_id_edit  = QLineEdit()

        self.query_button = QPushButton("query")
        self.query_button.clicked.connect(self.query_event)
        self.update_button = QPushButton("update")
        self.update_button.clicked.connect(self.update_event)
        self.add_button = QPushButton("add")
        self.add_button.clicked.connect(self.add_event)
        self.delete_button = QPushButton("delete")
        self.delete_button.clicked.connect(self.delete_event)

        self.head_layout = QGridLayout()
        self.head_layout.addWidget(self.depart_id_label, 0, 0)
        self.head_layout.addWidget(self.depart_id_edit, 0, 1)
        self.head_layout.addWidget(self.depart_name_label, 0, 2)
        self.head_layout.addWidget(self.depart_name_edit, 0, 3)
        self.head_layout.addWidget(self.depart_type_label, 1, 0)
        self.head_layout.addWidget(self.depart_type_edit, 1, 1)
        self.head_layout.addWidget(self.manager_id_label,1,2)
        self.head_layout.addWidget(self.manager_id_edit,1,3)

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
        if self.depart_id_edit.text() != "":
            select_string += "depart_id=" + "'" + self.depart_id_edit.text() + "'"

        if self.depart_name_edit.text() != "":
            if select_string != "":
                select_string += " and depart_name=" + "'" + self.depart_name_edit.text() + "'"
            else:
                select_string += "depart_name=" + "'" + self.depart_name_edit.text() + "'"

        if self.depart_type_edit.text() != "":
            if select_string != "":
                select_string += " and depart_type= " + self.depat_type_edit.text()
            else:
                select_string += "depart= " + self.depart_type_edit.text()

        if self.manager_id_edit.text() != "":
            if select_string != "":
                select_string += " and manager_id= " + self.manager_id_edit.text()
            else:
                select_string += "manager_id= " + self.manager_id_edit.text()
        print(select_string)
        self.model.setFilter(select_string)
        self.model.select()

    def update_event(self):
        if self.tableWidget.currentIndex().row() > -1:
            record = self.model.record(self.tableWidget.currentIndex().row())
            record.setValue("depart_id", self.depart_id_edit.text())
            record.setValue("depart_name", self.depart_name_edit.text())
            record.setValue("depart_type", self.depart_type_edit.text())
            record.setValue("manager_id", self.manager_id_edit.text())
            if not self.model.setRecord(self.tableWidget.currentIndex().row(), record):
                QMessageBox.warning(QMessageBox(), 'Error', self.model.lastError().text())
        else:
            QMessageBox.question(self, 'Message', "Please select a row would you like to update.", QMessageBox.Ok)
            self.show()
        self.model.select()

    def add_event(self):
        row = self.model.rowCount()
        self.model.insertRows(row, 1)
        self.model.setData(self.model.index(row, 0), self.depart_id_edit.text())
        self.model.setData(self.model.index(row, 1), self.depart_name_edit.text())
        self.model.setData(self.model.index(row, 2), self.depart_type_edit.text())
        self.model.setData(self.model.index(row, 3), self.manager_id_edit.text())
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


