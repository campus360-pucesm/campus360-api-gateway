from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.v1 import proxy_reservas, proxy_incidencias, proxy_auth, proxy_attendance

app = FastAPI(
    title="CAMPUS360 API Gateway",
    version="1.0.0",
    description="""
Gateway central para el ecosistema Campus360

---

## 🔐 Módulo de Autenticación

Sistema de autenticación inteligente con control de acceso basado en QR.

### Endpoints Públicos:
- `POST /api/v1/auth/login` - Iniciar sesión (OAuth2)

### Endpoints QR Access (requieren autenticación):
- `GET /api/v1/auth/qr/me` - Obtener perfil del usuario actual
- `POST /api/v1/auth/qr/scan` - Escanear código QR de ubicación
- `GET /api/v1/auth/qr/history` - Historial de accesos
- `POST /api/v1/auth/qr/scan-advanced` - Escaneo con geolocalización

### Endpoints Admin (requieren rol admin):
- `GET /api/v1/auth/admin/users` - Listar usuarios
- `POST /api/v1/auth/admin/users` - Crear usuario
- `GET /api/v1/auth/admin/users/{id}` - Obtener usuario
- `PUT /api/v1/auth/admin/users/{id}` - Actualizar usuario
- `DELETE /api/v1/auth/admin/users/{id}` - Eliminar usuario
- `GET /api/v1/auth/admin/stats` - Estadísticas
- `POST /api/v1/auth/admin/qr/generate-location` - Generar QR de ubicación

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
- `GET /api/v1/recursos` - Consultar recursos disponibles
- `GET /api/v1/recursos/tipos` - Tipos de recursos
- `GET /api/v1/recursos/{id}/disponibilidad` - Disponibilidad de un recurso
- `POST /api/v1/reservas` - Crear reserva
- `GET /api/v1/reservas/usuario/{id}` - Reservas de un usuario
- `DELETE /api/v1/reservas/{id}` - Cancelar reserva
- `POST /api/v1/checkin` - Realizar check-in vía QR

### Flujo de Uso:
1. **Consultar recursos** - Ver qué hay disponible
2. **Ver disponibilidad** - Consultar horarios libres de un recurso
3. **Crear reserva** - Apartar un recurso para una fecha/hora
4. **Check-in vía QR** - Confirmar asistencia escaneando código QR

---

## 📋 Módulo de Asistencia

Sistema de registro de asistencia.

### Endpoints:
- `POST /api/v1/asistencia/registrar` - Registrar asistencia

---

## 🔧 Health Check

- `GET /health` - Estado del API Gateway
- `GET /api/v1/auth/health` - Estado del módulo Auth
- `GET /api/v1/reservas/health` - Estado del módulo Reservas
    """,
    openapi_tags=[
        {
            "name": "Auth Proxy",
            "description": "Proxy hacia el módulo de autenticación (puerto 8003)"
        },
        {
            "name": "Reservas Proxy", 
            "description": "Proxy hacia el módulo de reservas (puerto 8001)"
        },
        {
            "name": "Asistencia Proxy",
            "description": "Proxy hacia el módulo de asistencia (puerto 8004)"
        },
        {
            "name": "Incidencias Proxy",
            "description": "Proxy hacia el módulo de incidencias (puerto 8002)"
        }
    ]
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
    return {
        "message": "Welcome to Campus360 API Gateway",
        "docs": "/docs",
        "services": {
            "auth": "http://localhost:8003",
            "reservas": "http://localhost:8001", 
            "asistencia": "http://localhost:8004",
            "incidencias": "http://localhost:8002"
        }
    }