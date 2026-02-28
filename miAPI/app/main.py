# ============================
# 1. IMPORTACIONES
# ============================
from fastapi import FastAPI, status, HTTPException
from typing import Optional
from pydantic import BaseModel, Field
import asyncio

# ============================
# 2. INSTANCIA DEL SERVIDOR
# ============================
app = FastAPI(
    title="Mi primer API",
    description="Ivan Isay Guerra L",
    version="1.0"
)

# ============================
# 3. BASE DE DATOS SIMULADA
# ============================
usuarios = [
    {"id": 1, "nombre": "Fany", "edad": 21},
    {"id": 2, "nombre": "Aly", "edad": 21},
    {"id": 3, "nombre": "Dulce", "edad": 21},
]

# ============================
# 4. MODELO DE VALIDACIÓN PYDANTIC
# ============================
class crear_usuario(BaseModel):
    id: int = Field(gt=0, description="Identificador de usuario")
    nombre: str = Field(..., min_length=3, max_length=50, example="Juanita")
    edad: int = Field(..., ge=1, le=123, description="Edad válida entre 1 y 123")


# ============================
# 5. ENDPOINTS BÁSICOS
# ============================
@app.get("/", tags=["Inicio"])
async def holamundo():
    return {"message": "Hola Mundo desde FastAPI"}


@app.get("/v1/bienvenida", tags=["Inicio"])
async def bienvenida():
    return {"message": "Bienvenido a mi API con FastAPI"}


@app.get("/v1/promedios", tags=["Calificacion"])
async def promedios():
    await asyncio.sleep(3)
    return {
        "promedio": 85.5,
        "estatus": "200"
    }


@app.get("/v1/usuario/{id}", tags=["Parametros"])
async def consulta_uno(id: int):
    await asyncio.sleep(2)

    for usuario in usuarios:
        if usuario["id"] == id:
            return {
                "resultado": "Usuario encontrado",
                "datos": usuario,
                "estatus": "200"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )


@app.get("/v1/usuarios_op/", tags=["Parametro Opcional"])
async def consulta_op(id: Optional[int] = None):
    await asyncio.sleep(2)

    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {
                    "Usuario encontrado": id,
                    "Datos": usuario
                }
        return {"Mensaje": "Usuario no encontrado"}
    else:
        return {"Aviso": "No se proporciono Id"}


# ============================
# 6. ENDPOINT POST (CREAR USUARIO)
# ============================
@app.post(
    "/v1/usuarios/",
    tags=["CRUD HTTP"],
    status_code=status.HTTP_201_CREATED
)
async def crear_usuario_endpoint(usuario: crear_usuario):

    # Validamos que no exista el ID
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El id ya existe"
            )

    usuarios.append(usuario.dict())

    return {
        "mensaje": "Usuario Agregado",
        "Usuario": usuario
    }