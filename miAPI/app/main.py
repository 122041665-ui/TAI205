# ==========================================
# Importaciones principales del proyecto
# ==========================================

from fastapi import FastAPI, HTTPException, status
from typing import Optional
import asyncio
from pydantic import BaseModel, Field


# ==========================================
# Inicialización de la aplicación
# Rafael Reséndiz Vázquez - API de práctica
# ==========================================

app = FastAPI(
    title="Mi PRIMER API",
    description="Rafael Reséndiz Vazquez",
    version="1.0.0"
)


# ==========================================
# Base de datos ficticia (simulación temporal)
# Se manejan tipos correctos para trabajar con Pydantic
# ==========================================

usuarios = [
    {"id": 1, "nombre": "Rafael", "edad": 20},
    {"id": 2, "nombre": "Berna", "edad": 25},
    {"id": 3, "nombre": "Yahir", "edad": 30},
]


# ==========================================
# Modelo de validación con Pydantic
# Se agregan validaciones personalizadas
# ==========================================

class CrearUsuario(BaseModel):
    id: int = Field(..., gt=0, description="Identificador único del usuario")
    nombre: str = Field(..., min_length=3, max_length=50, example="Juanita")
    edad: int = Field(..., ge=1, le=123, description="Edad válida entre 1 y 123 años")


# ==========================================
# Endpoints básicos
# ==========================================

@app.get("/", tags=["Inicio"])
async def holamundo():
    return {"mensaje": "Hola mundo FASTAPI"}


@app.get("/bienvenidos", tags=["Inicio"])
async def bienvenidos():
    return {"mensaje": "Bienvenidos"}


# ==========================================
# Simulación de llamada externa con asyncio
# ==========================================

@app.get("/v1/promedio", tags=["Calificaciones"])
async def promedio():
    await asyncio.sleep(3)  # Simulación de consulta externa
    return {
        "calificacion": "7.5",
        "estatus": "200"
    }


# ==========================================
# Consulta de usuario por ID (parámetro obligatorio)
# ==========================================

@app.get("/v1/usuario/{id}", tags=["Parametros"])
async def consulta_uno(id: int):

    for usuario in usuarios:
        if usuario["id"] == id:
            return {
                "resultado": "Usuario encontrado",
                "estatus": "200",
                "data": usuario
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


# ==========================================
# Consulta con parámetro opcional
# ==========================================

@app.get("/v1/usuario-op/", tags=["Parametros Opcional"])
async def consulta_opcional(id: Optional[int] = None):

    if id is None:
        return {"aviso": "No se proporcionó ID"}

    for usuario in usuarios:
        if usuario["id"] == id:
            return {"usuario encontrado": usuario}

    return {"mensaje": "Usuario no encontrado"}


# ==========================================
# Obtener todos los usuarios
# ==========================================

@app.get("/v1/usuarios/", tags=["CRUD HTTP"])
async def consultar_todos():
    return {
        "status": "200",
        "total": len(usuarios),
        "data": usuarios
    }


# ==========================================
# Crear nuevo usuario con validación Pydantic
# ==========================================

@app.post("/v1/usuarios/", tags=["CRUD HTTP"], status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario: CrearUsuario):

    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El ID ya existe"
            )

    usuarios.append(usuario.dict())

    return {
        "mensaje": "Usuario agregado correctamente",
        "usuario": usuario
    }


# ==========================================
# Actualizar usuario existente
# ==========================================

@app.put("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def actualizar_usuario(id: int, usuario: dict):

    for usr in usuarios:
        if usr["id"] == id:
            usr["nombre"] = usuario.get("nombre", usr["nombre"])
            usr["edad"] = usuario.get("edad", usr["edad"])

            return {
                "mensaje": "Usuario actualizado correctamente",
                "usuario": usr
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


# ==========================================
# Eliminar usuario
# ==========================================

@app.delete("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def eliminar_usuario(id: int):

    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": "Usuario eliminado correctamente"
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )