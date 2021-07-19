import json
import sys
import requests

from PyQt5.QtWidgets import QWidget, QApplication

from main_view import MainView
from ui.form_login import Ui_Form

url = 'http://127.0.0.1:8080/login'


class LoginView(QWidget, Ui_Form):

    def __init__(self):
        super(LoginView, self).__init__()
        self.setupUi(self)

    def login(self):
        cid = self.lineEdit.text()
        password = self.lineEdit_2.text()
        d = {'cid': cid, 'password': password}
        # d = {'cid': '1234', 'password': '123'}
        r = requests.post(url, json.dumps(d))
        if r.status_code == 200:
            r = json.loads(r.text)
            print(r)
            if r['result']:
                self.mainView = MainView(r)
                self.mainView.show()
                self.close()
            else:
                self.label_4.setText(r['reason'])
        else:
            print('服务器出现错误')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = LoginView()
    login.show()
    sys.exit(app.exec_())