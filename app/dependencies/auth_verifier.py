from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from app.core.config import SECRET_KEY, ALGORITHM

security = HTTPBearer()

async def verify_token(request: Request):
    """
    Verify JWT token from Authorization header
    Decodes the token and extracts user information
    """
    auth_header = request.headers.get("Authorization")
    
    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing Authorization Header")
    
    # Extract token from "Bearer <token>"
    try:
        scheme, token = auth_header.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Authorization Header format")
    
    try:
        # Decode JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        role = payload.get("role")
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        
        return {
            "user_id": user_id,
            "role": role
        }
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

