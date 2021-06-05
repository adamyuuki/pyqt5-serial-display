from sqlite3.dbapi2 import connect
from PyQt5 import QtCore, QtGui, QtWidgets, QtSerialPort 
from PyQt5.QtWidgets import QApplication, QAction
import sys
import layout
import sqlite3
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import time
from PyQt5.QtSerialPort import QSerialPortInfo

class ExampleApp(QtWidgets.QMainWindow, layout.Ui_MainWindow):

    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.connectBtn.setCheckable(True)

        portname = "None"

        info_list = QSerialPortInfo()
        print(info_list)
        serial_list = info_list.availablePorts()
        print(serial_list)
        serial_ports = [port.portName() for port in serial_list]
        print(serial_ports)
        if(len(serial_ports)> 0):
            self.comboBox.insertItems(1,serial_ports)

        else:
            print('No ports connected')

        self.serial = QtSerialPort.QSerialPort(
            portname,
            baudRate=QtSerialPort.QSerialPort.Baud9600,
            readyRead=self.receive)

        self.comboBox.currentIndexChanged.connect(self.handleComboChange)
        self.connectBtn.toggled.connect(self.handleConnect)

    def handleComboChange(self):
        porta = self.comboBox.currentText()
        print(porta)
        seropen = False
        if self.serial.isOpen():
            seropen = True
            self.serial.close()   
        self.serial.setPortName(porta)
        if seropen:
            self.serial.open(QtCore.QIODevice.ReadWrite)
            if not self.serial.isOpen():
                self.connectBtn.setChecked(False)
    
    @QtCore.pyqtSlot()
    def receive(self):
        while self.serial.canReadLine():
            text = self.serial.readLine().data().decode()
            text = text.rstrip('\r\n')
            self.value.setText(text)

    @QtCore.pyqtSlot(bool)
    def handleConnect(self, checked):
        if checked:
            self.connectBtn.setText("Disconnect")
            if not self.serial.isOpen():
                self.serial.open(QtCore.QIODevice.ReadWrite)
                if not self.serial.isOpen():
                    self.connectBtn.setChecked(False)
            else:
                self.connectBtn.setChecked(False)
        else:
            self.connectBtn.setText("Connect")
            self.serial.close()
        print(checked)


    def closeEvent(self, event):
        self.serial.close()

def main():
    app = QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()