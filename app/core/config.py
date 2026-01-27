import os
from dotenv import load_dotenv

load_dotenv()

RESERVAS_SERVICE_URL = os.getenv("RESERVAS_SERVICE_URL", "http://localhost:8001/api/v1/reservas")
INCIDENCIAS_SERVICE_URL = os.getenv("INCIDENCIAS_SERVICE_URL", "http://localhost:8002/api/v1/tickets")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8003")
ATTENDANCE_SERVICE_URL = os.getenv("ATTENDANCE_SERVICE_URL", "http://localhost:8004")
SECRET_KEY = os.getenv("SECRET_KEY", "campus360-super-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

