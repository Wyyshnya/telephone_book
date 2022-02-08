from PyQt5.Qt import *

from adder import adderU
from database import DataBase


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(452, 290)
        self.active = None
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setGeometry(QRect(0, 0, 231, 51))
        self.table = QTableWidget(MainWindow)
        self.table.setGeometry(QRect(40, 30, 417, 239))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ФИО", "Номер телефона", "Дата рождения"])
        self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
        self.table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignRight)
        font = QFont()
        self.grid_layout = QGridLayout()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignRight)
        self.label.setObjectName("label")
        self.button_add = QPushButton(MainWindow)
        self.button_add.setGeometry(QRect(100, 0, 60, 23))
        MainWindow.setCentralWidget(self.centralwidget)
        self.but_group = QButtonGroup(MainWindow)
        self.button1 = QPushButton(MainWindow)
        self.button1.setGeometry(QRect(0, 0, 40, 23))
        self.button2 = QPushButton(MainWindow)
        self.button2.setGeometry(QRect(0, 22, 40, 23))
        self.button3 = QPushButton(MainWindow)
        self.button3.setGeometry(QRect(0, 44, 40, 23))
        self.button4 = QPushButton(MainWindow)
        self.button4.setGeometry(QRect(0, 66, 40, 23))
        self.button5 = QPushButton(MainWindow)
        self.button5.setGeometry(QRect(0, 88, 40, 23))
        self.button6 = QPushButton(MainWindow)
        self.button6.setGeometry(QRect(0, 110, 40, 23))
        self.button7 = QPushButton(MainWindow)
        self.button7.setGeometry(QRect(0, 132, 40, 23))
        self.button8 = QPushButton(MainWindow)
        self.button8.setGeometry(QRect(0, 154, 40, 23))
        self.button9 = QPushButton(MainWindow)
        self.button9.setGeometry(QRect(0, 176, 40, 23))
        self.button10 = QPushButton(MainWindow)
        self.button10.setGeometry(QRect(0, 198, 40, 23))
        self.button11 = QPushButton(MainWindow)
        self.button11.setGeometry(QRect(0, 220, 40, 23))
        self.button12 = QPushButton(MainWindow)
        self.button12.setGeometry(QRect(0, 244, 40, 23))
        self.button13 = QPushButton(MainWindow)
        self.button13.setGeometry(QRect(0, 266, 40, 23))
        self.but_group.addButton(self.button1, 1)
        self.but_group.addButton(self.button2, 2)
        self.but_group.addButton(self.button3, 3)
        self.but_group.addButton(self.button4, 4)
        self.but_group.addButton(self.button5, 5)
        self.but_group.addButton(self.button6, 6)
        self.but_group.addButton(self.button7, 7)
        self.but_group.addButton(self.button8, 8)
        self.but_group.addButton(self.button9, 9)
        self.but_group.addButton(self.button10, 10)
        self.but_group.addButton(self.button11, 11)
        self.but_group.addButton(self.button12, 12)
        self.but_group.addButton(self.button13, 13)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Телефонная книжка"))
        self.label.setText(_translate("MainWindow", "Зашли как"))
        self.button1.setText(_translate("MainWindow", "АБ"))
        self.button2.setText(_translate("MainWindow", "ВГ"))
        self.button3.setText(_translate("MainWindow", "ДЕ"))
        self.button4.setText(_translate("MainWindow", "ЖЗИЙ"))
        self.button5.setText(_translate("MainWindow", "КЛ"))
        self.button6.setText(_translate("MainWindow", "МН"))
        self.button7.setText(_translate("MainWindow", "ОП"))
        self.button8.setText(_translate("MainWindow", "РС"))
        self.button9.setText(_translate("MainWindow", "ТУ"))
        self.button10.setText(_translate("MainWindow", "ФХ"))
        self.button11.setText(_translate("MainWindow", "ЦЧШЩ"))
        self.button12.setText(_translate("MainWindow", "ЫЭ"))
        self.button13.setText(_translate("MainWindow", "ЮЯ"))
        self.button_add.setText(_translate("MainWindow", "Добавить"))


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, name, id_user):
        self.cursor = DataBase().cursor
        super().__init__()
        self.id_user = id_user
        self.setupUi(self)
        self.current = None
        self.previous = None
        self.label.setText('{} {}'.format(self.label.text(), name))
        gridLayout = QGridLayout(self.centralwidget)
        gridLayout.addWidget(self.label)
        self.but_group.idClicked.connect(self.handle_button_clicked)
        self.button_add.clicked.connect(self.adding)
        self.table.currentItemChanged.connect(self.current_item_changed)
        self.table.cellChanged.connect(self.cell_changed)
        self.cursor.execute("select * from book where id_user=?", (self.id_user,))
        self.nums = self.cursor.fetchall()

    def adding(self):
        self.addShow()

    def addShow(self):
        self.addShow = adderU(self)
        self.addShow.set_id(self.id_user)
        self.addShow.show()
        self.cursor.execute("select * from book where id_user=?", (self.id_user,))
        self.nums = self.cursor.fetchall()

    def handle_button_clicked(self, id_):
        if self.active:
            self.but_group.button(self.active).setStyleSheet("background: none;")
        self.active = id_
        self.but_group.button(id_).setStyleSheet("background: cyan;")
        self.set_data(id_)

    def set_data(self, id_):
        self.cursor.execute("select * from book where id_user=?", (self.id_user,))
        self.nums = self.cursor.fetchall()
        rows = []
        for num in self.nums:
            if num[4] == id_:
                rows.append(num)
        rows.sort(key=lambda x: (x[1]))
        self.table.setRowCount(len(rows))
        self.grid_layout.addWidget(self.table, 0, 0)
        for i in range(len(rows)):
            for j in range(3):
                if j != 2:
                    self.table.setItem(i, j, QTableWidgetItem(rows[i][j+1]))
                else:
                    widg = QDateEdit()
                    widg.setDisplayFormat("dd.MM.yyyy")
                    qdate= QDate.fromString(rows[i][j+1], "dd.MM.yyyy")
                    widg.setDate(qdate)
                    self.table.setCellWidget(i, j, widg)

    def cell_changed(self, row, column):
        print(f'\nИзменились данные элемента в ячейке, строка={row}, столбец={column}')
        if self.table.currentItem():
            self.prev = self.table.cellWidget(row, 2).text()
            if column == 0:
                self.cursor.execute("update book set fio=? where id_user=? and fio=? and telephone=? "
                                    "and data_birth=?", (self.table.currentItem().text(), self.id_user,
                                                         self.current, self.table.item(row, 1).text(),
                                                         self.table.cellWidget(row, 2).text(),))
            elif column == 1:
                self.cursor.execute("update book set telephone=? where id_user=? and fio=? and telephone=? "
                                   "and data_birth=?", (self.table.currentItem().text(), self.id_user,
                                                        self.table.item(row, 0).text(), self.current,
                                                        self.table.cellWidget(row, 2).text(),))
            elif self.table.cellWidget(row, 2).text() != self.prev:
                self.cursor.execute("update book set data_birth=? where id_user=? and fio=? and telephone=? "
                                    "and data_birth=?", (self.table.currentItem().text(), self.id_user,
                                                         self.table.item(row, 0).text(),
                                                         self.table.cellWidget(row, 2).text(), self.current,))

    def current_item_changed(self, current, previous):
        self.current = current.text() if current else ''
        self.previous = previous.text() if previous else ''


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())