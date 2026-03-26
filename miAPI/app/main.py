# 1. Importaciones
from fastapi import FastAPI
from app.routers import usuarios,varios
from app.data.db import engine
from app.data import usuario

usuario.Base.metadata.create_all(bind=engine)

# 2. Inicialización de la APP
app = FastAPI(
    title='Mi PRIMER API', 
    description="Rafael", 
    version='1.0.0'
)

app.include_router(usuarios.routerU)
app.include_router(varios.routerV)

