from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QTextEdit, QPushButton, QLabel

class AppointmentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Appointment")
        self.layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")
        self.layout.addWidget(self.name_input)

        self.reason_input = QLineEdit()
        self.reason_input.setPlaceholderText("Reason for appointment")
        self.layout.addWidget(self.reason_input)

        self.time_input = QLineEdit()
        self.time_input.setPlaceholderText("Time (e.g., 10:00 AM)")
        self.layout.addWidget(self.time_input)

        self.comments_input = QTextEdit()
        self.comments_input.setPlaceholderText("Additional Comments")
        self.layout.addWidget(self.comments_input)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

    def get_appointment_data(self):
        return {
            "name": self.name_input.text(),
            "reason": self.reason_input.text(),
            "time": self.time_input.text(),
            "comments": self.comments_input.toPlainText()
        }