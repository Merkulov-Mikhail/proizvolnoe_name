import sys
import sqlite3
from addEditCoffeeForm import Ui_Dialog
from ui import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog

name = "data/coffee.sqlite"


class Dialog(QDialog, Ui_Dialog):
    def __init__(self, dat=None):
        super().__init__()
        self.setupUi(self)
        if dat is not None:
            self.lineEdit.setText(str(dat[1]))
            self.lineEdit_2.setText(str(dat[2]))
            self.lineEdit_3.setText(str(dat[3]))
            self.lineEdit_4.setText(str(dat[4]))
            self.lineEdit_5.setText(str(dat[5]))
            self.lineEdit_6.setText(str(dat[6]))

    def get_data(self):
        return self.lineEdit, self.lineEdit_2, self.lineEdit_3, self.lineEdit_4, self.lineEdit_5, self.lineEdit_6


class My(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.genres_x = None
        self.conn = sqlite3.connect(name)
        self.cur = self.conn.cursor()
        self.funct()
        self.pushButton.clicked.connect(self.magic1)
        self.pushButton_2.clicked.connect(self.magic2)
        self.tableWidget.cellClicked.connect(self.qwe)

    def magic1(self):
        dial = Dialog()
        if dial.exec_():
            name, obzh, stat, taste, price, size = dial.get_data()
            if name.text() and obzh.text() and stat.text() and taste.text() and price.text() and size.text():
                mx = max(self.cur.execute("SELECT id FROM coffee").fetchall())[0] + 1
                self.cur.execute(
                    f"INSERT INTO coffee(id, name, obzh, sta, taste, price, size) VALUES({mx}, '{name.text()}', '{obzh.text()}', '{stat.text()}', '{taste.text()}', {price.text()}, {size.text()})")
                self.conn.commit()
                self.funct()

    def magic2(self):
        if self.genres_x is None:
            return
        dial = Dialog(dat=self.cur.execute(f"SELECT * FROM coffee where id={self.genres_x}").fetchone())
        ans = dial.exec_()
        if ans:
            name, obzh, stat, taste, price, size = dial.get_data()
            self.cur.execute(
                f"UPDATE coffee SET name='{name.text()}', obzh='{obzh.text()}', sta='{stat.text()}', taste='{taste.text()}', price={price.text()}, size={size.text()} WHERE id={self.genres_x}")
            self.conn.commit()
            self.funct()

    def funct(self):
        cnt = 0
        self.tableWidget.setRowCount(0)
        for id, name, obzh, stat, taste, price, size in sorted(self.cur.execute("SELECT * FROM coffee").fetchall(),
                                                               key=lambda x: -x[0]):
            self.tableWidget.insertRow(cnt)
            self.tableWidget.setItem(cnt, 0, QTableWidgetItem(str(id)))
            self.tableWidget.setItem(cnt, 1, QTableWidgetItem(str(name)))
            self.tableWidget.setItem(cnt, 2, QTableWidgetItem(str(obzh)))
            self.tableWidget.setItem(cnt, 3, QTableWidgetItem(str(stat)))
            self.tableWidget.setItem(cnt, 4, QTableWidgetItem(str(taste)))
            self.tableWidget.setItem(cnt, 5, QTableWidgetItem(str(price)))
            self.tableWidget.setItem(cnt, 6, QTableWidgetItem(str(size)))

    def qwe(self, *args):
        self.genres_x = args[0]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = My()
    ex.show()
    sys.exit(app.exec_())
