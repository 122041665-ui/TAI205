from typing import Optional
import asyncio
from app.data.database import usuarios
from fastapi import APIRouter

routerV= APIRouter (tags= ['inicio'])

# 5. Endpoints de Inicio
@routerV.get("/")
async def holaMundo():
    return {"mensaje": "Hola mundo desde FastApi"}

@routerV.get("/v1/bienvenidos")
async def bienvenidos():
    return {"mensaje": "Bienvenidos"}

@routerV.get("/v1/promedio")
async def promedio():
    await asyncio.sleep(2)  # Simulando una operación asíncrona
    return {
        "Calificacion": "7",
        "estatus": 200
    }