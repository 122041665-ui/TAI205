from fastapi import FastAPI, HTTPException, status
from typing import Optional
import asyncio
from pydantic import BaseModel, Field  # Agregar BaseModel pydantic

# 2. Inicialización APP
app = FastAPI(
    title="Mi primer API",
    description="Rafael Resendiz Vazquez",
    version="1.0.0"
)

# BD ficticia por el momento
usuarios = [
    {"id": 1, "nombre": "Fany", "edad": 21},
    {"id": 2, "nombre": "Aly", "edad": 21},
    {"id": 3, "nombre": "Dulce", "edad": 21},
]

# *************************
# Modelo de Validación Pydantic
# *************************
class crear_usuario(BaseModel):
    id: int = Field(..., ge=1)
    nombre: str = Field(..., min_length=1, max_length=60)
    edad: int = Field(..., ge=0, le=120)


# 3. Endpoints
@app.get("/", tags=["Inicio"])
async def holamundo():
    return {"mensaje": "Hola mundo FASTAPI"}


@app.get("/bienvenidos", tags=["Inicio"])
async def bienvenidos():
    return {"mensaje": "Bienvenidos"}


@app.get("/v1/promedio", tags=["Calificaciones"])
async def promedio():
    await asyncio.sleep(3)  # simula llamada externa
    return {
        "calificacion": "7.5",
        "estatus": "200"
    }


@app.get("/v1/usuario/{id}", tags=["Parametros"])
async def consulta_uno(id: int):
    await asyncio.sleep(3)  # simula llamada externa
    return {
        "Resultado": "usuario encontrado",
        "Estatus": "200",
    }


@app.get("/v1/usuario-op/", tags=["Parametros Opcional"])
async def consulta_uno_op(id: Optional[int] = None):
    await asyncio.sleep(2)  # simula llamada externa

    if id is None:
        return {"Aviso": "No se proporciono id"}

    for usuario in usuarios:
        if usuario["id"] == id:
            return {"usuario encontrado": id, "Datos": usuario}

    return {"Mensaje": "usuario no encontrado"}


@app.get("/v1/usuario/", tags=["CRUD HTTP"])
async def consulta_todos():
    return {
        "status": "200",
        "total": len(usuarios),
        "data": usuarios
    }


# 3. Usamos el modelo en nuestro EndPoint POST:
@app.post("/v1/usuarios/", tags=["CRUD HTTP"], status_code=status.HTTP_201_CREATED)
async def crear_usuario_endpoint(usuario: crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )

    nuevo = usuario.model_dump()  # Pydantic -> dict
    usuarios.append(nuevo)

    return {
        "mensaje": "Usuario Agregado",
        "Usuario": nuevo
    }


@app.put("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def actualizar_usuario(id: int, usuario: dict):
    for usr in usuarios:
        if usr["id"] == id:
            usr["nombre"] = usuario.get("nombre", usr["nombre"])
            usr["edad"] = usuario.get("edad", usr["edad"])
            return {
                "mensaje": "Usuario actualizado correctamente",
                "status": "200",
                "usuario": usr
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


@app.delete("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def eliminar_usuario(id: int):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": "Usuario eliminado correctamente",
                "status": "200"
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )