import sys
from PyQt5 import QtWidgets, QtCore
from led import Ui_MainWindow  # Importa la classe Ui_MainWindow dal file led.py

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_led)
        self.timer.start(1000)  # Imposta il timer per lampeggiare ogni secondo

    def update_led(self):
        # Cambia lo stato del LED ogni volta che viene chiamata questa funzione
        if self.radioButton.isChecked():
            self.radioButton.setChecked(False)
        else:
            self.radioButton.setChecked(True)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
