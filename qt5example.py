import sys
from PyQt5 import QtWidgets, uic
import socket

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('ele.ui', self)

        self.button = self.findChild(QtWidgets.QPushButton, 'connectButton')
        self.button.clicked.connect(self.connectButtonPressed)

        self.disconnectButton = self.findChild(QtWidgets.QPushButton, 'disconnectButton')
        self.disconnectButton.clicked.connect(self.disconnectButtonPressed)

        self.show()

    def connectButtonPressed(self):
        ip = self.findChild(QtWidgets.QTextEdit, 'IPentry').toPlainText()
        port = int(self.findChild(QtWidgets.QTextEdit, 'port_entry').toPlainText())
        mac = self.findChild(QtWidgets.QTextEdit, 'mac_entry').toPlainText()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))
        print(f"Connected to {ip}:{port}")

    def disconnectButtonPressed(self):
        self.sock.close()
        print("Disconnected")

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
