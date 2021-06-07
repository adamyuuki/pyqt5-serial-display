# pyqt5-serial-display

Simple pyqt5 project that display a dropdown menu with all the current COM ports available and connects to the port through a button.
when connected, the value sent by the serial device is displayed on the GUI.

I was using an arduino Leonardo and faced the problem that the Leonardo has to set de DTR and the RTS to True before trying to receive the signals.
Solved the problem with the following lines of code:
   self.serial.setDataTerminalReady(True)
   self.serial.setRequestToSend(True)
