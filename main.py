from PyQt5 import QtWidgets, uic
import sys
import connessione
import loadINI
import manualcommand

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('connessione.ui', self)

        ip, port, mac, commands = loadINI.load_config()
        self.IPentry.setText(ip)
        self.port_entry.setText(port)
        self.mac_entry.setText(mac)
        self.comboBox.addItems(commands)

        self.connection = connessione.Connection()  # Crea un'istanza della classe Connection

        #self.manual_commandbox = manualcommand.manua_commandbox(self)  # Crea un'istanza della classe manua_commandbox

        self.manua_commandbox.setEnabled(False)  # Disabilita manua_commandbox all'avvio

        self.show()

        self.disconnectButton.clicked.connect(self.disconnect)
        self.connectButton.clicked.connect(self.connect)

        self.sendcommand.clicked.connect(self.send_command)  # Connetti il segnale al metodo send_command


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
            self.manua_commandbox.setEnabled(True)  # Abilita manua_commandbox quando la connessione è stabilita
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
        self.manua_commandbox.setEnabled(False)  # Disabilita manua_commandbox quando la connessione viene chiusa

    def send_command(self):
        command = self.comboBox.currentText()
        channel = self.channelselection.value()
        manualcommand.send_command(self.connection, command, channel)
        #self.connection.connect(ip, port)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
