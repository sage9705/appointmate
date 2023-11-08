from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QPushButton, 
                             QCalendarWidget, QLabel, QMessageBox, QHBoxLayout, 
                             QMenu, QAction, QListWidget, QInputDialog, QStyle)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon
from appointmate.utils.appointment_manager import AppointmentManager
from appointmate.ui.appointment_dialog import AppointmentDialog
from appointmate.ui.search_dialog import SearchDialog
from appointmate.ui.edit_appointment_dialog import EditAppointmentDialog
from config import APPOINTMENTS_FILE, ENCRYPTION_KEY

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AppointMate")
        self.setMinimumSize(900, 700)

        self.appointment_manager = AppointmentManager(APPOINTMENTS_FILE, ENCRYPTION_KEY)

        self.create_ui()
        self.create_menu()
        self.setup_notification_timer()
        self.apply_stylesheet()

    def create_ui(self):
        layout = QVBoxLayout()

        self.calendar = QCalendarWidget()
        self.calendar.selectionChanged.connect(self.update_appointment_display)
        layout.addWidget(self.calendar)

        self.appointment_list = QListWidget()
        self.appointment_list.itemDoubleClicked.connect(self.edit_appointment)
        layout.addWidget(self.appointment_list)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Appointment")
        self.add_button.clicked.connect(self.add_appointment)
        self.add_button.setIcon(self.style().standardIcon(QStyle.SP_FileDialogNewFolder))
        button_layout.addWidget(self.add_button)

        self.search_button = QPushButton("Search Appointments")
        self.search_button.clicked.connect(self.search_appointments)
        self.search_button.setIcon(self.style().standardIcon(QStyle.SP_FileDialogContentsView))
        button_layout.addWidget(self.search_button)

        self.delete_button = QPushButton("Delete Appointment")
        self.delete_button.clicked.connect(self.delete_appointment)
        self.delete_button.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
        button_layout.addWidget(self.delete_button)

        layout.addLayout(button_layout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def create_menu(self):
        menu_bar = self.menuBar()
        
        appointments_menu = menu_bar.addMenu("Appointments")
        
        pending_action = QAction("View Pending", self)
        pending_action.triggered.connect(self.view_pending_appointments)
        appointments_menu.addAction(pending_action)
        
        past_action = QAction("View Past", self)
        past_action.triggered.connect(self.view_past_appointments)
        appointments_menu.addAction(past_action)
        
        today_action = QAction("View Today's", self)
        today_action.triggered.connect(self.view_today_appointments)
        appointments_menu.addAction(today_action)

    def setup_notification_timer(self):
        self.notification_timer = QTimer(self)
        self.notification_timer.timeout.connect(self.check_approaching_appointments)
        self.notification_timer.start(60000)  # Check every minute

    def update_appointment_display(self):
        self.appointment_list.clear()
        date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        appointments = self.appointment_manager.get_appointments_by_date(date)
        
        for app_id, app in appointments.items():
            self.appointment_list.addItem(f"{app['time']} - {app['name']}: {app['reason']} (ID: {app_id})")

    def add_appointment(self):
        dialog = AppointmentDialog(self)
        if dialog.exec_():
            appointment_data = dialog.get_appointment_data()
            date = self.calendar.selectedDate().toString("yyyy-MM-dd")
            appointment_data["date"] = date
            if self.appointment_manager.validate_appointment(appointment_data):
                appointment_id = self.appointment_manager.add_appointment(appointment_data)
                QMessageBox.information(self, "Success", f"Appointment added with ID: {appointment_id}")
                self.update_appointment_display()
            else:
                QMessageBox.warning(self, "Invalid Input", "Please ensure all fields are filled correctly.")

    def search_appointments(self):
        query, ok = QInputDialog.getText(self, "Search Appointments", "Enter search term:")
        if ok and query:
            appointments = self.appointment_manager.search_appointments(query)
            self.display_appointments(appointments, f"Search Results for '{query}'")

    def delete_appointment(self):
        current_item = self.appointment_list.currentItem()
        if current_item:
            app_id = current_item.text().split("(ID: ")[-1][:-1]
            reply = QMessageBox.question(self, 'Delete Appointment', 
                                         'Are you sure you want to delete this appointment?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                if self.appointment_manager.delete_appointment(app_id):
                    QMessageBox.information(self, "Success", "Appointment deleted successfully.")
                    self.update_appointment_display()
                else:
                    QMessageBox.warning(self, "Error", "Failed to delete appointment.")
        else:
            QMessageBox.warning(self, "No Selection", "Please select an appointment to delete.")

    def edit_appointment(self, item):
        app_id = item.text().split("(ID: ")[-1][:-1]
        appointment_data = self.appointment_manager.get_appointment(app_id)
        if appointment_data:
            dialog = EditAppointmentDialog(appointment_data, self)
            if dialog.exec_():
                if self.appointment_manager.update_appointment(app_id, dialog.appointment_data):
                    QMessageBox.information(self, "Success", "Appointment updated successfully.")
                    self.update_appointment_display()
                else:
                    QMessageBox.warning(self, "Error", "Failed to update appointment.")
        else:
            QMessageBox.warning(self, "Error", "Appointment not found.")

    def view_pending_appointments(self):
        self.display_appointments(self.appointment_manager.get_pending_appointments(), "Pending Appointments")

    def view_past_appointments(self):
        self.display_appointments(self.appointment_manager.get_past_appointments(), "Past Appointments")

    def view_today_appointments(self):
        self.display_appointments(self.appointment_manager.get_today_appointments(), "Today's Appointments")

    def display_appointments(self, appointments, title):
        dialog = QListWidget(self)
        dialog.setWindowTitle(title)
        for app_id, app in appointments.items():
            dialog.addItem(f"{app['date']} {app['time']} - {app['name']}: {app['reason']} (ID: {app_id})")
        dialog.show()

    def check_approaching_appointments(self):
        approaching = self.appointment_manager.get_approaching_appointments()
        for app in approaching.values():
            QMessageBox.information(self, "Upcoming Appointment", 
                                    f"You have an appointment with {app['name']} at {app['time']} for {app['reason']}")

    def apply_stylesheet(self):
        with open("resources/style.css", "r") as f:
            self.setStyleSheet(f.read())