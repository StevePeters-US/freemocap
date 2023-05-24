from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton, QComboBox
from PyQt6.QtCore import QTimer
import serial
import serial.tools.list_ports as list_ports
import datetime as dt
import pandas as pd
import time
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui

class SensorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.label = QLabel("This is sensorwidget!")
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        self.timer = QTimer(self)
        self.elapsed_time = 0.0
        self.start_time = 0.0

        # Create a combo box for selecting the COM port
        self.com_port_combo = QComboBox()
        self.layout.addWidget(self.com_port_combo)

        ports = list(list_ports.comports())
        for port in ports:
            self.com_port_combo.addItem(port.device)

        self.com_port_combo.setCurrentIndex(0)  # Set the default selection to the first port

        def get_selected_port():
            return self.com_port_combo.currentText()

        def open_serial_port():
            port_name = get_selected_port()
            serialPort = serial.Serial(port=port_name, baudrate=115200, timeout=1)
            return serialPort

        def is_serial_port_open(serial_port):
            return serial_port.isOpen()

        self.serial_port = open_serial_port()
        self.chart_data = pd.DataFrame()

        # Create a PlotWidget for real-time data plotting
        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)

        # Initialize the plot curve
        self.plot_curve = self.plot_widget.plot()

        def collect_data():
            if is_serial_port_open(self.serial_port):
                self.serial_port.write(b'g')
                time.sleep(0.05)
                arduino_data = self.serial_port.readline().decode('ascii').split()

                if arduino_data:
                    time_now = dt.datetime.now()
                    self.elapsed_time = round((time_now - self.start_time).total_seconds(), 2)

                    new_row = {'time': time_now, 'kg': arduino_data[0], 'elapsedTime': self.elapsed_time}
                    new_df = pd.DataFrame([new_row])
                    self.chart_data = pd.concat([self.chart_data, new_df], ignore_index=True)

                    # Convert 'kg' column to numeric type, handle non-numeric values as NaN
                    self.chart_data['kg'] = pd.to_numeric(self.chart_data['kg'], errors='coerce')

                    # Exclude non-numeric values from the plot
                    valid_data = self.chart_data.loc[self.chart_data['kg'].notna()]

                    # Update the plot curve with the latest data
                    self.plot_curve.setData(valid_data['elapsedTime'], valid_data['kg'])

            else:
                print('serial port not opened')

        # Add a method to trigger data collection
        def start_collecting_data():
            self.chart_data = pd.DataFrame()
            self.start_time = dt.datetime.now()
            self.timer.timeout.connect(collect_data)
            self.timer.start(50)

        # Add a method to stop data collection
        def stop_collecting_data():
            self.timer.stop()

            # Save chart data to a CSV file
            file_name = 'chart_data.csv'
            self.chart_data.to_csv(file_name, index=False)
            print(f"Chart data saved to '{file_name}'")

        self.start_collecting_data = start_collecting_data

        # Create a button to start data collection
        self.start_button = QPushButton("Start Collecting Data")
        self.start_button.clicked.connect(start_collecting_data)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Collecting Data")
        self.stop_button.clicked.connect(stop_collecting_data)
        self.layout.addWidget(self.stop_button)
