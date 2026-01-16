from fastapi import APIRouter, Request, HTTPException, Depends
import httpx
from typing import Optional
from app.dependencies.auth_verifier import verify_token
from app.core.config import ATTENDANCE_SERVICE_URL

router = APIRouter(prefix="/attendance", tags=["Attendance Proxy"])
http_client = httpx.AsyncClient()

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_attendance(
    request: Request,
    path: str,
    authenticated_user: dict = Depends(verify_token)
):
    """
    Proxy requests to attendance service
    Requires valid authentication token
    """
    target_url = f"{ATTENDANCE_SERVICE_URL}/api/attendance/{path}"
    
    # Debug log
    print(f"Proxying attendance request to: {target_url}")
    
    body = await request.body()
    headers = dict(request.headers)
    headers['X-User-ID'] = str(authenticated_user.get("user_id", ""))
    headers['X-User-Role'] = str(authenticated_user.get("role", ""))
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
        raise HTTPException(status_code=e.response.status_code, detail=f"Attendance Service Error: {e.response.text}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Attendance Service is unavailable: {str(e)}")
