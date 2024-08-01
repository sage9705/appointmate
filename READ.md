# AppointMate - Appointment Management Application

**AppointMate** is a Python application built with PyQt5 that allows users to schedule, manage, search, and delete appointments. This README provides an overview of its features and usage.

## Features

### 1. Schedule Appointments

- Click the "Schedule Appointment" button to add new appointments.
- Enter appointment details, including name, reason, time, and additional comments.
- Appointments are associated with the selected date on the calendar.

### 2. Calendar Integration

- Utilizes a calendar widget to select and display dates.
- View and schedule appointments on the calendar.

### 3. Search Functionality

- Search for appointments by entering keywords in the search bar.
- Search criteria include appointment details and date.
- Displays search results in the label.

### 4. Delete Appointments

- Delete one or more appointments by selecting them and clicking the "Delete" button.
- A confirmation dialog appears before deletion.
- Supports multi-selection for easy deletion.

### 5. Menu System

- Features a menu bar with different appointment categories:
  - **Pending Appointments**: Lists pending appointments for future dates.
  - **Due Appointments**: Shows appointments due today.
  - **Past Appointments**: Displays past appointments.
  - **Delete Appointment**: Initiates the appointment deletion process.

### 6. Data Persistence

- Appointments are saved to a JSON file ("appointments.json") for data persistence.
- Automatically loads existing appointments upon startup.

### 7. Notification

- Checks for approaching appointments within the next 15 minutes.
- Notifies users with an information dialog.

## Usage

1. Run the application by executing the script (`main.py`).
2. The main window displays the calendar, search bar, label, and buttons.
3. Schedule appointments:
   - Click the "Schedule Appointment" button.
   - Enter name, reason, time, and optional comments.
   - Click "OK" to schedule the appointment.
4. Search for appointments:
   - Enter keywords in the search bar and click "Search."
   - Matching appointments are displayed in the label.
5. Delete appointments:
   - Click the "Delete Appointment" button.
   - Select appointments to delete and click "Delete."
   - Confirm the deletion in the confirmation dialog.
6. View different types of appointments using the menu:
   - "Pending Appointments," "Due Appointments," "Past Appointments."
7. Check for approaching appointments:
   - Appointments due within 15 minutes trigger a notification.

## Customization

- Customize the application's appearance by modifying the `style.css` file.
- Adjust the notification time interval by modifying the timer in the code.

## Dependencies

- PyQt5 for the graphical user interface.
- Python 3.x for running the application.

## License

This project is licensed under the MIT License, allowing you to use and modify it freely.

## Acknowledgments

AppointMate was developed with PyQt5, a powerful library for building GUI applications in Python. Thanks to the PyQt5 developers and the open-source community for their contributions.

Feel free to contribute, report issues, or provide feedback to enhance AppointMate.

## Author
Edem Godwin Kumahor

