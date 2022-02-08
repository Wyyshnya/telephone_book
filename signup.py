from PyQt5.Qt import *


class Ui_signUp(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 200)
        self.uname_lineEdit = QLineEdit(Dialog)
        self.uname_lineEdit.setPlaceholderText("Имя пользователя")
        self.uname_lineEdit.setGeometry(QRect(100, 50, 113, 20))
        self.uname_lineEdit.setObjectName("uname_lineEdit")
        self.password_lineEdit = QLineEdit(Dialog)
        self.password_lineEdit.setEchoMode(QLineEdit.Password)
        self.password_lineEdit.setGeometry(QRect(100, 80, 113, 20))
        self.password_lineEdit.setObjectName("pass_lineEdit")
        self.password_lineEdit.setPlaceholderText("Пароль")
        self.password1_lineEdit = QLineEdit(Dialog)
        self.password1_lineEdit.setEchoMode(QLineEdit.Password)
        self.password1_lineEdit.setGeometry(QRect(100, 110, 113, 20))
        self.password1_lineEdit.setObjectName("pass_lineEdit")
        self.password1_lineEdit.setPlaceholderText("Повторите пароль")
        self.date_birth = QDateEdit(Dialog)
        self.date_birth.setGeometry(QRect(100, 140, 113, 20))
        self.signup_btn = QPushButton(Dialog)
        self.signup_btn.setGeometry(QRect(100, 170, 51, 23))
        self.signup_btn.setObjectName("login_btn")
        self.cansel_btn = QPushButton(Dialog)
        self.cansel_btn.setGeometry(QRect(160, 170, 51, 23))
        self.cansel_btn.setObjectName("cansel_btn")
        self.label = QLabel(Dialog)
        self.label.setGeometry(QRect(80, 5, 211, 51))
        font = QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Телефонная книжка - регистрация"))
        self.signup_btn.setText(_translate("Dialog", "Ок"))
        self.cansel_btn.setText(_translate("Dialog", "Отмена"))
        self.label.setText(_translate("Dialog", "Регистрация"))


class Dialog(QDialog, Ui_signUp):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent

        self.signup_btn.clicked.connect(self.insertData)
        self.cansel_btn.clicked.connect(self.close)

    @pyqtSlot()
    def insertData(self):
        username = self.uname_lineEdit.text()
        password = self.password_lineEdit.text()
        password1 = self.password1_lineEdit.text()
        data_birth = self.date_birth.text()
        if password1 != password:
            msg = QMessageBox.information(self, 'Внимание!', 'Пароли не совпадают.')
            return
        if (not username) or (not password):
            msg = QMessageBox.information(self, 'Внимание!', 'Вы не заполнили все поля.')
            return

        self.parent.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        try:
            user = self.parent.cursor.fetchone()[1]
            msg = QMessageBox.information(self, 'Внимание!', 'Пользоватеть с таким именем уже зарегистрирован.')
        except Exception as err:
            from werkzeug.security import generate_password_hash
            passwd = generate_password_hash(password)
            self.parent.cursor.execute("INSERT INTO users (username, password, data_birth) VALUES(?, ?, ?)",
                                                   (username, passwd, data_birth,))
            self.close()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = Dialog()
    w.show()
    sys.exit(app.exec_())