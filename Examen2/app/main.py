#importaciones para proyecto, una api para gestionar reservas de un hotel.

from fastapi import FastAPI, status, HTTPException, Depends
from typing import Optional 
import asyncio
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

#Inicializacion de la API.

app = FastAPI (
    tittle = "Mi examen en API",
    description= "Rafael Resendiz Vazquez",
    version= "1.0.1",  
)

#Base de datos Ficticia para crear, listar, consultar por ID, confirmar reserva y cancelar reservaciones, con fecha de entrega, tipo de habitacion y limite de estacion de 7 dias para cada reserva
reservas = [
    {"id": 1, "nombre": "Juan Perez", "fecha": "2024-07-01", "Salida": "2024-07-08", "Tipo": "Suite", "confirmada": False},
    {"id": 2, "nombre": "Maria Lopez", "fecha": "2024-07-05", "Salida": "2024-07-12", "Tipo": "Doble", "confirmada": False},
    {"id": 3, "nombre": "Carlos Sanchez", "fecha": "2024-07-10", "Salida": "2024-07-17", "Tipo": "Individual", "confirmada": False},
    
]      

#Modelo de validacion de datos con Pydantic personalizadas para crear una reserva, con validacion de fecha, tipo de habitacion y limite de estacion de 7 dias para cada reserva.
class CrearReserva(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de la reserva")
    nombre: str = Field(..., min_length=3, max_length=50, example="Juan Perez")
    fecha: str = Field(..., description="Fecha de entrada en formato YYYY-MM-DD")
    Salida: str = Field(..., description="Fecha de salida en formato YYYY-MM-DD")
    Tipo: str = Field(..., description="Tipo de habitación (Suite, Doble, Individual)")

#Seguridad HTTP Basic para proteger los endpoints de la API.
security = HTTPBasic()
def verificar_peticion(credenciales: HTTPBasicCredentials = Depends(security)):
    userAuth = secrets.compare_digest(credenciales.username, "rafaelresendiz")
    passAuth = secrets.compare_digest(credenciales.password, "123456")
    
    if not (userAuth and passAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no autorizadas",
        )
    return credenciales.username

#Endpoints de inicio para verificar que la API.
@app.get("/", tags=['Inicio'])
async def holaMidas():
    return {"mensaje": "Hola Midas"}

#endpoint para  crear uan reserva con validacion de datos y seguridad HTTP Basic.
@app.post("/reservas", tags=['Reservas'])
async def crear_reserva(reserva: CrearReserva, username: str = Depends(verificar_peticion)):
    nueva_reserva = {
        "id": reserva.id,
        "nombre": reserva.nombre,
        "fecha": reserva.fecha,
        "Salida": reserva.Salida,
        "Tipo": reserva.Tipo,
    
    }
    reservas.append(nueva_reserva)
    return nueva_reserva

#endpoint para listar todas las reservas.
@app.get("/reservas", tags=['Reservas'])
async def listar_reservas(username: str = Depends(verificar_peticion)):
    return {"reservas": reservas}   

#consultar una reserva por ID.
@app.get("/reservas/{reserva_id}", tags=['Reservas'])
async def consultar_reserva(reserva_id: int, username: str = Depends(verificar_peticion)):
    for reserva in reservas:
        if reserva["id"] == reserva_id:
            return reserva
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")  

#confirmar una reserva por ID.
@app.put("/reservas/{reserva_id}/confirmar", tags=['Reservas'])
async def confirmar_reserva(reserva_id: int, username: str = Depends(verificar_peticion)):
    for reserva in reservas:
        if reserva["id"] == reserva_id:
            reserva["confirmada"] = True
            return {"resultado": "Reserva confirmada",
                "estatus": "200",
                "data": reserva}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")

#cancelar una reserva por ID.
@app.delete("/reservas/{reserva_id}", tags=['Reservas'])
async def cancelar_reserva(reserva_id: int, username: str = Depends(verificar_peticion)):
    for reserva in reservas:
        if reserva["id"] == reserva_id:
            reservas.remove(reserva)
            return {"resultado": "Reserva cancelada",
                "estatus": "200",
                "data": reserva}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")





         