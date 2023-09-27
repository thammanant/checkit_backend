from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from taskManagement import token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def getCurrentUser(data: str = Depends(oauth2_scheme)):
    credentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Permissions denied",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return token.verifyAccessToken(data, credentialsException)