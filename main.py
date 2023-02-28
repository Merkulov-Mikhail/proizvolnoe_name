import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


name = "coffee.sqlite"


class My(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.conn = sqlite3.connect(name)
        self.cur = self.conn.cursor()
        self.funct()

    def funct(self):
        cnt = 0
        for name, obzh, stat, taste, price, size in self.cur.execute("SELECT * FROM coffee").fetchall():
            self.tableWidget.insertRow(cnt)
            self.tableWidget.setItem(cnt, 0, QTableWidgetItem(str(name)))
            self.tableWidget.setItem(cnt, 1, QTableWidgetItem(str(obzh)))
            self.tableWidget.setItem(cnt, 2, QTableWidgetItem(str(stat)))
            self.tableWidget.setItem(cnt, 3, QTableWidgetItem(str(taste)))
            self.tableWidget.setItem(cnt, 4, QTableWidgetItem(str(price)))
            self.tableWidget.setItem(cnt, 5, QTableWidgetItem(str(size)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = My()
    ex.show()
    sys.exit(app.exec_())

