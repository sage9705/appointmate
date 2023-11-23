import json
from cryptography.fernet import Fernet, InvalidToken
from datetime import datetime, timedelta
import os
from config import APPOINTMENTS_FILE, ENCRYPTION_KEY

class AppointmentManager:
    def __init__(self):
        self.file_path = APPOINTMENTS_FILE
        self.fernet = Fernet(ENCRYPTION_KEY.encode())

    def load_appointments(self):
        try:
            if not os.path.exists(self.file_path):
                return {}
            with open(self.file_path, 'rb') as file:
                encrypted_data = file.read()
                try:
                    decrypted_data = self.fernet.decrypt(encrypted_data)
                    return json.loads(decrypted_data)
                except InvalidToken:
                    print("Warning: Unable to decrypt the appointments file. Starting with an empty appointment list.")
                    return {}
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

    def get_appointments_by_date(self, date):
        return {
            id: app for id, app in self.get_all_appointments().items()
            if app['date'] == date
        }

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

    def validate_appointment(self, appointment):
        required_fields = ['name', 'reason', 'date', 'time']
        return all(field in appointment and appointment[field] for field in required_fields)