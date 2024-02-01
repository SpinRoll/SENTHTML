from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtCore
import sys
import connessione
import loadINI
import manualcommand
import setIP
import micro  #  importare il modulo micro
import telemetria  # Assicurati di importare il modulo telemetria
import toggle
import SLEEP


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
        self.micro_box.setEnabled(False)  # Disabilita manua_commandbox all'avvio
        self.show()
        # Connetti il segnale clicked del pulsante al metodo save_log
        self.save_log.clicked.connect(self.save_loggi)
        self.clear_log.clicked.connect(self.clear)  # Connetti il segnale al metodo clear_log
        self.disconnectButton.clicked.connect(self.disconnect)
        self.connectButton.clicked.connect(self.connect)
        self.refresh_update.clicked.connect(self.start_refresh)
        self.sendcommand.clicked.connect(self.send_command)  # Connetti il segnale al metodo send_command

        self.set_newip_button.clicked.connect(self.set_ip_address)  # Aggiungi questa riga

        # Connetti i segnali dei pulsanti alle funzioni appropriate
        self.Micro_ENABLE.clicked.connect(lambda: self.handle_micro_button('ENPIC', self.Micro_ENABLE, "lightgreen"))
        self.Micro_DISABLE.clicked.connect(lambda: self.handle_micro_button('DISPIC', self.Micro_DISABLE, "red"))
        self.Micro_SLEEP.clicked.connect(lambda: self.handle_micro_button('SLEEPSV', self.Micro_SLEEP, "yellow"))
        self.Micro_WAKE.clicked.connect(lambda: self.handle_micro_button('WAKESV', self.Micro_WAKE, "lightblue"))

        self.refresh_secondi.setMinimum(1)  # Imposta il valore minimo a 1
        self.refresh_secondi.setValue(1)

        # Crea un timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.refresh_update_fn)

        self.CH_ENABLE_1.setText("OFF")  # Imposta il testo iniziale a "OFF"
        self.CH_ENABLE_1.clicked.connect(self.ENCHANNEL)  # Collega il segnale clicked alla funzione toggle_channel
        self.CH_ENABLE_2.setText("OFF")  # Imposta il testo iniziale a "OFF"
        self.CH_ENABLE_2.clicked.connect(self.ENCHANNEL)  # Collega il segnale clicked alla funzione toggle_channel

        self.CH_SLEEP_WAKE_1.setText("W/S")  # Imposta il testo iniziale a "OFF"
        self.CH_SLEEP_WAKE_1.clicked.connect(self.SLEEPCHANNEL)  # Collega il segnale clicked alla funzione toggle_channel
        self.CH_SLEEP_WAKE_2.setText("W/S")  # Imposta il testo iniziale a "OFF"
        self.CH_SLEEP_WAKE_2.clicked.connect(self.SLEEPCHANNEL)  # Collega il segnale clicked alla funzione toggle_channel

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
            self.micro_box.setEnabled(True)  # abilita manua_commandbox all'avvio



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
        self.micro_box.setEnabled(False)  # Disabilita manua_commandbox all'avvio

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
            # Abilita il pulsante corrispondente
            button.setEnabled(True)

            # Se il pulsante "enable" o "sleep" è stato premuto, disabilita il pulsante "disable" o "wake"
            if button == self.Micro_ENABLE:
                self.Micro_DISABLE.setStyleSheet("")
                self.Micro_DISABLE.setEnabled(True)
            elif button == self.Micro_SLEEP:
                self.Micro_WAKE.setStyleSheet("")
                self.Micro_WAKE.setEnabled(True)

            # Se il pulsante "disable" è stato premuto, disabilita i pulsanti "enable", "wake" e "sleep"
            elif button == self.Micro_DISABLE:
                self.Micro_ENABLE.setStyleSheet("")
                self.Micro_ENABLE.setEnabled(True)
                self.Micro_SLEEP.setStyleSheet("")
                self.Micro_SLEEP.setEnabled(True)
                self.Micro_WAKE.setStyleSheet("")
                self.Micro_WAKE.setEnabled(True)

            # Se il pulsante "wake" è stato premuto, disabilita il pulsante "sleep"
            elif button == self.Micro_WAKE:
                self.Micro_SLEEP.setStyleSheet("")
                self.Micro_SLEEP.setEnabled(True)
        else:
            # Gestisci il caso in cui il comando non sia stato impostato correttamente
            print(result)  # Stampa l'errore

        # Aggiungi la risposta al QTextBrowser
        self.textBrowser.append(result)

    def save_loggi(self):
        # Apri la finestra di dialogo per scegliere dove salvare il file
        filename, _ = QFileDialog.getSaveFileName(self, "Salva log", "", "File di testo (*.txt);;Tutti i file (*)")

        if filename:
            # Se l'utente ha scelto un file, salva il contenuto del QTextBrowser in quel file
            with open(filename, 'w') as f:
                f.write(self.textBrowser.toPlainText())

    def start_refresh(self):
        # Ottieni il numero di secondi dal QSpinBox
        seconds = self.refresh_secondi.value()
        # Avvia il timer per chiamare refresh_update ogni tot secondi
        self.timer.start(seconds * 1000)  # moltiplica per 1000 per convertire in millisecondi
    def refresh_update_fn(self):
        data = telemetria.request_data(self.connection)

        if data:
            # Aggiorna i widget con i primi due set di dati
            self.VAL1_1.setText(str(data[0][0]))
            self.VAL1_2.setText(str(data[0][1]))
            self.VAL1_3.setText(str(data[0][2]))
            self.VAL1_4.setText(str(data[0][3]))
            self.VAL1_5.setText(str(data[0][4]))
            self.VAL2_1.setText(str(data[1][0]))
            self.VAL2_2.setText(str(data[1][1]))
            self.VAL2_3.setText(str(data[1][2]))
            self.VAL2_4.setText(str(data[1][3]))
            self.VAL2_5.setText(str(data[1][4]))

    def ENCHANNEL(self):

        channel_number = int(self.sender().objectName().split('_')[-1])

        # Chiama la funzione toggle_channel da toggle.py
        toggle.toggle_channel(self.connection, self.sender(), channel_number, self.send_command)

    def SLEEPCHANNEL(self):

        sleep_channel_number = int(self.sender().objectName().split('_')[-1])

        # Chiama la funzione toggle_channel da toggle.py
        SLEEP.sleep_channel(self.connection, self.sender(), sleep_channel_number, self.send_command)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
