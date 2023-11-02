from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QTextEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import QDate, QTime

class EditAppointmentDialog(QDialog):
    def __init__(self, appointment_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Appointment")
        self.appointment_data = appointment_data
        self.layout = QVBoxLayout()

        self.name_input = QLineEdit(appointment_data['name'])
        self.layout.addWidget(QLabel("Name:"))
        self.layout.addWidget(self.name_input)

        self.reason_input = QLineEdit(appointment_data['reason'])
        self.layout.addWidget(QLabel("Reason:"))
        self.layout.addWidget(self.reason_input)

        self.date_input = QLineEdit(appointment_data['date'])
        self.layout.addWidget(QLabel("Date (YYYY-MM-DD):"))
        self.layout.addWidget(self.date_input)

        self.time_input = QLineEdit(appointment_data['time'])
        self.layout.addWidget(QLabel("Time (HH:MM AM/PM):"))
        self.layout.addWidget(self.time_input)

        self.comments_input = QTextEdit(appointment_data.get('comments', ''))
        self.layout.addWidget(QLabel("Comments:"))
        self.layout.addWidget(self.comments_input)

        self.save_button = QPushButton("Save Changes")
        self.save_button.clicked.connect(self.save_changes)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

    def save_changes(self):
        new_data = {
            'name': self.name_input.text(),
            'reason': self.reason_input.text(),
            'date': self.date_input.text(),
            'time': self.time_input.text(),
            'comments': self.comments_input.toPlainText()
        }
        
        if self.validate_input(new_data):
            self.appointment_data.update(new_data)
            self.accept()
        else:
            QMessageBox.warning(self, "Invalid Input", "Please ensure all fields are filled correctly.")

    def validate_input(self, data):
        if not all([data['name'], data['reason'], data['date'], data['time']]):
            return False
        try:
            QDate.fromString(data['date'], "yyyy-MM-dd")
            QTime.fromString(data['time'], "hh:mm AP")
        except ValueError:
            return False
        return True