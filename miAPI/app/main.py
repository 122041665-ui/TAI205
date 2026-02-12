#1.importaciones
from fastapi import FastAPI

#instalaciones APP
app = FastAPI()

#3. endpoint 
@app.get("/")
async def holamundo():
    return {"message": "Hola Mundo desde FastAPI"}

@app.get("/bienvenida")
async def bienvenida():
    return {"message": "Bienvenido a mi API con FastAPI"}