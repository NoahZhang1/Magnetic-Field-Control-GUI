import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QLabel, QComboBox, QMessageBox
import serial
from PyQt5.QtCore import Qt, QTimer
from serial.tools import list_ports

class SerialApp(QWidget):
    def __init__(self):
        super().__init__()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_ports)
        self.timer.start(5000)

        self.setWindowTitle("Magnetic Field Controller GUI")

        # Set the window size
        self.resize(500, 400)

        # Create the status label to show messages
        self.status_label = QLabel('<font color="green">Status: Ready</font>', self)
        self.status_label.setAlignment(Qt.AlignCenter)

        # Create a dropdown (QComboBox) to display available ports
        self.port_dropdown = QComboBox(self)
        self.populate_ports()

        # Create three QLineEdit widgets for input
        self.line_edit1 = QLineEdit(self)
        self.line_edit2 = QLineEdit(self)
        self.line_edit3 = QLineEdit(self)
        self.line_edit4 = QLineEdit(self)

        # Create a QPushButton widget to send the strings
        self.send_button = QPushButton("Send to USB", self)
        self.send_button.setFixedWidth(150) 
        self.send_button.clicked.connect(self.send_to_usb)


        self.setStatusTip("MF_GUI tool ©2023 Yunnuo 'Noah' Zhang and Liuxi Xing")

        self.status_label_bottom = QLabel(self.statusTip(), self)

        # Use QVBoxLayout for vertical layout
        layout = QVBoxLayout()

        layout.addWidget(self.status_label)

        # Adding the port dropdown to the layout
        layout.addWidget(QLabel("Select Port:"))
        layout.addWidget(self.port_dropdown)

        # Adding labels and line edits to the layout
        layout.addWidget(QLabel("Input 1:"))
        layout.addWidget(self.line_edit1)

        layout.addWidget(QLabel("Input 2:"))
        layout.addWidget(self.line_edit2)

        layout.addWidget(QLabel("Input 3:"))
        layout.addWidget(self.line_edit3)

        layout.addWidget(QLabel("Input 4:"))
        layout.addWidget(self.line_edit4)

        layout.addWidget(self.send_button)

        layout.addWidget(self.status_label_bottom)

        self.setLayout(layout)

    def populate_ports(self):
        current_port = self.port_dropdown.currentText()
        self.port_dropdown.clear()

        # Get the list of available ports
        ports = list_ports.comports()
        for port in ports:
            self.port_dropdown.addItem(port.device)

        index = self.port_dropdown.findText(current_port)
        if index != -1:
            self.port_dropdown.setCurrentIndex(index)
    
    def update_ports(self):
        self.populate_ports()


    '''
    UNUSED LOGIC FOR POP-OUT NOTIFICATION WINDOW
    '''
    # def send_to_usb(self):
    #     selected_port = self.port_dropdown.currentText()

    #     text1 = self.line_edit1.text()
    #     text2 = self.line_edit2.text()
    #     text3 = self.line_edit3.text()
    #     text4 = self.line_edit4.text()


    #     combined_text = f"{text1},{text2},{text3},{text4}"
    #     print(combined_text)
    #     # Make sure to close any previous connections and open a new one
    #     try:
    #         if hasattr(self, 'ser') and self.ser.is_open:
    #             self.ser.close()
    #         self.ser = serial.Serial(selected_port, 9600)
    #         self.ser.write(combined_text.encode())
    #         self.ser.close()

    #     # Display the success notification
    #         QMessageBox.information(self, "Notification", "Data sent successfully!")

    #     except Exception as e:
    #         print(f"Error: {e}")
    #     # Display the error notification
    #         QMessageBox.critical(self, "Error", f"Failed to send data: {e}")

    def send_to_usb(self):
        selected_port = self.port_dropdown.currentText()

        text1 = self.line_edit1.text()
        text2 = self.line_edit2.text()
        text3 = self.line_edit3.text()
        text4 = self.line_edit4.text()


        combined_text = f"{text1},{text2},{text3},{text4}"
        print(combined_text)
        selected_port = self.port_dropdown.currentText()

        try:
            if hasattr(self, 'ser') and self.ser.is_open:
                self.ser.close()
            self.ser = serial.Serial(selected_port, 9600)
            self.ser.write(combined_text.encode())
            self.ser.close()

            # Update status label with success message in green color
            self.status_label.setText('<font color="green">Status: Data sent successfully!</font>\n <font color="black">Data sent: ' + combined_text + '</font>')

        except Exception as e:
            print(f"Error: {e}")
            # Update status label with error message in red color
            self.status_label.setText(f'<font color="red">Status: Failed to send data: {e}</font>')

    def closeEvent(self, event):
        # Close the serial connection when the app is closed
        if hasattr(self, 'ser') and self.ser.is_open:
            self.ser.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SerialApp()
    window.show()
    sys.exit(app.exec_())
