from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QCalendarWidget, QLabel, QMessageBox
from appointmate.utils.appointment_manager import AppointmentManager
from appointmate.ui.appointment_dialog import AppointmentDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AppointMate")
        self.setMinimumSize(900, 700)

        self.appointment_manager = AppointmentManager()

        layout = QVBoxLayout()

        self.calendar = QCalendarWidget()
        self.calendar.selectionChanged.connect(self.update_appointment_display)
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
        dialog = AppointmentDialog(self)
        if dialog.exec_():
            appointment_data = dialog.get_appointment_data()
            date = self.calendar.selectedDate().toString("yyyy-MM-dd")
            appointment_data["date"] = date
            appointment_id = self.appointment_manager.add_appointment(appointment_data)
            QMessageBox.information(self, "Success", f"Appointment added with ID: {appointment_id}")
            self.update_appointment_display()

    def update_appointment_display(self):
        date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        appointments = self.appointment_manager.get_all_appointments()
        appointments_on_date = [app for app in appointments.values() if app["date"] == date]
        
        if appointments_on_date:
            display_text = "Appointments:\n\n"
            for app in appointments_on_date:
                display_text += f"{app['time']} - {app['name']}: {app['reason']}\n"
        else:
            display_text = "No appointments on this date"
        
        self.appointment_label.setText(display_text)