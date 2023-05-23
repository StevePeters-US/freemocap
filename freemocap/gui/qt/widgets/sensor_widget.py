from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import QTimer
import serial
import serial.tools.list_ports as list_ports
import datetime as dt
import pandas as pd
import time

class SensorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.label = QLabel("This is sensorwidget!")
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        self.timer = QTimer(self)

        ports = list(list_ports.comports())
        if ports:
            port_name = ports[0].device
            serialPort = serial.Serial(port=port_name, baudrate=115200, timeout=1)
            self.chart_data = pd.DataFrame()

            def collect_data():
                serialPort.write(b'g')
                time.sleep(0.1)
                arduino_data = serialPort.readline().decode('ascii').split()

                if arduino_data:
                    print('arduino data' + arduino_data[0])
                    time_now = dt.datetime.now()
                    elapsed_time = 0.0
                    
                    new_row = {'time': time_now, 'kg': arduino_data[0], 'elapsedTime': elapsed_time}
                    new_df = pd.DataFrame([new_row])
                    print(new_df)
                    self.chart_data = pd.concat([self.chart_data, new_df], ignore_index=True)

            # Add a method to trigger data collection
            def start_collecting_data():
                self.timer.timeout.connect(collect_data)
                self.timer.start(100)

            # Add a method to stop data collection
            def stop_collecting_data():
                self.timer.stop()

            self.start_collecting_data = start_collecting_data

            # Create a button to start data collection
            self.start_button = QPushButton("Start Collecting Data")
            self.start_button.clicked.connect(start_collecting_data)
            self.layout.addWidget(self.start_button)
            
            self.stop_button = QPushButton("Stop Collecting Data")
            self.stop_button.clicked.connect(stop_collecting_data)
            self.layout.addWidget(self.stop_button)

