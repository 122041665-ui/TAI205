from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from fastapi import FastAPI, status, HTTPException,Depends

#seguridad http basic

security = HTTPBasic()
def verificar_peticion(credenciales: HTTPBasicCredentials = Depends(security)):
    userAuth = secrets.compare_digest(credenciales.username, "Rafael Resendiz")
    passAuth = secrets.compare_digest(credenciales.password, "123456")
    
    if not (userAuth and passAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales noa autorizadas",
        )
    return credenciales.username