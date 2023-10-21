from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QCalendarWidget, QLabel
from appointmate.utils.appointment_manager import AppointmentManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AppointMate")
        self.setMinimumSize(900, 700)

        self.appointment_manager = AppointmentManager()

        layout = QVBoxLayout()

        self.calendar = QCalendarWidget()
        layout.addWidget(self.calendar)

        self.appointment_label = QLabel("No appointment selected")
        layout.addWidget(self.appointment_label)

        self.add_button = QPushButton("Add Appointment")
        self.add_button.clicked.connect(self.add_appointment)
        layout.addWidget(self.add_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def add_appointment(self):
        print("Add appointment clicked")