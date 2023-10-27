from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QLabel

class SearchDialog(QDialog):
    def __init__(self, appointments, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Search Appointments")
        self.appointments = appointments
        self.layout = QVBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search term")
        self.layout.addWidget(self.search_input)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.perform_search)
        self.layout.addWidget(self.search_button)

        self.results_list = QListWidget()
        self.layout.addWidget(self.results_list)

        self.setLayout(self.layout)

    def perform_search(self):
        search_term = self.search_input.text().lower()
        self.results_list.clear()
        for app_id, app_data in self.appointments.items():
            if (search_term in app_data['name'].lower() or
                search_term in app_data['reason'].lower() or
                search_term in app_data['date']):
                self.results_list.addItem(f"{app_data['date']} - {app_data['name']}: {app_data['reason']}")