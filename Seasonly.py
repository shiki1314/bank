# # -*- coding: utf-8 -*-
#
import sys
import pandas as pd
import pymysql
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtSql import *
from PyQt5.QtChart import *
if __name__ == "__main__":
    app = QApplication(sys.argv)

    ## 加上字符集参数，防止中文乱码
    dbconn=pymysql.connect(
      host="127.0.0.1",
      database="bank",
      user="root",
      password="l9254866486",
      port=3306
     )
    dict = {
      "合肥支行":0,
      "南京支行":1
    }
    # print(dict["合肥支行"])
    # 贷款
    month = []
    print(month)
    temp = []
    temp1 = []
    for i in range(12):
      point = [i+1, 0]
      temp.append(point)
      temp1.append(point)
    month.insert(0,temp)
    month.insert(1,temp1)
    # month[0][1]= [3,0]
    print(month)
    for i,s in enumerate([("01",  "03"), ("04", "06"), ("07", "09"),("10", "12")]):
      sqlcmd="select branch_name,sum(payment.amount) from payment,loan \
                  where payment.loan_id=loan.loan_id and payment_date >= '2020-%s 'and payment_date <= '2020-%s' group by branch_name;"% (
                s[0], s[1])
      #利用pandas 模块导入mysql数据
      a=pd.read_sql(sqlcmd,dbconn)
      # if not a.values.any() :
      #   print("1")
      #取前5行数据
      # b=a.head()
      # print(a.values)
      if a.values.any():
        for data in a.values:
          # print(dict[data[0]])
          # print(month[dict[data[0]]][i][1])
          # print(month[dict[data[0]]])
          month[dict[data[0]]][i] = [i+1,data[1]]
          # print(month)

    print(month)
    series = []
    for i in range(len(month)):
      series_here = QLineSeries()
      point_list = []
      for item in month[i]:
        point = QPointF(item[0],item[1])
        point_list.append(point)
      print(point_list)
      series_here.append(point_list)
      series_here.setName(list(dict.keys())[i])
      series.append(series_here)

    x_Aix = QValueAxis()  # 定义x轴，实例化
    x_Aix.setRange(1.00, 4.00)  # 设置量程
    x_Aix.setLabelFormat("%d")  # 设置坐标轴坐标显示方式，精确到小数点后两位
    x_Aix.setTickType(QValueAxis.TicksFixed)
    x_Aix.setTickCount(3)  # 设置x轴有几个量程
    x_Aix.setMinorTickCount(1)  # 设置每个单元格有几个小的分级

    y_Aix = QValueAxis()  # 定义y轴
    y_Aix.setRange(0.00, 300)
    y_Aix.setLabelFormat("%d")
    y_Aix.setTickType(QValueAxis.TicksFixed)
    y_Aix.setTickCount(20)
    y_Aix.setMinorTickCount(10)

    charView = QChartView()  # 定义charView，父窗体类型为 Window
    charView.setGeometry(0, 0, 800, 600)  # 设置charView位置、大小
    # charView.resize(800, 600)
    charView.setRenderHint(QPainter.Antialiasing)  # 抗锯齿

    charView.chart().addSeries(series[0])  # 添加折线
    charView.chart().addSeries(series[1])  # 添加折线

    charView.chart().setAxisX(x_Aix, series[0])  # 设置x轴属性
    charView.chart().setAxisX(x_Aix, series[1])
    charView.chart().setAxisY(y_Aix, series[0])  # 设置y轴属性
    charView.chart().setAxisY(y_Aix, series[1])
    charView.chart().createDefaultAxes() # 使用默认坐标系
    # charView.chart().setTitleBrush(QBrush(Qt.cyan))  # 设置标题笔刷
    charView.chart().setTitle("偿还贷款")  # 设置标题
    #表格
    tableWidget = QTableWidget()  # 创建一个表格

    tableWidget.setRowCount(4)
    tableWidget.setColumnCount(2)  # 12行2列

    tableWidget.setHorizontalHeaderLabels(['合肥支行', '南京支行'])
    tableWidget.setVerticalHeaderLabels(['1', '2', '3', '4', '5','6','7','8','9','10','11','12'])
    for i in range(12):
      print(month[0][i][1])
      tableWidget.setItem(i, 0, QTableWidgetItem(str(month[0][i][1])))
      tableWidget.setItem(i, 1, QTableWidgetItem(str(month[1][i][1])))


    # 用户
    month = []
    print(month)
    temp = []
    temp1 = []
    for i in range(12):
      point = [i + 1, 0]
      temp.append(point)
      temp1.append(point)
    month.insert(0, temp)
    month.insert(1, temp1)
    # month[0][1]= [3,0]
    print(month)
    for i, s in enumerate([("01", "03"), ("04", "06"), ("07", "09"), ("10", "12")]):
      sqlcmd = "select branch_name,count(borrow.customer_id) from payment,borrow,loan \
            where borrow.loan_id=loan.loan_id and payment.loan_id = loan.loan_id and payment.payment_date >= '2020-%s' and payment.payment_date <= '2020-%s' group by branch_name;"%(s[0],s[1])
      # 利用pandas 模块导入mysql数据
      a = pd.read_sql(sqlcmd, dbconn)
      # if not a.values.any() :
      #   print("1")
      # 取前5行数据
      # b=a.head()
      print(a.values)
      if a.values.any():
        for data in a.values:
          # print(dict[data[0]])
          # print(month[dict[data[0]]][i][1])
          # print(month[dict[data[0]]])
          month[dict[data[0]]][i] = [i + 1, data[1]]
          # print(month)

    print(month)
    series = []
    for i in range(len(month)):
      series_here = QLineSeries()
      point_list = []
      for item in month[i]:
        point = QPointF(item[0], item[1])
        point_list.append(point)
      print(point_list)
      series_here.append(point_list)
      series_here.setName(list(dict.keys())[i])
      series.append(series_here)

    x_Aix = QValueAxis()  # 定义x轴，实例化
    x_Aix.setRange(1.00, 4.00)  # 设置量程
    x_Aix.setLabelFormat("%d")  # 设置坐标轴坐标显示方式，精确到小数点后两位
    x_Aix.setTickType(QValueAxis.TicksFixed)
    x_Aix.setTickCount(3)  # 设置x轴有几个量程
    x_Aix.setMinorTickCount(1)  # 设置每个单元格有几个小的分级

    y_Aix = QValueAxis()  # 定义y轴
    y_Aix.setRange(0.00, 20)
    y_Aix.setLabelFormat("%d")
    y_Aix.setTickType(QValueAxis.TicksFixed)
    y_Aix.setTickCount(20)
    y_Aix.setMinorTickCount(10)

    charView_client = QChartView()  # 定义charView，父窗体类型为 Window
    charView_client.setGeometry(0, 0, 800, 600)  # 设置charView位置、大小
    # charView.resize(800, 600)
    charView_client.setRenderHint(QPainter.Antialiasing)  # 抗锯齿

    charView_client.chart().addSeries(series[0])  # 添加折线
    charView_client.chart().addSeries(series[1])  # 添加折线
    charView_client.chart().setAxisX(x_Aix, series[0])  # 设置x轴属性
    charView_client.chart().setAxisX(x_Aix, series[1])
    charView_client.chart().setAxisY(y_Aix, series[0])  # 设置y轴属性
    charView_client.chart().setAxisY(y_Aix, series[1])
    charView_client.chart().createDefaultAxes()  # 使用默认坐标系
    # charView.chart().setTitleBrush(QBrush(Qt.cyan))  # 设置标题笔刷
    charView_client.chart().setTitle("还贷用户人数")  # 设置标题

    # 表格
    tableWidget_client = QTableWidget()  # 创建一个表格

    tableWidget_client.setRowCount(4)
    tableWidget_client.setColumnCount(2)  # 12行2列

    tableWidget_client.setHorizontalHeaderLabels(['合肥支行', '南京支行'])
    tableWidget_client.setVerticalHeaderLabels(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])
    for i in range(12):
      print(month[0][i][1])
      tableWidget_client.setItem(i, 0, QTableWidgetItem(str(month[0][i][1])))
      tableWidget_client.setItem(i, 1, QTableWidgetItem(str(month[1][i][1])))

    #  储蓄
    month = []
    print(month)
    temp = []
    temp1 = []
    for i in range(12):
      point = [i + 1, 0]
      temp.append(point)
      temp1.append(point)
    month.insert(0, temp)
    month.insert(1, temp1)
    # month[0][1]= [3,0]
    print(month)
    for i, s in enumerate([("01", "03"), ("04", "06"), ("07", "09"), ("10", "12")]):
      sqlcmd = "select branch_name,sum(balance) from saving_account where open_date >= '2020-%s' and open_date <= '2020-%s'group by branch_name;"%(s[0],s[1])
      # 利用pandas 模块导入mysql数据
      a = pd.read_sql(sqlcmd, dbconn)
      # if not a.values.any() :
      #   print("1")
      # 取前5行数据
      # b=a.head()
      # print(a.values)
      if a.values.any():
        for data in a.values:
          # print(dict[data[0]])
          # print(month[dict[data[0]]][i][1])
          # print(month[dict[data[0]]])
          month[dict[data[0]]][i] = [i + 1, data[1]]
          # print(month)

    print(month)
    series = []
    for i in range(len(month)):
      series_here = QLineSeries()
      point_list = []
      for item in month[i]:
        point = QPointF(item[0], item[1])
        point_list.append(point)
      print(point_list)
      series_here.append(point_list)
      series_here.setName(list(dict.keys())[i])
      series.append(series_here)

    x_Aix = QValueAxis()  # 定义x轴，实例化
    x_Aix.setRange(1.00, 4.00)  # 设置量程
    x_Aix.setLabelFormat("%d")  # 设置坐标轴坐标显示方式，精确到小数点后两位
    x_Aix.setTickType(QValueAxis.TicksFixed)
    x_Aix.setTickCount(11)  # 设置x轴有几个量程
    x_Aix.setMinorTickCount(1)  # 设置每个单元格有几个小的分级

    y_Aix = QValueAxis()  # 定义y轴
    y_Aix.setRange(0.00, 20000)
    y_Aix.setLabelFormat("%d")
    y_Aix.setTickType(QValueAxis.TicksFixed)
    y_Aix.setTickCount(20)
    y_Aix.setMinorTickCount(10)

    charView_saving = QChartView()  # 定义charView，父窗体类型为 Window
    charView_saving.setGeometry(0, 0, 2400, 1800)  # 设置charView位置、大小
    # charView.resize(800, 600)
    charView_saving.setRenderHint(QPainter.Antialiasing)  # 抗锯齿

    charView_saving.chart().addSeries(series[0])  # 添加折线
    charView_saving.chart().addSeries(series[1])  # 添加折线

    charView_saving.chart().setAxisX(x_Aix, series[0])  # 设置x轴属性
    charView_saving.chart().setAxisX(x_Aix, series[1])
    charView_saving.chart().setAxisY(y_Aix, series[0])  # 设置y轴属性
    charView_saving.chart().setAxisY(y_Aix, series[1])
    charView_saving.chart().createDefaultAxes()  # 使用默认坐标系
    # charView.chart().setTitleBrush(QBrush(Qt.cyan))  # 设置标题笔刷
    charView_saving.chart().setTitle("储蓄")  # 设置标题

    tableWidget_saving = QTableWidget()  # 创建一个表格

    tableWidget_saving.setRowCount(4)
    tableWidget_saving.setColumnCount(2)  # 12行2列

    tableWidget_saving.setHorizontalHeaderLabels(['合肥支行', '南京支行'])
    tableWidget_saving.setVerticalHeaderLabels(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])
    for i in range(12):
      print(month[0][i][1])
      tableWidget_saving.setItem(i, 0, QTableWidgetItem(str(month[0][i][1])))
      tableWidget_saving.setItem(i, 1, QTableWidgetItem(str(month[1][i][1])))

    # 储蓄人数
    month = []
    print(month)
    temp = []
    temp1 = []
    for i in range(12):
      point = [i + 1, 0]
      temp.append(point)
      temp1.append(point)
    month.insert(0, temp)
    month.insert(1, temp1)
    # month[0][1]= [3,0]
    print(month)
    for i, s in enumerate([("01", "03"), ("04", "06"), ("07", "09"), ("10", "12")]):
      sqlcmd = "select branch_name,count(depositor.customer_id) from depositor,saving_account \
                where depositor.account_id =saving_account.account_id and saving_account.open_date >= '2020-%s' and saving_account.open_date <= '2020-%s' group by branch_name;"%(s[0],s[1])
      # 利用pandas 模块导入mysql数据
      a = pd.read_sql(sqlcmd, dbconn)
      # if not a.values.any() :
      #   print("1")
      # 取前5行数据
      # b=a.head()
      print(a.values)
      if a.values.any():
        for data in a.values:
          # print(dict[data[0]])
          # print(month[dict[data[0]]][i][1])
          # print(month[dict[data[0]]])
          month[dict[data[0]]][i] = [i + 1, data[1]]
          # print(month)

    print(month)
    series = []
    for i in range(len(month)):
      series_here = QLineSeries()
      point_list = []
      for item in month[i]:
        point = QPointF(item[0], item[1])
        point_list.append(point)
      print(point_list)
      series_here.append(point_list)
      series_here.setName(list(dict.keys())[i])
      series.append(series_here)

    x_Aix = QValueAxis()  # 定义x轴，实例化
    x_Aix.setRange(1.00, 4.00)  # 设置量程
    x_Aix.setLabelFormat("%d")  # 设置坐标轴坐标显示方式，精确到小数点后两位
    x_Aix.setTickType(QValueAxis.TicksFixed)
    x_Aix.setTickCount(11)  # 设置x轴有几个量程
    x_Aix.setMinorTickCount(1)  # 设置每个单元格有几个小的分级

    y_Aix = QValueAxis()  # 定义y轴
    y_Aix.setRange(0.00, 20)
    y_Aix.setLabelFormat("%d")
    y_Aix.setTickType(QValueAxis.TicksFixed)
    y_Aix.setTickCount(20)
    y_Aix.setMinorTickCount(10)

    charView_saving_client = QChartView()  # 定义charView，父窗体类型为 Window
    charView_saving_client.setGeometry(0, 0, 800, 600)  # 设置charView位置、大小
    # charView.resize(800, 600)
    charView_saving_client.setRenderHint(QPainter.Antialiasing)  # 抗锯齿

    charView_saving_client.chart().addSeries(series[0])  # 添加折线
    charView_saving_client.chart().addSeries(series[1])  # 添加折线
    charView_saving_client.chart().setAxisX(x_Aix, series[0])  # 设置x轴属性
    charView_saving_client.chart().setAxisX(x_Aix, series[1])
    charView_saving_client.chart().setAxisY(y_Aix, series[0])  # 设置y轴属性
    charView_saving_client.chart().setAxisY(y_Aix, series[1])
    charView_saving_client.chart().createDefaultAxes()  # 使用默认坐标系
    # charView.chart().setTitleBrush(QBrush(Qt.cyan))  # 设置标题笔刷
    charView_saving_client.chart().setTitle("储蓄用户人数")  # 设置标题

    # 表格
    tableWidget_saving_client = QTableWidget()  # 创建一个表格

    tableWidget_saving_client.setRowCount(4)
    tableWidget_saving_client.setColumnCount(2)  # 12行2列

    tableWidget_saving_client.setHorizontalHeaderLabels(['合肥支行', '南京支行'])
    tableWidget_saving_client.setVerticalHeaderLabels(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])
    for i in range(12):
      print(month[0][i][1])
      tableWidget_saving_client.setItem(i, 0, QTableWidgetItem(str(month[0][i][1])))
      tableWidget_saving_client.setItem(i, 1, QTableWidgetItem(str(month[1][i][1])))
    # charView.show()  # 显示charView
    window = QWidget()
    window.setGeometry(0,0,1000,1000)
    layout = QGridLayout()
    layout.addWidget(charView, 0, 0)
    layout.addWidget(tableWidget, 0, 1)
    layout.addWidget(charView_client, 1, 0)
    layout.addWidget(tableWidget_client, 1, 1)
    layout.addWidget(charView_saving,2,0)
    layout.addWidget(tableWidget_saving,2,1)
    layout.addWidget(charView_saving_client,3,0)
    layout.addWidget(tableWidget_saving_client,3,1)
    window.setLayout(layout)
    window.show()
sys.exit(app.exec_())

