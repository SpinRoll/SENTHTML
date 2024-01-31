from PyQt5 import QtWidgets, uic
import sys
import connessione
import loadINI

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('connessione.ui', self)

        ip, port, mac = loadINI.load_config()
        self.IPentry.setText(ip)
        self.port_entry.setText(port)
        self.mac_entry.setText(mac)

        self.connection = connessione.Connection()  # Crea un'istanza della classe Connection

        self.show()

        self.disconnectButton.clicked.connect(self.disconnect)
        self.connectButton.clicked.connect(self.connect)

    def connect(self):
        ip = self.IPentry.toPlainText()
        port = self.port_entry.toPlainText()
        # Aggiungi qui le altre informazioni necessarie
        status = self.connection.connect(ip, port)  # Utilizza l'istanza della classe Connection
        self.status.setPlainText(status)  # Imposta il testo del widget QTextEdit "status"

        if status == 'online':
            self.connectButton.setStyleSheet("background-color: lightgreen; opacity: 0.3")
            self.connectButton.setEnabled(False)
            self.disconnectButton.setEnabled(True)
        else:
            self.disconnectButton.setStyleSheet("background-color: lightcoral; opacity: 0.6")
            self.connectButton.setEnabled(True)
            self.disconnectButton.setEnabled(False)

    def disconnect(self):
        self.connection.disconnect()  # Utilizza l'istanza della classe Connection
        self.status.setPlainText('offline')  # Imposta il testo del widget QTextEdit "status"
        self.connectButton.setStyleSheet("")
        self.disconnectButton.setStyleSheet("")
        self.connectButton.setEnabled(True)
        self.disconnectButton.setEnabled(False)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
