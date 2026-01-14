from fastapi import APIRouter, Request, HTTPException, Depends
import httpx
from typing import Optional
from app.dependencies.auth_verifier import verify_token
from app.core.config import AUTH_SERVICE_URL

router = APIRouter(prefix="/auth", tags=["Auth Proxy"])
http_client = httpx.AsyncClient()

# Public endpoint - no authentication required
@router.post("/login")
async def proxy_login(request: Request):
    """
    Proxy login requests to auth service
    This endpoint is public and does not require authentication
    """
    target_url = f"{AUTH_SERVICE_URL}/auth/login"
    
    body = await request.body()
    headers = dict(request.headers)
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
        raise HTTPException(status_code=e.response.status_code, detail=f"Auth Error: {e.response.text}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Auth Service is unavailable: {str(e)}")


# QR Access endpoints - require authentication
@router.api_route("/qr/{path:path}", methods=["GET", "POST"])
async def proxy_qr(
    request: Request,
    path: str,
    authenticated_user: dict = Depends(verify_token)
):
    """
    Proxy QR access requests to auth service
    Requires valid authentication token
    """
    target_url = f"{AUTH_SERVICE_URL}/qr/{path}"
    
    body = await request.body()
    headers = dict(request.headers)
    headers['X-User-ID'] = str(authenticated_user.get("user_id", ""))
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
        raise HTTPException(status_code=e.response.status_code, detail=f"Auth Error: {e.response.text}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Auth Service is unavailable: {str(e)}")


# Admin endpoints - require authentication
@router.api_route("/admin/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_admin(
    request: Request,
    path: str,
    authenticated_user: dict = Depends(verify_token)
):
    """
    Proxy admin requests to auth service
    Requires valid authentication token
    """
    target_url = f"{AUTH_SERVICE_URL}/admin/{path}"
    
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
        
        # Handle different response types (JSON, images, etc.)
        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            return response.json()
        else:
            # For non-JSON responses (like QR code images), return raw content
            from fastapi.responses import Response
            return Response(
                content=response.content,
                media_type=content_type,
                headers=dict(response.headers)
            )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Auth Error: {e.response.text}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Auth Service is unavailable: {str(e)}")


# Health check endpoint
@router.get("/health")
async def proxy_health():
    """Check if auth service is reachable"""
    try:
        response = await http_client.get(f"{AUTH_SERVICE_URL}/health")
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Auth Service is unavailable: {str(e)}")
