import requests
from fastapi import HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import USERS_SERVICE_URL

auth_scheme = HTTPBearer()


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    token = credentials.credentials
    try:
        response = requests.post(
            f"{USERS_SERVICE_URL}/api/users/verify-token",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5,
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=401, detail="Token inválido")
    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=500,
            detail="Error al comunicarse con el servicio de autenticación",
        )
