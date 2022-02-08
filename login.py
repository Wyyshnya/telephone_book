from PyQt5.Qt import *

from welcome import MainWindow
from signup import Dialog
from change_passwd import Change_passwd
from database import DataBase


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 200)
        self.uname_lineEdit = QLineEdit(Dialog)
        self.uname_lineEdit.setPlaceholderText("Имя пользователя")
        self.uname_lineEdit.setGeometry(QRect(100, 50, 113, 20))
        self.uname_lineEdit.setObjectName("uname_lineEdit")
        self.pass_lineEdit = QLineEdit(Dialog)
        self.pass_lineEdit.setEchoMode(QLineEdit.Password)
        self.pass_lineEdit.setGeometry(QRect(100, 80, 113, 20))
        self.pass_lineEdit.setObjectName("pass_lineEdit")
        self.pass_lineEdit.setPlaceholderText("Пароль")
        self.login_btn = QPushButton(Dialog)
        self.login_btn.setGeometry(QRect(90, 110, 51, 23))
        self.login_btn.setObjectName("login_btn")
        self.signup_btn = QPushButton(Dialog)
        self.signup_btn.setGeometry(QRect(145, 110, 80, 23))
        self.signup_btn.setObjectName("signup_btn")
        self.label = QLabel(Dialog)
        self.label.setGeometry(QRect(80, 5, 211, 51))
        font = QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.remember_me_chkbx = QCheckBox(Dialog)
        self.remember_me_chkbx.setGeometry(QRect(120, 130, 100, 30))
        self.remember_me_chkbx.setObjectName("remember_me_chkbx")
        self.show_passwd = QCheckBox(Dialog)
        self.show_passwd.setGeometry(QRect(120, 150, 100, 30))
        self.show_passwd.setObjectName("show_passwd")
        self.passwd_rem = QPushButton(Dialog)
        self.passwd_rem.setGeometry(QRect(120, 170, 100, 23))
        self.passwd_rem.setObjectName("passwd_rem")
        self.passwd_rem.setStyleSheet("background: none; border: none; text-decoration: underline; color: blue;")

        self.retranslateUi(Dialog)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Телефонная книжка - вход"))
        self.login_btn.setText(_translate("Dialog", "Войти"))
        self.signup_btn.setText(_translate("Dialog", "Регистрация"))
        self.passwd_rem.setText(_translate("Dialog", "Забыли пароль?"))
        self.remember_me_chkbx.setText(_translate("Dialog", "Запомнить меня"))
        self.show_passwd.setText(_translate("Dialog", "Показать пароль"))
        self.label.setText(_translate("Dialog", "Авторизация"))


class MainDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)
        self.setupUi(self)
        self.cursor = DataBase().cursor
        self.login_btn.clicked.connect(self.loginCheck)
        self.signup_btn.clicked.connect(self.signUpCheck)
        self.passwd_rem.clicked.connect(self.change_passwd)

    def showMessageBox(self, title, message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()

    def welcomeWindowShow(self, username, id):
        self.welcomeWindow = MainWindow(username, id)
        self.welcomeWindow.show()

    def change_passwd_show(self):
        self.change_passwdWindow = Change_passwd(self)
        self.change_passwdWindow.show()

    def signUpShow(self):
        self.signUpWindow = Dialog(self)
        self.signUpWindow.show()

    def loginCheck(self):
        username = self.uname_lineEdit.text()
        password = self.pass_lineEdit.text()
        if (not username) or (not password):
            msg = QMessageBox.information(self, 'Внимание!', 'Вы не заполнили все поля.')
            return

        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = self.cursor.fetchone()
        from werkzeug.security import generate_password_hash, check_password_hash
        if check_password_hash(user[2], password):
            self.welcomeWindowShow(username, user[0])
            self.hide()
        else:
            self.showMessageBox('Внимание!', 'Неправильное имя пользователя или пароль.')

    def signUpCheck(self):
        self.signUpShow()

    def change_passwd(self):
        self.change_passwd_show()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = MainDialog()
    w.show()
    sys.exit(app.exec_())