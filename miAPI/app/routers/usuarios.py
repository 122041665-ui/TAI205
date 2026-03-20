
from fastapi import FastAPI, status, HTTPException,Depends, APIRouter
from app.data.database import usuarios
from app.models.usuarios import crear_usuario
from app.security.auth import verificar_peticion

routerU = APIRouter(
    prefix= "/v1/usuario",
    tags= ['CRUD HTTP']
)

# 6. Endpoints de Consultas
# get
@routerU.get("/")
async def consultaT():
    return {
        "status": "200",
        "total": len(usuarios),
        "data": usuarios
    }

# get por id
@routerU.get("/{id}", status_code=status.HTTP_200_OK)
async def consulta_uno(id: int):
    for usr in usuarios:
        if usr["id"] == id:
            return {
                "mensaje": "usuario encontrado exitosamente",
                "status": "200",
                "usuario": usr
            }

    raise HTTPException(
        status_code=404,
        detail="el usuario no existe"
    )

# post
@routerU.post("/", status_code=status.HTTP_201_CREATED)
async def crea_usuario(usuario: crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="el usuario ya existe"
            )

    usuarios.append(usuario.dict())

    return {
        "mensaje": "usuario creado exitosamente",
        "usuario": usuario.dict()
    }

# put
@routerU.put("/{id}", status_code=status.HTTP_200_OK)
async def actualiza_usuario(id: int, usuario: dict):
    for usr in usuarios:
        if usr["id"] == id:
            usr["nombre"] = usuario.get("nombre", usr["nombre"])
            usr["edad"] = usuario.get("edad", usr["edad"])
            return {
                "mensaje": "usuario actualizado exitosamente",
                "status": "200",
                "usuario": usr
            }

    raise HTTPException(
        status_code=404,
        detail="el usuario no existe"
    )

# delete
@routerU.delete("/{id}", status_code=status.HTTP_200_OK)
async def elimina_usuario(id: int, userAuth: str = Depends(verificar_peticion)):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": f"usuario eliminado por {userAuth}",
            }

    raise HTTPException(
        status_code=404,
        detail="el usuario no existe"
    )