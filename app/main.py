from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.v1 import proxy_reservas, proxy_incidencias, proxy_auth, proxy_attendance

app = FastAPI(
    title="CAMPUS360 API Gateway",
    version="1.0.0",
    description="Gateway central para el ecosistema Campus360"
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

