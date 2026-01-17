import os
from dotenv import load_dotenv

load_dotenv()

RESERVAS_SERVICE_URL = os.getenv("RESERVAS_SERVICE_URL", "http://reservas-service:8001/api/v1/reservas")
INCIDENCIAS_SERVICE_URL = os.getenv("INCIDENCIAS_SERVICE_URL", "http://incidencias-service:8002/api/v1/incidencias")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8003")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

