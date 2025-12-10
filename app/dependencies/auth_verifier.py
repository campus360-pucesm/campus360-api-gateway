import httpx
from fastapi import HTTPException, Request
from app.core.config import AUTH_SERVICE_URL

async def verify_token(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing Authorization Header")
    
    # Example: call Auth Service to validate
    # Ensure AUTH_SERVICE_URL points to a validation endpoint like /validate?token=...
    # For now we just implement the call structure based on user request logic
    
    # We strip 'Bearer ' if present for cleaner passing? 
    # Or just pass the header as is.
    
    async with httpx.AsyncClient() as client:
        try:
            # Assuming auth service has a validate endpoint that accepts the token
            # Adjust the endpoint path as necessary based on actual Auth Service API
            response = await client.get(f"{AUTH_SERVICE_URL}/validate", params={"token": token})
            
            if response.status_code != 200:
                raise HTTPException(status_code=401, detail="Invalid Token")
            
            user_data = response.json()
            return user_data
            
        except httpx.RequestError:
            # Fallback if auth service is down
            raise HTTPException(status_code=503, detail="Auth Service Unavailable")
