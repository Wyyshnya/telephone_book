import random

from PyQt5.Qt import *


class Ui_adder(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 200)
        self.uname_lineEdit = QLineEdit(Dialog)
        self.uname_lineEdit.setPlaceholderText("Имя пользователя")
        self.uname_lineEdit.setGeometry(QRect(100, 10, 113, 20))
        self.uname_lineEdit.setObjectName("uname_lineEdit")
        self.num_lineEdit = QLineEdit(Dialog)
        self.num_lineEdit.setPlaceholderText("Номер телефона")
        self.num_lineEdit.setGeometry(QRect(100, 40, 113, 20))
        self.num_lineEdit.setObjectName("num_lineEdit")
        self.date_birth = QDateEdit(Dialog)
        self.date_birth.setGeometry(QRect(100, 100, 113, 20))
        self.signup_btn = QPushButton(Dialog)
        self.signup_btn.setGeometry(QRect(100, 170, 51, 23))
        self.signup_btn.setObjectName("add")
        self.cansel_btn = QPushButton(Dialog)
        self.cansel_btn.setGeometry(QRect(160, 170, 51, 23))
        self.cansel_btn.setObjectName("cansel_btn")

        self.retranslateUi(Dialog)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Телефонная книжка"))
        self.signup_btn.setText(_translate("Dialog", "Ок"))
        self.cansel_btn.setText(_translate("Dialog", "Отмена"))


class adderU(QDialog, Ui_adder):
    def __init__(self, parent=None):
        super(adderU, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.id_user = None
        self.signup_btn.clicked.connect(self.insertData)
        self.cansel_btn.clicked.connect(self.close)

    def set_id(self, id):
        self.id_user = id

    @pyqtSlot()
    def insertData(self):
        username = self.uname_lineEdit.text()
        num = self.num_lineEdit.text()
        data_birth = self.date_birth.text()

        if (not username) or (not num) or (not data_birth):
            msg = QMessageBox.information(self, 'Внимание!', 'Вы не заполнили все поля.')
            return

        self.parent.cursor.execute("SELECT * FROM book WHERE fio = ? and telephone=? and data_birth=? and id_user=?",
                                   (username, num, data_birth, self.id_user))
        try:
            user = self.parent.cursor.fetchone()[1]
            msg = QMessageBox.information(self, 'Внимание!', 'Пользоватеть с таким именем уже есть.')
        except Exception as err:
            st = "A"
            id = random.randint(1, 13)
            if username[0] in "АБ":
                st = "АБ"
                id = 1
            elif username[0] in "ВГ":
                st = "ВГ"
                id = 2
            elif username[0] in "ДЕ":
                st = "ДЕ"
                id = 3
            elif username[0] in "ЖЗИЙ":
                st = "ЖЗИЙ"
                id = 4
            elif username[0] in "КЛ":
                st = "КЛ"
                id = 5
            elif username[0] in "МН":
                st = "МН"
                id = 6
            elif username[0] in "ОП":
                st = "ОП"
                id = 7
            elif username[0] in "РС":
                st = "РС"
                id = 8
            elif username[0] in "ТУ":
                st = "ТУ"
                id = 9
            elif username[0] in "ФХ":
                st = "ФХ"
                id = 10
            elif username[0] in "ЦЧШЩ":
                st = "ЦЧШЩ"
                id = 11
            elif username[0] in "ЬЫЪЭ":
                st = "ЬЫЪЭ"
                id = 12
            elif username[0] in "ЮЯ":
                st = "ЮЯ"
                id = 13
            self.parent.cursor.execute("INSERT INTO book (id_user, fio, telephone, data_birth, id_char) VALUES(?, ?, ?, ?, ?)",
                                                   (self.id_user, username, num, data_birth, id, ))
            msg = QMessageBox.information(self, 'Внимание!',
                                          f'Он записан на странице {st}.')
            self.close()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = adderU()
    w.show()
    sys.exit(app.exec_())