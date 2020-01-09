import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from release.new import Ui_MainWindow
from release.addEditCoffeeForm import Ui_Form


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.con = sqlite3.connect('coffee.db')
        cur = self.con.cursor()
        self.result = cur.execute('SELECT * FROM sorts').fetchall()
        if self.result:
            self.tableWidget.setRowCount(len(self.result))
            self.tableWidget.setColumnCount(len(self.result[0]))
            self.tableWidget.setHorizontalHeaderLabels(['id', 'название сорта', 'степень обжарки', 'молотый/в зернах',
                                                        'описание вкуса', 'цена', 'объем упаковки'])
            for i, row in enumerate(self.result):
                for j, col in enumerate(row):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(col)))
            self.tableWidget.resizeColumnsToContents()
        self.pushButton.clicked.connect(self.adding)
        self.pushButton_2.clicked.connect(self.editing)

    def showing(self, result):
        self.result = result
        if self.result:
            self.tableWidget.setRowCount(len(self.result))
            self.tableWidget.setColumnCount(len(self.result[0]))
            self.tableWidget.setHorizontalHeaderLabels(['id', 'название сорта', 'степень обжарки', 'молотый/в зернах',
                                                        'описание вкуса', 'цена', 'объем упаковки'])
            for i, row in enumerate(self.result):
                for j, col in enumerate(row):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(col)))
            self.tableWidget.resizeColumnsToContents()

    def adding(self):
        self.otherwindow = Addition()
        self.otherwindow.show()
        self.con = sqlite3.connect('coffee.db')
        cur = self.con.cursor()
        self.result = cur.execute('SELECT * FROM sorts').fetchall()
        self.showing(self.result)

    def editing(self):
        res = self.tableWidget.selectedItems()
        if len(res) == 0:
            QMessageBox.question(self, 'Сообщение', 'Запись не выбрана',
                                 QMessageBox.Ok)
        else:
            self.otherwindow = Redaction()
            self.otherwindow.show()
            self.con = sqlite3.connect('coffee.db')
            cur = self.con.cursor()
            self.result = cur.execute('SELECT * FROM sorts').fetchall()
            self.showing(self.result)


class Redaction(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.show()
        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.closing)

    def run(self):
        self.id = self.lineEdit.text()
        self.name = self.lineEdit_2.text()
        self.step = self.lineEdit_3.text()
        self.mol = self.lineEdit_4.text()
        self.op = self.lineEdit_5.text()
        self.price = self.lineEdit_6.text()
        self.val = self.lineEdit_7.text()
        self.con = sqlite3.connect('coffee.db')
        cur = self.con.cursor()
        cur.execute('''UPDATE sorts
                       SET id = ?,
                       [название сорта] = ?, [степень обжарки] = ?,
                       [молотый/в зернах] = ?, [описание вкуса] = ?,
                       цена = ?, [объем упаковки] = ?
                       WHERE id = ?''',
                    (self.id, self.name, self.step, self.mol,
                     self.op, self.price, self.val, self.id))
        self.con.commit()
        result = cur.execute('SELECT * FROM sorts').fetchall()
        ex.showing(result)
        self.close()

    def closing(self):
        self.close()


class Addition(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.show()
        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.closing)

    def run(self):
        self.id = self.lineEdit.text()
        self.name = self.lineEdit_2.text()
        self.step = self.lineEdit_3.text()
        self.mol = self.lineEdit_4.text()
        self.op = self.lineEdit_5.text()
        self.price = self.lineEdit_6.text()
        self.val = self.lineEdit_7.text()
        self.con = sqlite3.connect('coffee.db')
        cur = self.con.cursor()
        cur.execute('''INSERT INTO sorts('id', 'название сорта', 'степень обжарки', 'молотый/в зернах',
                    'описание вкуса', 'цена', 'объем упаковки') VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (self.id, self.name, self.step, self.mol,
                     self.op, self.price, self.val))
        self.con.commit()
        result = cur.execute('SELECT * FROM sorts').fetchall()
        ex.showing(result)
        self.close()

    def closing(self):
        self.close()


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
