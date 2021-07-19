import json
import threading

from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QMessageBox, QListWidgetItem
from websocket import create_connection
from ui.form_main import Ui_Form

ADDR = 'ws://127.0.0.1:8080/chat'
head_icon = 'icon/boy_48.png'


class MainView(QWidget, Ui_Form):

    def __init__(self, info):
        super(MainView, self).__init__()
        self.setupUi(self)
        print(info)
        self.cid = info['cid']
        self.name = info['name']
        self.contact = info['contact']
        self.ws = create_connection(ADDR)
        handshake = {'MsgType': 'handshake', 'cid': self.cid}
        self.ws.send(json.dumps(handshake))
        self.MR = MessageReceiver(self.ws)
        self.MR.signal.connect(self.dealMessage)
        self.MR.start()

        self.initView()

    def initView(self):
        png = QPixmap(head_icon)
        png.scaled(30, 30)
        self.label_2.setPixmap(png)
        self.label_3.setText(self.cid)
        self.label_4.setText(self.name)


    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.ws.close()

    def dealMessage(self, msg):
        print(msg)
        msgType = msg['MsgType']
        if msgType == 'system':
            if msg['code'] == 400:
                QMessageBox.information(self, '下线提醒', '有其他客户端登录，您被挤占下线了', QMessageBox.Yes)
                self.close()
            else:
                self.label_5.setText('已上线')
        elif msgType == 'chat':
            srcId = msg['SrcId']
            text = msg['text']
            self.listWidget_2.addItem(QListWidgetItem(text))

    def send(self):
        dct = {'MsgType': 'chat', 'cid': self.cid, 'DesId': '12345', 'text': self.textEdit.toPlainText()}
        self.ws.send(json.dumps(dct))


class MessageReceiver(QThread):

    stop = False
    signal = pyqtSignal(dict)

    def __init__(self, ws):
        super(MessageReceiver, self).__init__()
        self.ws = ws

    def run(self) -> None:
        while not self.stop:
            r = self.ws.recv()
            d = json.loads(r)
            self.signal.emit(d)
