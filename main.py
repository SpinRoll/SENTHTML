from PyQt5 import QtWidgets, uic
import sys
import connessione
import loadINI
import manualcommand
import setIP
import micro  #  importare il modulo micro

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
        self.LOG_BOX.setEnabled(False)  # Disabilita manua_commandbox all'avvio
        self.NewIP_box.setEnabled(False)  # Disabilita manua_commandbox all'avvio
        self.show()

        self.clear_log.clicked.connect(self.clear)  # Connetti il segnale al metodo clear_log
        self.disconnectButton.clicked.connect(self.disconnect)
        self.connectButton.clicked.connect(self.connect)

        self.sendcommand.clicked.connect(self.send_command)  # Connetti il segnale al metodo send_command

        self.set_newip_button.clicked.connect(self.set_ip_address)  # Aggiungi questa riga

        # Connetti i segnali dei pulsanti alle funzioni appropriate
        self.Micro_ENABLE.clicked.connect(lambda: self.handle_micro_button('ENPIC', self.Micro_ENABLE, "lightgreen"))
        self.Micro_DISABLE.clicked.connect(lambda: self.handle_micro_button('DISPIC', self.Micro_DISABLE, "red"))
        self.Micro_SLEEP.clicked.connect(lambda: self.handle_micro_button('SLEEPSV', self.Micro_SLEEP, "yellow"))
        self.Micro_WAKE.clicked.connect(lambda: self.handle_micro_button('WAKESV', self.Micro_WAKE, "lightblue"))

    def connect(self):
        ip = self.IPentry.toPlainText()
        port = self.port_entry.toPlainText()
        # Aggiungi qui le altre informazioni necessarie
        status = self.connection.connect(ip, port)  # Utilizza l'istanza della classe Connection
        self.status.setPlainText(status)  # Imposta il testo del widget QTextEdit "status"

        if status == 'online':
            self.connectButton.setStyleSheet("background-color: lightgreen; opacity: 0.3")
            self.disconnectButton.setStyleSheet("background-color: #FFFFFF; opacity: 0.6")
            self.connectButton.setEnabled(False)
            self.disconnectButton.setEnabled(True)
            self.manua_commandbox.setEnabled(True)  # Abilita manua_commandbox quando la connessione è stabilita
            self.LOG_BOX.setEnabled(True)  # abilita manua_commandbox all'avvio
            self.NewIP_box.setEnabled(True)  # abilita manua_commandbox all'avvio



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
        self.LOG_BOX.setEnabled(False)  # Disabilita manua_commandbox all'avvio
        self.NewIP_box.setEnabled(False)  # Disabilita manua_commandbox all'avvio

    def send_command(self):
        command = self.comboBox.currentText()
        channel = self.channelselection.value()
        response = manualcommand.send_command(self.connection, command, channel)
        #self.connection.connect(ip, port)
        self.textBrowser.append(response)  # Aggiungi la risposta al QTextBrowser

    def clear(self):
        self.textBrowser.clear()  # Cancella il QTextBrowser

    def set_ip_address(self):
        # Recupera i valori IP dai widget QTextEdit
        ip1 = self.ip.toPlainText()
        ip2 = self.ip_2.toPlainText()
        ip3 = self.ip_3.toPlainText()
        ip4 = self.ip_4.toPlainText()

        # Chiama la funzione set_ip in setIP.py
        response = setIP.set_ip(self.connection, ip1, ip2, ip3, ip4)

        # Aggiungi la risposta al QTextBrowser
        self.textBrowser.append(response)

    def handle_micro_button(self, command, button, color):
        result = micro.send_micro_command(self.connection, command)
        if "è stato impostato correttamente" in result:
            # Se il comando è stato impostato correttamente, colora il pulsante
            button.setStyleSheet(f"background-color: {color}")
            # Disabilita tutti i pulsanti
            self.Micro_ENABLE.setEnabled(False)
            self.Micro_DISABLE.setEnabled(False)
            self.Micro_SLEEP.setEnabled(False)
            self.Micro_WAKE.setEnabled(False)
            # Abilita il pulsante corrispondente
            button.setEnabled(True)
        else:
            # Gestisci il caso in cui il comando non sia stato impostato correttamente
            print(result)  # Stampa l'errore
        # Aggiungi la risposta al QTextBrowser
        self.textBrowser.append(result)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
