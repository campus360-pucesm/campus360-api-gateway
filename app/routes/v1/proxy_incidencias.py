from fastapi import APIRouter, Request, HTTPException, Depends
import httpx
from app.dependencies.auth_verifier import verify_token
from app.core.config import INCIDENCIAS_SERVICE_URL

router = APIRouter(prefix="/incidencias", tags=["Incidencias"])
http_client = httpx.AsyncClient()

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_incidencias(
    request: Request,
    path: str,
    authenticated_user: dict = Depends(verify_token) 
):
    target_url = f"{INCIDENCIAS_SERVICE_URL}/{path}"
    
    body = await request.body()
    headers = dict(request.headers)
    headers['X-User-ID'] = str(authenticated_user.get("user_id"))
    headers.pop("host", None)
    headers.pop("content-length", None)

    try:
        response = await http_client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            content=body
        )
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Upstream Error: {e.response.text}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Incidencias Service is unavailable: {str(e)}")
