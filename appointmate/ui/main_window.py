from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QPushButton, 
                             QCalendarWidget, QLabel, QMessageBox, QHBoxLayout, 
                             QMenu, QAction, QListWidget, QInputDialog)
from PyQt5.QtCore import QTimer
from appointmate.utils.appointment_manager import AppointmentManager
from appointmate.ui.appointment_dialog import AppointmentDialog
from appointmate.ui.search_dialog import SearchDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AppointMate")
        self.setMinimumSize(900, 700)

        self.appointment_manager = AppointmentManager()

        self.create_ui()
        self.create_menu()
        self.setup_notification_timer()

    def create_ui(self):
        layout = QVBoxLayout()

        self.calendar = QCalendarWidget()
        self.calendar.selectionChanged.connect(self.update_appointment_display)
        layout.addWidget(self.calendar)

        self.appointment_list = QListWidget()
        layout.addWidget(self.appointment_list)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Appointment")
        self.add_button.clicked.connect(self.add_appointment)
        button_layout.addWidget(self.add_button)

        self.search_button = QPushButton("Search Appointments")
        self.search_button.clicked.connect(self.search_appointments)
        button_layout.addWidget(self.search_button)

        self.delete_button = QPushButton("Delete Appointment")
        self.delete_button.clicked.connect(self.delete_appointment)
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
        appointments = self.appointment_manager.get_all_appointments()
        appointments_on_date = [app for app in appointments.values() if app["date"] == date]
        
        for app in appointments_on_date:
            self.appointment_list.addItem(f"{app['time']} - {app['name']}: {app['reason']}")

    def add_appointment(self):
        dialog = AppointmentDialog(self)
        if dialog.exec_():
            appointment_data = dialog.get_appointment_data()
            date = self.calendar.selectedDate().toString("yyyy-MM-dd")
            appointment_data["date"] = date
            appointment_id = self.appointment_manager.add_appointment(appointment_data)
            QMessageBox.information(self, "Success", f"Appointment added with ID: {appointment_id}")
            self.update_appointment_display()

    def search_appointments(self):
        appointments = self.appointment_manager.get_all_appointments()
        dialog = SearchDialog(appointments, self)
        dialog.exec_()

    def delete_appointment(self):
        current_item = self.appointment_list.currentItem()
        if current_item:
            reply = QMessageBox.question(self, 'Delete Appointment', 
                                         'Are you sure you want to delete this appointment?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                date = self.calendar.selectedDate().toString("yyyy-MM-dd")
                appointments = self.appointment_manager.get_all_appointments()
                for id, app in appointments.items():
                    if app['date'] == date and f"{app['time']} - {app['name']}: {app['reason']}" == current_item.text():
                        self.appointment_manager.delete_appointment(id)
                        self.update_appointment_display()
                        break
        else:
            QMessageBox.warning(self, "No Selection", "Please select an appointment to delete.")

    def view_pending_appointments(self):
        self.display_appointments(self.appointment_manager.get_pending_appointments(), "Pending Appointments")

    def view_past_appointments(self):
        self.display_appointments(self.appointment_manager.get_past_appointments(), "Past Appointments")

    def view_today_appointments(self):
        self.display_appointments(self.appointment_manager.get_today_appointments(), "Today's Appointments")

    def display_appointments(self, appointments, title):
        dialog = QListWidget(self)
        dialog.setWindowTitle(title)
        for app in appointments.values():
            dialog.addItem(f"{app['date']} {app['time']} - {app['name']}: {app['reason']}")
        dialog.show()

    def check_approaching_appointments(self):
        approaching = self.appointment_manager.get_approaching_appointments()
        for app in approaching.values():
            QMessageBox.information(self, "Upcoming Appointment", 
                                    f"You have an appointment with {app['name']} at {app['time']} for {app['reason']}")