from PyQt5.Qt import *


class Ui_change_passwd(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 150)
        self.uname_lineEdit = QLineEdit(Dialog)
        self.uname_lineEdit.setPlaceholderText("Адрес электронной почты")
        self.uname_lineEdit.setGeometry(QRect(70, 50, 150, 20))
        self.uname_lineEdit.setObjectName("uname_lineEdit")
        self.signup_btn = QPushButton(Dialog)
        self.signup_btn.setGeometry(QRect(60, 80, 100, 23))
        self.signup_btn.setObjectName("login_btn")
        self.cansel_btn = QPushButton(Dialog)
        self.cansel_btn.setGeometry(QRect(170, 80, 51, 23))
        self.cansel_btn.setObjectName("cansel_btn")
        self.label = QLabel(Dialog)
        self.label.setGeometry(QRect(20, 5, 300, 51))
        font = QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Телефонная книжка - смена паролья"))
        self.signup_btn.setText(_translate("Dialog", "Сменить пароль"))
        self.cansel_btn.setText(_translate("Dialog", "Отмена"))
        self.label.setText(_translate("Dialog", "Восстановление пароля"))

class Change_passwd(QDialog, Ui_change_passwd):
    def __init__(self, parent=None):
        super(Change_passwd, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent

        self.signup_btn.clicked.connect(self.insertData)
        self.cansel_btn.clicked.connect(self.close)

    @pyqtSlot()
    def insertData(self):
        username = self.uname_lineEdit.text()
        password = self.password_lineEdit.text()

        if (not username) or (not password):
            msg = QMessageBox.information(self, 'Внимание!', 'Вы не заполнили все поля.')
            return

        result = self.parent.loginDatabase.conn.execute("SELECT * FROM USERS WHERE USERNAME = ?", (username,))
        if result.fetchall():
            msg = QMessageBox.information(self, 'Внимание!', 'Пользоватеть с таким именем уже зарегистрирован.')
        else:
            self.parent.loginDatabase.conn.execute("INSERT INTO USERS VALUES(?, ?, ?)",
                                                   (username, password))
            self.parent.loginDatabase.conn.commit()
            self.close()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = Dialog()
    w.show()
    sys.exit(app.exec_())