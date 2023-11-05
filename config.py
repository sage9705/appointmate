import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APPOINTMENTS_FILE = os.path.join(BASE_DIR, os.getenv('APPOINTMENTS_FILE', 'appointments.json'))
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')

if not ENCRYPTION_KEY:
    raise ValueError("ENCRYPTION_KEY is not set in the environment variables")