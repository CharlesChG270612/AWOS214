from fastapi import FastAPI  
import asyncio
#Instancia del servidor
app = FastAPI()

@app.get("/")  # Endpoint de inicio, todos los endpoints se acompañan de una función
async def bienvenida():
    return {"mensaje": "¡Bienvenido a mi API!"}  # Formato JSON

@app.get("/HolaMundo")  # Endpoint
async def hola():
    await asyncio.sleep(7)#Simulacion de uns 
    return {"mensaje": "¡Hola Mundo FastAPI!",
            "estatus":"200"
            }  # Formato JSON