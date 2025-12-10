from fastapi import FastAPI
from app.routes.v1 import proxy_reservas, proxy_incidencias

app = FastAPI(
    title="CAMPUS360 API Gateway",
    version="1.0.0",
    description="Gateway central para el ecosistema Campus360"
)

# Incluir routers de proxy
app.include_router(proxy_reservas.router, prefix="/api/v1")
app.include_router(proxy_incidencias.router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "api-gateway"}

@app.get("/")
def root():
    return {"message": "Welcome to Campus360 API Gateway"}
