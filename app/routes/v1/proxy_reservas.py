from fastapi import APIRouter, Request, HTTPException, Depends
import httpx
from app.dependencies.auth_verifier import verify_token
from app.core.config import RESERVAS_SERVICE_URL

router = APIRouter(tags=["Modulo Reservas"])
http_client = httpx.AsyncClient()

# URL base del microservicio de reservas
RESERVAS_BASE_URL = "http://localhost:8001"  # Ajustar según tu configuración


# ============== ENDPOINTS PÚBLICOS (sin autenticación) ==============

@router.get("/reservas-service/health")
async def health_check():
    """Verificar si el servicio de reservas está disponible"""
    try:
        response = await http_client.get(f"{RESERVAS_BASE_URL}/health")
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Reservas Service is unavailable: {str(e)}")


# ============== RECURSOS (requiere autenticación) ==============

@router.api_route("/recursos/{path:path}", methods=["GET"])
async def proxy_recursos(
    request: Request,
    path: str,
    authenticated_user: dict = Depends(verify_token)
):
    """Proxy para endpoints de recursos"""
    target_url = f"{RESERVAS_BASE_URL}/recursos/{path}"
    return await _proxy_request(request, target_url, authenticated_user)


@router.get("/recursos")
async def proxy_recursos_root(
    request: Request,
    authenticated_user: dict = Depends(verify_token)
):
    """Proxy para listar recursos"""
    target_url = f"{RESERVAS_BASE_URL}/recursos/"
    return await _proxy_request(request, target_url, authenticated_user)


# ============== RESERVAS (requiere autenticación) ==============

@router.api_route("/reservas/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_reservas(
    request: Request,
    path: str,
    authenticated_user: dict = Depends(verify_token)
):
    """Proxy para endpoints de reservas"""
    target_url = f"{RESERVAS_BASE_URL}/reservas/{path}"
    return await _proxy_request(request, target_url, authenticated_user)


@router.api_route("/reservas", methods=["GET", "POST"])
async def proxy_reservas_root(
    request: Request,
    authenticated_user: dict = Depends(verify_token)
):
    """Proxy para crear/listar reservas"""
    target_url = f"{RESERVAS_BASE_URL}/reservas/"
    return await _proxy_request(request, target_url, authenticated_user)


# ============== CHECK-IN (requiere autenticación) ==============

@router.api_route("/checkin/{path:path}", methods=["GET", "POST"])
async def proxy_checkin(
    request: Request,
    path: str,
    authenticated_user: dict = Depends(verify_token)
):
    """Proxy para endpoints de check-in"""
    target_url = f"{RESERVAS_BASE_URL}/checkin/{path}"
    return await _proxy_request(request, target_url, authenticated_user)


@router.api_route("/checkin", methods=["GET", "POST"])
async def proxy_checkin_root(
    request: Request,
    authenticated_user: dict = Depends(verify_token)
):
    """Proxy para realizar check-in"""
    target_url = f"{RESERVAS_BASE_URL}/checkin/"
    return await _proxy_request(request, target_url, authenticated_user)


# ============== FUNCIÓN HELPER PARA PROXY ==============

async def _proxy_request(request: Request, target_url: str, authenticated_user: dict):
    """Función común para hacer proxy de requests"""
    body = await request.body()
    headers = dict(request.headers)
    
    # Inyectar datos del usuario autenticado
    headers['X-User-ID'] = str(authenticated_user.get("user_id", ""))
    headers['X-User-Role'] = str(authenticated_user.get("role", ""))
    
    # Limpiar headers problemáticos
    headers.pop("host", None)
    headers.pop("content-length", None)

    try:
        response = await http_client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            content=body,
            params=request.query_params  # Pasar query params también
        )
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Upstream Error: {e.response.text}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Reservas Service is unavailable: {str(e)}")