from fastapi import APIRouter, Request, HTTPException, Depends
import httpx
from app.dependencies.auth_verifier import verify_token
from app.core.config import INCIDENCIAS_SERVICE_URL

router = APIRouter(prefix="/tickets", tags=["Incidencias"])
http_client = httpx.AsyncClient(timeout=30.0, follow_redirects=True)

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
        
        # Verificar si la respuesta es exitosa
        if response.status_code >= 400:
            # Intentar obtener el detalle del error
            try:
                error_detail = response.json()
            except:
                error_detail = {"detail": response.text or "Error from incidencias service"}
            raise HTTPException(status_code=response.status_code, detail=error_detail)
        
        # Respuesta exitosa - intentar parsear como JSON
        try:
            return response.json()
        except Exception as e:
            # Si no es JSON válido, devolver el texto
            return {"message": response.text or "Empty response"}
            
    except HTTPException:
        # Re-raise HTTPException sin modificar
        raise
    except Exception as e:
        # Cualquier otro error (conexión, timeout, etc.)
        raise HTTPException(status_code=503, detail=f"Incidencias Service error: {str(e)}")


