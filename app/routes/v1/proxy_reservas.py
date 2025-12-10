from fastapi import APIRouter, Request, HTTPException, Depends
import httpx
from app.dependencies.auth_verifier import verify_token
from app.core.config import RESERVAS_SERVICE_URL

router = APIRouter(prefix="/reservas", tags=["Reservas"])
http_client = httpx.AsyncClient()

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_reservas(
    request: Request,
    path: str,
    # 1. Función Transversal: Se ejecuta antes de hacer el proxy
    authenticated_user: dict = Depends(verify_token) 
):
    # 2. Reconstrucción de la URL de destino
    # Note: request.url.path includes the prefix /reservas. 
    # If the backend service is mounted at /api/v1/reservas, we might simply append 'path'.
    # However, user example showed: target_url = f"{RESERVAS_SERVICE_URL}{request.url.path.replace('/api/v1/reservas', '')}"
    # But since we are inside a formatted scaffold, let's assume the router handles the stripping of prefix by using 'path' param if we use /{path:path}
    # Actually, simpler is to just use the path param.
    # If request is /reservas/123 -> path is 123
    # If backend is /api/v1/reservas/123 -> RESERVAS_SERVICE_URL + "/" + path
    
    # Let's check config default: http://reservas-service:8001/api/v1/reservas
    # So if we append /123 we get http://reservas-service:8001/api/v1/reservas/123
    
    target_url = f"{RESERVAS_SERVICE_URL}/{path}"
    
    # 3. Preparación de la Petición
    body = await request.body()
    headers = dict(request.headers)
    
    # OPCIONAL: Inyectar datos del usuario autenticado en los headers 
    # para que el Reservas-Service sepa quién es.
    headers['X-User-ID'] = str(authenticated_user.get("user_id")) # Assuming user_id based on auth service mock
    
    # Remove host header to avoid issues with proxying
    headers.pop("host", None)
    headers.pop("content-length", None) # Let httpx handle this

    # 4. Proxy de la Petición
    try:
        response = await http_client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            content=body
        )
        # Return simple response or parse json
        # Returning raw content to preserve original response exactly
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Upstream Error: {e.response.text}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Reservas Service is unavailable: {str(e)}")
