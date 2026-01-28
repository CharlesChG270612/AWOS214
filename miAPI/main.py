from fastapi import FastAPI  # <-- Corregido: FastAPI, no FASTAPI

app = FastAPI()  # <-- Corregido: FastAPI()

@app.get("/")  # Endpoint de inicio, todos los endpoints se acompañan de una función
async def bienvenida():
    return {"mensaje": "¡Bienvenido a mi API!"}  # Formato JSON
