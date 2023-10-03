import os
import sys
import json
import datetime
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtWidgets
#from PyQtWebEngine.QtWebEngineWidgets import QWebEngineView 
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QCalendarWidget, 
    QPushButton, QMessageBox, QAction, QLineEdit, QHBoxLayout, QDialog, QTextEdit, QDialogButtonBox
)

class AppointmentDetailsDialog(QDialog):
    """collect appointment details."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Appointment Details")
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

        button_box = QtWidgets.QDialogButtonBox()
        ok_button = button_box.addButton(QtWidgets.QDialogButtonBox.Ok)
        cancel_button = button_box.addButton(QtWidgets.QDialogButtonBox.Cancel)
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        self.layout.addWidget(button_box)

        self.setLayout(self.layout)

class SearchResultsDialog(QDialog):
    """display search results."""
    def __init__(self, search_results, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Search Results")
        self.layout = QVBoxLayout()

        self.search_results = search_results

        self.results_list = QtWidgets.QListWidget()
        self.results_list.itemClicked.connect(self.show_appointment_details)
        self.layout.addWidget(self.results_list)

        self.setLayout(self.layout)

    def show_appointment_details(self, item):
        appointment_id = item.text().split(":")[1].strip()
        if appointment_id in self.search_results:
            appointment_data = self.search_results[appointment_id]
            details = appointment_data["details"]
            date = appointment_data["date"]
            comments = appointment_data["comments"]
            details_text = f"Appointment ID: {appointment_id}\nDate: {date}\nDetails: {details}\nComments: {comments}"
            QMessageBox.information(self, "Appointment Details", details_text)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AppointMate")
        self.setMinimumSize(900, 700)

        css_file_path = os.path.join(os.path.dirname(__file__), "style.css")
        with open(css_file_path, "r") as f:
            stylesheet = f.read()

        self.setStyleSheet(stylesheet)
        self.layout = QVBoxLayout()
   
        self.create_search_bar() 
        self.create_calendar()
        self.create_label()
        self.create_button("Schedule Appointment", self.on_button_click)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        
        """
        # Create a QWebEngineView to display the HTML content
        self.web_view = QWebEngineView(self)
        self.web_view.setUrl(QUrl.fromLocalFile("your_web_page.html"))  # Load your HTML file
        self.layout.addWidget(self.web_view)
        """

        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        self.create_menu()

        self.resize(700, 400)

        self.appointments = {}
        self.load_appointments()
        self.search_results = {}

        # Set up a timer for checking approaching appointments
        self.appointment_timer = QtCore.QTimer(self)
        self.appointment_timer.timeout.connect(self.check_appointments)
        self.appointment_timer.start(60000)  # Check every minute

    def create_search_bar(self):
        self.search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by date or details")
        self.search_input.textChanged.connect(self.on_search_changed)
        self.search_layout.addWidget(self.search_input)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.on_search_button_click)
        self.search_layout.addWidget(self.search_button)

        self.layout.addLayout(self.search_layout)

    def create_calendar(self):
        self.calendar = QCalendarWidget()
        self.calendar.selectionChanged.connect(self.on_date_selection)
        self.layout.addWidget(self.calendar)

    def create_label(self):
        self.label = QLabel()
        self.layout.addWidget(self.label)

    def create_button(self, text, slot):
        button = QPushButton(text)
        button.clicked.connect(slot)
        self.layout.addWidget(button)

    def create_menu(self):
        menu_bar = self.menuBar()

        # Create the Appointments menu
        appointments_menu = menu_bar.addMenu("Menu")

        # Create the submenus for different types of appointments
        self.create_sub_menu("Pending Appointments", self.show_pending_appointments, appointments_menu)
        self.create_sub_menu("Due Appointments", self.show_due_appointments, appointments_menu)
        self.create_sub_menu("Past Appointments", self.show_past_appointments, appointments_menu)
        self.create_sub_menu("Delete Appointment", self.delete_appointment, appointments_menu)

        self.setMenuBar(menu_bar)

    def create_sub_menu(self, title, slot, parent_menu):
        action = QAction(title, self)
        action.triggered.connect(slot)
        parent_menu.addAction(action)

    def on_date_selection(self):
        selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        self.label.setText(f"Selected date: {selected_date}")

    def on_button_click(self):
        appointment_dialog = AppointmentDetailsDialog(self)
        if appointment_dialog.exec_() == QtWidgets.QDialog.Accepted:
            name = appointment_dialog.name_input.text()
            reason = appointment_dialog.reason_input.text()
            time = appointment_dialog.time_input.text()
            comments = appointment_dialog.comments_input.toPlainText()
            date = self.calendar.selectedDate().toString("yyyy-MM-dd")

            if name and reason and time:
                appointment_details = f"{name} - {reason} - {time}"
                self.process_appointment(appointment_details, date, comments)
            else:
                self.show_error_dialog("Invalid input", "Please enter valid appointment details.")

    def process_appointment(self, appointment_details, date, comments):
        appointment_data = {
            "details": appointment_details,
            "date": date,
            "comments": comments
        }

        appointment_id = str(len(self.appointments) + 1)
        self.appointments[appointment_id] = appointment_data

        self.save_appointments()

        self.show_success_dialog("Appointment Scheduled", "The appointment has been scheduled successfully.")

    def delete_appointment(self):
        if not self.appointments:
            self.show_error_dialog("No Appointments", "There are no appointments to delete.")
            return

        dialog = DeleteAppointmentDialog(self.appointments, self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            selected_appointment_ids = dialog.get_selected_appointment_ids()
            if selected_appointment_ids:
                for appointment_id in selected_appointment_ids:
                    if appointment_id in self.appointments:
                        del self.appointments[appointment_id]

                self.save_appointments()

                self.show_success_dialog("Appointments Deleted", "Selected appointments have been deleted successfully.")
            else:
                self.show_error_dialog("No Appointments Selected", "No appointments were selected for deletion.")

    def show_error_dialog(self, title, message):
        error_dialog = QtWidgets.QMessageBox()
        error_dialog.setIcon(QtWidgets.QMessageBox.Warning)
        error_dialog.setWindowTitle(title)
        error_dialog.setText(message)
        error_dialog.exec_()

    def show_success_dialog(self, title, message):
        success_dialog = QtWidgets.QMessageBox()
        success_dialog.setIcon(QtWidgets.QMessageBox.Information)
        success_dialog.setWindowTitle(title)
        success_dialog.setText(message)
        success_dialog.exec_()

    def on_search_changed(self):
        search_text = self.search_input.text()
        if search_text:
            filtered_appointments = {k: v for k, v in self.appointments.items() if
                                      search_text.lower() in v["details"].lower() or
                                      search_text in v["date"]}
            self.search_results = filtered_appointments
            self.display_search_results(filtered_appointments)
        else:
            self.search_results = {}
            self.label.setText("")
            self.display_appointments(self.appointments)

    def on_search_button_click(self):
        self.on_search_changed()

    def load_appointments(self):
        try:
            with open("appointments.json", "r") as file:
                self.appointments = json.load(file)
        except FileNotFoundError:
            self.save_appointments()
        except json.JSONDecodeError as e:
            self.show_error_dialog("Error Loading Appointments", f"Failed to load appointments: {str(e)}")

    def save_appointments(self):
        try:
            with open("appointments.json", "w") as file:
                json.dump(self.appointments, file)
        except Exception as e:
            self.show_error_dialog("Error Saving Appointments", f"Failed to save appointments: {str(e)}")

    def show_pending_appointments(self):
        pending_appointments = []
        today = QtCore.QDate.currentDate()

        for appointment_id, appointment_data in self.appointments.items():
            appointment_date = QtCore.QDate.fromString(appointment_data["date"], "yyyy-MM-dd")
            if appointment_date >= today:
                pending_appointments.append(appointment_data["details"])

        if pending_appointments:
            message = "Pending Appointments:\n\n" + "\n".join(pending_appointments)
            self.show_information_dialog("Pending Appointments", message)
        else:
            self.show_information_dialog("No Pending Appointments", "There are no pending appointments.")

    def show_due_appointments(self):
        due_appointments = []
        today = QtCore.QDate.currentDate()

        for appointment_id, appointment_data in self.appointments.items():
            appointment_date = QtCore.QDate.fromString(appointment_data["date"], "yyyy-MM-dd")
            if appointment_date == today:
                due_appointments.append(appointment_data["details"])

        if due_appointments:
            message = "Due Appointments:\n\n" + "\n".join(due_appointments)
            self.show_information_dialog("Due Appointments", message)
        else:
            self.show_information_dialog("No Due Appointments", "There are no appointments due today.")

    def show_past_appointments(self):
        past_appointments = []
        today = QtCore.QDate.currentDate()

        for appointment_id, appointment_data in self.appointments.items():
            appointment_date = QtCore.QDate.fromString(appointment_data["date"], "yyyy-MM-dd")
            if appointment_date < today:
                past_appointments.append(appointment_data["details"])

        if past_appointments:
            message = "Past Appointments:\n\n" + "\n".join(past_appointments)
            self.show_information_dialog("Past Appointments", message)
        else:
            self.show_information_dialog("No Past Appointments", "There are no past appointments.")

    def show_information_dialog(self, title, message):
        info_dialog = QtWidgets.QMessageBox()
        info_dialog.setIcon(QtWidgets.QMessageBox.Information)
        info_dialog.setWindowTitle(title)
        info_dialog.setText(message)
        info_dialog.exec_()

    def display_appointments(self, appointments_dict):
        # Display appointments in the label
        appointments_text = "\n".join([f"ID: {k}, Date: {v['date']}, Details: {v['details']}" for k, v in appointments_dict.items()])
        self.label.setText(appointments_text)

    def display_search_results(self, search_results):
        if search_results:
            search_text = "\n".join([f"ID: {k}, Date: {v['date']}, Details: {v['details']}" for k, v in search_results.items()])
            self.label.setText(search_text)
        else:
            self.label.setText("No matching appointments found.")

    def check_appointments(self):
        # Get the current date and time
        current_datetime = datetime.datetime.now()

        # Check for approaching appointments within the next 15 minutes
        for appointment_id, appointment_data in self.appointments.items():
            appointment_datetime = datetime.datetime.strptime(appointment_data["date"], "%Y-%m-%d %I:%M %p")
            time_difference = appointment_datetime - current_datetime

            # If the appointment is within the next 15 minutes, show a notification
            if time_difference.total_seconds() > 0 and time_difference.total_seconds() <= 900:
                self.show_notification("Approaching Appointment", f"Appointment ID: {appointment_id} is approaching!")

    def show_notification(self, title, message):
        notification = QMessageBox()
        notification.setIcon(QMessageBox.Information)
        notification.setWindowTitle(title)
        notification.setText(message)
        notification.exec_()

class DeleteAppointmentDialog(QDialog):
    """Dialog for deleting appointments."""
    def __init__(self, appointments, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Delete Appointments")
        self.layout = QVBoxLayout()
        self.appointments = appointments
        self.selected_appointment_ids = []

        self.create_instructions_label()  # Add instructions label
        self.create_appointments_list()
        self.create_button_box()

        self.setLayout(self.layout)

    def create_instructions_label(self):
        instructions_label = QLabel("Select the appointments you want to delete:")
        self.layout.addWidget(instructions_label)

    def create_appointments_list(self):
        appointments_list = QtWidgets.QListWidget()
        appointments_list.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

        for appointment_id, appointment_data in self.appointments.items():
            details = appointment_data["details"]
            date = appointment_data["date"]
            item_text = f"Appointment ID: {appointment_id}, Date: {date}, Details: {details}"
            item = QtWidgets.QListWidgetItem(item_text)
            appointments_list.addItem(item)

        appointments_list.itemSelectionChanged.connect(self.on_selection_changed)
        self.layout.addWidget(appointments_list)

    def create_button_box(self):
        button_box = QDialogButtonBox()
        delete_button = button_box.addButton("Delete", QDialogButtonBox.AcceptRole)
        cancel_button = button_box.addButton("Cancel", QDialogButtonBox.RejectRole)

        delete_button.clicked.connect(self.on_delete_button_click)
        cancel_button.clicked.connect(self.reject)

        self.layout.addWidget(button_box)

    def on_selection_changed(self):
        selected_items = self.sender().selectedItems()
        self.selected_appointment_ids = [item.text().split(",")[0].split(":")[1].strip() for item in selected_items]

    def on_delete_button_click(self):
        if not self.selected_appointment_ids:
            QMessageBox.warning(self, "No Appointments Selected", "Please select at least one appointment to delete.")
        else:
            # Show a confirmation dialog here before proceeding with deletion
            confirmation = QMessageBox.question(self, "Confirm Deletion", "Are you sure you want to delete the selected appointments?", QMessageBox.Yes | QMessageBox.No)
            if confirmation == QMessageBox.Yes:
                self.accept()

    def get_selected_appointment_ids(self):
        return self.selected_appointment_ids

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_DisableWindowContextHelpButton)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
