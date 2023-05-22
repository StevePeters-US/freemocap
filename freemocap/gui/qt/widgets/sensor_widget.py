from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget


class sensorwidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.label = QLabel("This is sensorwidget!")
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

