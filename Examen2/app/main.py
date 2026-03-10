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

#Base de datos Ficticia para crear, listar, consultar por ID, confirmar reserva y cancelar reservaciones.   
reservaciones = [
    
]


         