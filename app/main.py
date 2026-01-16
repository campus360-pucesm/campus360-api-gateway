from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.v1 import proxy_reservas, proxy_incidencias, proxy_auth, proxy_attendance

app = FastAPI(
    title="CAMPUS360 API Gateway",
    version="1.0.0",
    description="""
Gateway central para el ecosistema Campus360

---

## 📅 Módulo de Reservas

Sistema de Reservas de Recursos Universitarios que permite gestionar:

### Recursos Disponibles:
- **5 Salas de Estudio** (capacidad: 10 personas c/u)
- **5 Laboratorios de Computación** (capacidad: 20 personas c/u)
- **5 Módulos de Biblioteca** (capacidad: 4 personas c/u)
- **20 Parqueaderos** (capacidad: 1 vehículo c/u)
- **5 Equipos** (proyectores, laptops, cámara)

### Endpoints del Módulo:
- `/api/v1/recursos` - Consultar recursos disponibles
- `/api/v1/reservas` - Crear y gestionar reservas
- `/api/v1/checkin` - Realizar check-in vía QR

### Flujo de Uso:
1. **Consultar recursos** - Ver qué hay disponible
2. **Ver disponibilidad** - Consultar horarios libres de un recurso
3. **Crear reserva** - Apartar un recurso para una fecha/hora
4. **Check-in vía QR** - Confirmar asistencia escaneando código QR

### Control de Capacidad:
- Cada recurso tiene una capacidad máxima
- El check-in cuenta asistentes hasta llenar capacidad
- Cuando está lleno: "Capacidad completa, no hay más lugares"
    """
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers de proxy
app.include_router(proxy_auth.router, prefix="/api/v1")
app.include_router(proxy_reservas.router, prefix="/api/v1")
app.include_router(proxy_incidencias.router, prefix="/api/v1")
app.include_router(proxy_attendance.router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "api-gateway"}

@app.get("/")
def root():
    return {"message": "Welcome to Campus360 API Gateway"}