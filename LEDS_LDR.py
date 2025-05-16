import sys
from PyQt5 import uic, QtWidgets, QtGui, QtCore
import serial as tarjeta
from fontTools.misc.textTools import caselessSort

qtCreatorFile = "LEDS_LDR.ui" # Nombre del archivo aquí
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        # Área de los signals
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(1023)
        self.horizontalSlider.setSingleStep(1)
        self.horizontalSlider.setValue(0)
        self.horizontalSlider.valueChanged.connect(self.cambiaValor)
        self.txt_com.setText("COM3")
        self.txt_valor.setText("1023")
        self.arduino = None
        self.btn_accion.clicked.connect(self.accion)
        self.segundoPlano = QtCore.QTimer()

    # Área de los Slots
    def cambiaValor(self):
        if self.arduino is not None and self.arduino.is_open:
            value = self.horizontalSlider.value()
            self.txt_valor.setText(str(value))
            comando = f"{value}\n"
            self.arduino.write(comando.encode())
        else:
            self.txt_estado.setText("ERROR: Arduino no conectado")

    def accion(self):
        texto = self.btn_accion.text()
        com = self.txt_com.text()
        if texto == "CONECTAR":
            try:
                self.arduino = tarjeta.Serial(com, baudrate=9600, timeout=1)
                self.segundoPlano.start(100)
                self.btn_accion.setText("DESCONECTAR")
                self.txt_estado.setText("CONECTADO")
                self.horizontalSlider.setEnabled(True)
            except Exception as e:
                self.txt_estado.setText(f"Error al conectar: {str(e)}")
        elif texto == "DESCONECTAR":
            self.segundoPlano.stop()
            self.arduino.close()
            self.btn_accion.setText("RECONECTAR")
            self.txt_estado.setText("DESCONECTADO")
            self.horizontalSlider.setEnabled(False)
        elif texto == "RECONECTAR":
            try:
                self.arduino.open()
                self.segundoPlano.start(100)
                self.btn_accion.setText("DESCONECTAR")
                self.txt_estado.setText("RECONECTADO")
                self.horizontalSlider.setEnabled(True)
            except Exception as e:
                self.txt_estado.setText(f"Error al reconectar: {str(e)}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())