from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QCompleter
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QButtonGroup
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
        ip, port, mac, commands, set_ip, otx_thresholds, orx_thresholds = loadINI.load_config()
        self.IPentry.setText(ip)
        self.port_entry.setText(port)
        self.mac_entry.setText(mac)
        self.comboBox.addItems(commands)
        self.comboBox.setEditable(True)

        # Dividi l'indirizzo IP in blocchi
        ip_blocks = set_ip.split('.')

        self.type_orx.setChecked(True)

        # Inserisci ciascun blocco in un diverso QTextEdit
        self.ip.setText(ip_blocks[0])
        self.ip_2.setText(ip_blocks[1])
        self.ip_3.setText(ip_blocks[2])
        self.ip_4.setText(ip_blocks[3])

        self.connection = connessione.Connection()  # Crea un'istanza della classe Connection

        self.button_group = QButtonGroup()
        self.button_group.addButton(self.type_orx)
        self.button_group.addButton(self.type_otx)

        self.TEL_1.setText('-')
        self.TEL_2.setText('-')
        self.TEL_3.setText('-')
        self.TEL_4.setText('-')
        self.TEL_5.setText('-')
        # Crea un QCompleter
        completer = QCompleter()

        # Imposta il modello del completatore per corrispondere a quello del combobox
        completer.setModel(self.comboBox.model())

        # Imposta il completatore per il combobox
        self.comboBox.setCompleter(completer)

        #self.manual_commandbox = manualcommand.manua_commandbox(self)  # Crea un'istanza della classe manua_commandbox

        self.manua_commandbox.setEnabled(False)  # Disabilita manua_commandbox all'avvio
        self.LOG_BOX.setEnabled(False)  # Disabilita manua_commandbox all'avvio
        self.NewIP_box.setEnabled(False)  # Disabilita manua_commandbox all'avvio
        self.micro_box.setEnabled(False)  # Disabilita manua_commandbox all'avvio
        self.TELEMETRIA.setEnabled(False)
        self.setting_refresh.setEnabled(False)
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
        self.Micro_DISABLE.clicked.connect(lambda: self.handle_micro_button('DISPIC', self.Micro_DISABLE, "orange"))
        self.Micro_SLEEP.clicked.connect(lambda: self.handle_micro_button('SLEEPSV', self.Micro_SLEEP, "yellow"))
        self.Micro_WAKE.clicked.connect(lambda: self.handle_micro_button('WAKESV', self.Micro_WAKE, "lightblue"))

        self.refresh_secondi.setMinimum(1)  # Imposta il valore minimo a 1
        self.refresh_secondi.setValue(1)

        # Crea un timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.refresh_update_fn)
        self.refresh_stop.clicked.connect(self.stop_refresh)

        # Inizializza i canali
        for i in range(1, 21):
            getattr(self, f"CH_ENABLE_{i}").setText("OFF")
            getattr(self, f"CH_ENABLE_{i}").clicked.connect(self.ENCHANNEL)
            getattr(self, f"CH_SLEEP_WAKE_{i}").setText("W/S")
            getattr(self, f"CH_SLEEP_WAKE_{i}").clicked.connect(self.SLEEPCHANNEL)

        '''
        self.CH_ENABLE_1.setText("OFF")  # Imposta il testo iniziale a "OFF"
        self.CH_ENABLE_1.clicked.connect(self.ENCHANNEL)  # Collega il segnale clicked alla funzione toggle_channel
        self.CH_ENABLE_2.setText("OFF")  # Imposta il testo iniziale a "OFF"
        self.CH_ENABLE_2.clicked.connect(self.ENCHANNEL)  # Collega il segnale clicked alla funzione toggle_channel

        self.CH_SLEEP_WAKE_1.setText("W/S")  # Imposta il testo iniziale a "OFF"
        self.CH_SLEEP_WAKE_1.clicked.connect(self.SLEEPCHANNEL)  # Collega il segnale clicked alla funzione toggle_channel
        self.CH_SLEEP_WAKE_2.setText("W/S")  # Imposta il testo iniziale a "OFF"
        self.CH_SLEEP_WAKE_2.clicked.connect(self.SLEEPCHANNEL)  # Collega il segnale clicked alla funzione toggle_channel
        '''


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
            self.TELEMETRIA.setEnabled(True)
            self.setting_refresh.setEnabled(True)



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
        #self.LOG_BOX.setEnabled(False)  # Disabilita manua_commandbox all'avvio
        self.NewIP_box.setEnabled(False)  # Disabilita manua_commandbox all'avvio
        self.micro_box.setEnabled(False)  # Disabilita manua_commandbox all'avvio
        self.TELEMETRIA.setEnabled(False)  # Disabilita manua_commandbox all'avvio
        self.setting_refresh.setEnabled(False)
        self.timer.stop()

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
        # Controlla se uno dei radio button è selezionato
        if not self.type_orx.isChecked() and not self.type_otx.isChecked():
            print("Nessun tipo selezionato!")
            return

        # Ottieni il numero di secondi dal QSpinBox
        seconds = self.refresh_secondi.value()
        # Avvia il timer per chiamare refresh_update ogni tot secondi
        self.timer.start(seconds * 1000)  # moltiplica per 1000 per convertire in millisecondi

    def stop_refresh(self):
        self.timer.stop()

    def refresh_update_fn(self):

        # Controlla se uno dei radio button è selezionato
        if not self.type_orx.isChecked() and not self.type_otx.isChecked():
            print("Nessun tipo selezionato!")
            return

        data = telemetria.request_data(self.connection, self.type_orx.isChecked())
        ip, port, mac, commands, set_ip, otx_thresholds, orx_thresholds = loadINI.load_config()

        # Stampa i dizionari delle soglie
        #print("OTX thresholds:", otx_thresholds)
        #print("ORX thresholds:", orx_thresholds)

        if data:
            # Controlla se i dati rientrano nelle soglie
            if self.type_orx.isChecked():
                thresholds = orx_thresholds
                self.TEL_5.hide()
                self.CANALE_15.show()
                self.CANALE_16.show()
                self.CANALE_17.show()
                self.CANALE_18.show()
                self.CANALE_19.show()
                self.CANALE_20.show()
                threshold_keys = ['totcurr', 'lnacurr', 'pdcurr', 'brdtemp']
                num_values = 4  # 4 valori per orx
                num_channels = 20  # 20 canali per orx
            elif self.type_otx.isChecked():
                self.TEL_5.show()
                self.CANALE_15.hide()
                self.CANALE_16.hide()
                self.CANALE_17.hide()
                self.CANALE_18.hide()
                self.CANALE_19.hide()
                self.CANALE_20.hide()
                thresholds = otx_thresholds
                threshold_keys = ['lastemp', 'lascurr', 'teccurr', 'lnacurr', 'totcurr']
                num_values = 5  # 5 valori per otx
                num_channels = 14  # 14 canali per otx

            # Imposta il testo di ogni QLineEdit con il nome della label corrispondente
            for i, key in enumerate(threshold_keys):
                getattr(self, f'TEL_{i + 1}').setText(key.upper())

            for j in range(1, num_channels + 1):  # Itera su tutti i gruppi di valori VAL

                if self.type_orx.isChecked():
                    getattr(self, f'VAL{j}_5').hide()
                elif self.type_otx.isChecked():
                    getattr(self, f'VAL{j}_5').show()

                # Ripristina il colore di sfondo dei widget
                for i in range(5):
                    getattr(self, f'VAL{j}_{i + 1}').setStyleSheet("")

                # Aggiorna i widget con i primi due set di dati
                for i in range(num_values):
                    getattr(self, f'VAL{j}_{i + 1}').setText(str(data[j - 1][i]))

                for i, key in enumerate(threshold_keys):
                    #print(f"Checking value {i + 1}...")
                    #print(f"Thresholds: {thresholds[key][0]} - {thresholds[key][1]}")
                    #print(f"Data: {data[j - 1][i]}")
                    if not (thresholds[key][0] <= float(data[j - 1][i]) <= thresholds[key][1]):
                        print(f"Valore {i + 1} fuori dalle soglie!")
                        getattr(self, f'VAL{j}_{i + 1}').setStyleSheet("background-color: lightyellow")
                        # Aggiungi la risposta al QTextBrowser
                        self.textBrowser.append(f"Canale {j}, Tipo {key}, {data[j - 1][i]}  fuori dalle soglie!")

    def ENCHANNEL(self):
        channel_number = int(self.sender().objectName().split('_')[-1])

        # Passa lo stato del radio button alla funzione toggle_channel
        toggle.toggle_channel(self.connection, self.sender(), channel_number, self.send_command,self.type_orx.isChecked())


    def SLEEPCHANNEL(self):

        sleep_channel_number = int(self.sender().objectName().split('_')[-1])

        # Chiama la funzione toggle_channel da toggle.py
        SLEEP.sleep_channel(self.connection, self.sender(), sleep_channel_number, self.send_command, self.type_orx.isChecked())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
