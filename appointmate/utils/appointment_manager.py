import json
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
import os

class AppointmentManager:
    def __init__(self, file_path, encryption_key):
        self.file_path = file_path
        self.fernet = Fernet(encryption_key.encode())

    def load_appointments(self):
        try:
            if not os.path.exists(self.file_path):
                return {}
            with open(self.file_path, 'rb') as file:
                encrypted_data = file.read()
                decrypted_data = self.fernet.decrypt(encrypted_data)
                return json.loads(decrypted_data)
        except (IOError, json.JSONDecodeError, ValueError) as e:
            print(f"Error loading appointments: {str(e)}")
            return {}

    def save_appointments(self, appointments):
        try:
            encrypted_data = self.fernet.encrypt(json.dumps(appointments).encode())
            with open(self.file_path, 'wb') as file:
                file.write(encrypted_data)
        except IOError as e:
            print(f"Error saving appointments: {str(e)}")

    def add_appointment(self, appointment):
        appointments = self.load_appointments()
        appointment_id = str(len(appointments) + 1)
        appointments[appointment_id] = appointment
        self.save_appointments(appointments)
        return appointment_id

    def get_appointment(self, appointment_id):
        appointments = self.load_appointments()
        return appointments.get(appointment_id)

    def update_appointment(self, appointment_id, updated_appointment):
        appointments = self.load_appointments()
        if appointment_id in appointments:
            appointments[appointment_id] = updated_appointment
            self.save_appointments(appointments)
            return True
        return False

    def delete_appointment(self, appointment_id):
        appointments = self.load_appointments()
        if appointment_id in appointments:
            del appointments[appointment_id]
            self.save_appointments(appointments)
            return True
        return False

    def get_all_appointments(self):
        return self.load_appointments()

    def get_pending_appointments(self):
        today = datetime.now().date()
        return {id: app for id, app in self.get_all_appointments().items() 
                if datetime.strptime(app['date'], "%Y-%m-%d").date() >= today}

    def get_past_appointments(self):
        today = datetime.now().date()
        return {id: app for id, app in self.get_all_appointments().items() 
                if datetime.strptime(app['date'], "%Y-%m-%d").date() < today}

    def get_today_appointments(self):
        today = datetime.now().date().strftime("%Y-%m-%d")
        return {id: app for id, app in self.get_all_appointments().items() 
                if app['date'] == today}

    def get_approaching_appointments(self, minutes=15):
        now = datetime.now()
        approaching = {}
        for id, app in self.get_all_appointments().items():
            app_datetime = datetime.strptime(f"{app['date']} {app['time']}", "%Y-%m-%d %I:%M %p")
            if timedelta(minutes=0) <= (app_datetime - now) <= timedelta(minutes=minutes):
                approaching[id] = app
        return approaching

    def search_appointments(self, query):
        all_appointments = self.get_all_appointments()
        return {
            id: app for id, app in all_appointments.items()
            if query.lower() in app['name'].lower() or
               query.lower() in app['reason'].lower() or
               query in app['date'] or
               query in app['time']
        }

    def get_appointments_by_date(self, date):
        return {
            id: app for id, app in self.get_all_appointments().items()
            if app['date'] == date
        }

    def get_appointments_by_date_range(self, start_date, end_date):
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
        return {
            id: app for id, app in self.get_all_appointments().items()
            if start <= datetime.strptime(app['date'], "%Y-%m-%d").date() <= end
        }

    def validate_appointment(self, appointment):
        required_fields = ['name', 'reason', 'date', 'time']
        for field in required_fields:
            if field not in appointment or not appointment[field]:
                return False
        try:
            datetime.strptime(appointment['date'], "%Y-%m-%d")
            datetime.strptime(appointment['time'], "%I:%M %p")
        except ValueError:
            return False
        return True