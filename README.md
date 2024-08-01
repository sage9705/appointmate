# AppointMate

AppointMate is a user-friendly appointment management application built with Python and PyQt5. It allows users to schedule, manage, and track appointments efficiently.

## Features

- **Calendar Integration**: View and manage appointments on an interactive calendar.
- **Add Appointments**: Easily schedule new appointments with details like name, reason, date, and time.
- **Edit Appointments**: Modify existing appointment details as needed.
- **Delete Appointments**: Remove unwanted or cancelled appointments.
- **Search Functionality**: Quickly find specific appointments using various search criteria.
- **Appointment Categories**: View pending, past, and today's appointments at a glance.
- **Notifications**: Receive reminders for upcoming appointments.
- **Data Encryption**: All appointment data is securely encrypted for privacy.

## Installation

1. Clone the repository:
   git clone https://github.com/sage9705/appointmate.git
   cd appointmate

2. Create a virtual environment (optional but recommended):
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the required dependencies:
   pip install -r requirements.txt

4. Set up the environment variables:
   - Create a `.env` file in the root directory
   - Add the following lines to the `.env` file:
     ENCRYPTION_KEY=your_generated_key_here
     APPOINTMENTS_FILE=appointments.json
   - Replace `your_generated_key_here` with a valid Fernet encryption key

5. Run the application:
   python main.py

## Usage

### Main Window

The main window consists of a calendar view on the left and an appointment list on the right.

- **Calendar**: Click on any date to view appointments for that day.
- **Appointment List**: Displays appointments for the selected date.
- **Add Button**: Click to add a new appointment.
- **Search Button**: Click to search for specific appointments.
- **Delete Button**: Select an appointment and click to delete it.

### Adding an Appointment

1. Click the "Add" button.
2. Fill in the appointment details in the dialog that appears.
3. Click "Save" to add the appointment.

### Editing an Appointment

1. Double-click on an appointment in the list.
2. Modify the details in the edit dialog.
3. Click "Save" to update the appointment.

### Searching for Appointments

1. Click the "Search" button.
2. Enter your search criteria in the dialog.
3. View the search results in the displayed list.

### Deleting an Appointment

1. Select an appointment from the list.
2. Click the "Delete" button.
3. Confirm the deletion in the prompt that appears.

### Viewing Appointment Categories

Use the "Appointments" menu in the menu bar to view:
- Pending Appointments
- Past Appointments
- Today's Appointments

## Development

### Contributing

Contributions to AppointMate are welcome! Please feel free to submit a Pull Request.
