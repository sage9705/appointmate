from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, 
                             QCalendarWidget, QLabel, QMessageBox, QListWidget, QInputDialog, 
                             QStyle, QStyleFactory, QFrame, QSplitter, QMenu, QAction)
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QIcon, QFont
from appointmate.utils.appointment_manager import AppointmentManager
from .appointment_dialog import AppointmentDialog
from .search_dialog import SearchDialog
from .edit_appointment_dialog import EditAppointmentDialog
from config import APPOINTMENTS_FILE, ENCRYPTION_KEY

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AppointMate")
        self.setMinimumSize(1000, 600)
        self.appointment_manager = AppointmentManager()
        self.create_ui()
        self.create_menu_bar()
        self.setup_notification_timer()
        self.apply_stylesheet()

    def create_ui(self):
        main_layout = QHBoxLayout()
        
        # Left side: Calendar and buttons
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.selectionChanged.connect(self.update_appointment_display)
        left_layout.addWidget(self.calendar)
        
        button_layout = QHBoxLayout()
        self.add_button = self.create_button("Add", "plus.png", self.add_appointment)
        self.search_button = self.create_button("Search", "search.png", self.search_appointments)
        self.delete_button = self.create_button("Delete", "trash.png", self.delete_appointment)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.delete_button)
        left_layout.addLayout(button_layout)
        
        # Right side: Appointment list
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        self.date_label = QLabel()
        self.date_label.setAlignment(Qt.AlignCenter)
        self.date_label.setFont(QFont("Arial", 14, QFont.Bold))
        right_layout.addWidget(self.date_label)
        
        self.appointment_list = QListWidget()
        self.appointment_list.setAlternatingRowColors(True)
        self.appointment_list.itemDoubleClicked.connect(self.edit_appointment)
        right_layout.addWidget(self.appointment_list)
        
        # Add left and right widgets to main layout
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([400, 600])
        
        main_layout.addWidget(splitter)
        
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_button(self, text, icon_name, connection):
        button = QPushButton(text)
        button.setIcon(QIcon(f"resources/icons/{icon_name}"))
        button.setIconSize(QSize(24, 24))
        button.clicked.connect(connection)
        return button

    def create_menu_bar(self):
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
        date = self.calendar.selectedDate()
        self.date_label.setText(date.toString("MMMM d, yyyy"))
        appointments = self.appointment_manager.get_appointments_by_date(date.toString("yyyy-MM-dd"))
        
        for app_id, app in appointments.items():
            item = QListWidget.Item(f"{app['time']} - {app['name']}: {app['reason']}")
            item.setData(Qt.UserRole, app_id)
            self.appointment_list.addItem(item)

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
        dialog = SearchDialog(self.appointment_manager, self)
        dialog.exec_()

    def delete_appointment(self):
        current_item = self.appointment_list.currentItem()
        if current_item:
            app_id = current_item.data(Qt.UserRole)
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
        app_id = item.data(Qt.UserRole)
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
            dialog.addItem(f"{app['date']} {app['time']} - {app['name']}: {app['reason']}")
        dialog.show()

    def check_approaching_appointments(self):
        approaching = self.appointment_manager.get_approaching_appointments()
        for app in approaching.values():
            QMessageBox.information(self, "Upcoming Appointment", 
                                    f"You have an appointment with {app['name']} at {app['time']} for {app['reason']}")

    def apply_stylesheet(self):
        self.setStyle(QStyleFactory.create("Fusion"))
        with open("resources/style.css", "r") as f:
            self.setStyleSheet(f.read())