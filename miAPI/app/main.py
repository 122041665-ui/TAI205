from fastapi import FastAPI, HTTPException, status
from typing import Optional
import asyncio


# 2. Inicialización APP
app = FastAPI(title='Mi PRIMER API', 
              description="Rafael Resendiz Vazquez ", 
              version='1.0.0')

#BD ficticia por el momento
usuarios = [
    {"id": "1", "nombre": "Rafael", "edad": "20"},
    {"id": "2", "nombre": "Berna", "edad": "25"},
    {"id": "3", "nombre": "Yahir", "edad": "30"},
]
# 3. Endpoints
@app.get("/", tags=['Inicio'])
async def holamundo():
    return {"mensaje": "Hola mundo FASTAPI"}

@app.get("/bienvenidos", tags=['Inicio'])
async def bienvenidos():
    return {"mensaje": "Bienvenidos"}

@app.get("/v1/promedio", tags=['Calificaciones'])
async def promedio():
    await asyncio.sleep(3)  # Peticion a otra api, consultaa otra base de datos, imula llamada externa
    return {
        "calificacion": "7.5",
        "estatus": "200"
    }

@app.get("/v1/usuario/{id}", tags=['Parametros'])
async def consultaUno(id: int):
    await asyncio.sleep(3)  # Peticion a otra api, consultaa otra base de datos, imula llamada externa
    return {"Resultado": "usuario encontrado",
            "Estatus": "200",
            }

@app.get("/v1/usuario-op/", tags=['Parametros Opcional'])
async def consultaUno(id: Optional[int] = None):
    await asyncio.sleep(2)  # Peticion a otra api, consultaa otra base de datos, imula llamada externa
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"usuario encontrado":id,"Datos": usuario}
            return{"Mensaje":"usuario no encontrado"}
        else:
            return {"Aviso":"No se proporciono id"}
    

@app.get("/v1/usuario/", tags=['CRUD HTTP'])
async def consultaT():
    return{
        "status":"200",
        "total": len(usuarios),
        "data": usuarios
    }


@app.post("/v1/usuarios/", tags=["CRUD HTTP"])
async def crear_usuario(usuario: dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code=400,
                detail="El usuario ya existe"
            )
    usuarios.append(usuario)
    return {
        "mensaje": "Usuario creado exitosamente",
        "status": "200",
        "usuario": usuario
    }       

@app.put("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def actualizar_usuario(id: int, usuario: dict):

    for usr in usuarios:
        if usr["id"] == str(id):
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
        if usr["id"] == str(id):
            usuarios.remove(usr)
            return {
                "mensaje": "Usuario eliminado correctamente",
                "status": "200"
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )
