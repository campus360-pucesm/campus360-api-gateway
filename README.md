# CAMPUS360 API Gateway

El **API Gateway** es el punto de entrada único para todo el ecosistema Campus360. Se encarga de enrutar las peticiones a los microservicios correspondientes, validar la autenticación y unificar la respuesta hacia el frontend.

## Tecnologías

*   **Python 3.10+** (FastAPI)
*   **Httpx**: Para el proxy inverso asíncrono.
*   **Docker**: Para contenerización.

## Configuración

Las variables de entorno se definen en `.env`:

```env
RESERVAS_SERVICE_URL=http://localhost:8001/api/v1/reservas
INCIDENCIAS_SERVICE_URL=http://localhost:8002/api/v1/incidencias
AUTH_SERVICE_URL=http://localhost:8003/api/v1/auth
```

## ▶Ejecución Local

1.  Instalar dependencias:
    ```bash
    pip install -r requirements.txt
    ```
2.  Iniciar el servidor:
    ```bash
    uvicorn app.main:app --reload --port 8000
    ```

## Ejecución con Docker

```bash
docker build -t campus360-gateway .
docker run -p 8000:8000 campus360-gateway
```
