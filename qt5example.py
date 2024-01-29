from PyQt5 import QtWidgets, uic, QtCore
import sys

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('led.ui', self)

        # Crea un QTimer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.toggleRadioButton)

        # Connetti il segnale clicked del PushButton al metodo startBlinking
        self.pushButton.clicked.connect(self.startBlinking)

        self.show()

    def startBlinking(self):
        # Avvia il timer per far lampeggiare il RadioButton
        self.timer.start(500)  # lampeggia ogni 500 millisecondi

    def toggleRadioButton(self):
        # Cambia lo stato del RadioButton
        self.radioButton.setChecked(not self.radioButton.isChecked())
        # Aggiorna il QTextBrowser con il colore corrente
        if self.radioButton.isChecked():
            self.textBrowser.setText("Verde")
        else:
            self.textBrowser.setText("Rosso")

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
