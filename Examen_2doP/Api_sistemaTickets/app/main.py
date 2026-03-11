from fastapi import FastAPI, status, HTTPException, Depends
from typing import Literal
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app = FastAPI(
    title="API de sistema de tickets",
    description="Carlos",
    version="1.0.0"
)

ticket = [
    {"id": 1, "nombre": "Juan", "descripcion": "Compra de artículos varios", "prioridad": "baja", "estado": "pendiente"},
    {"id": 2, "nombre": "Israel", "descripcion": "Compra de insumos", "prioridad": "media", "estado": "pendiente"},
    {"id": 3, "nombre": "Sofi", "descripcion": "Compra urgente", "prioridad": "alta", "estado": "pendiente"}
]

class TicketCreate(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario")
    nombre: str = Field(..., min_length=5, example="Juanita")
    descripcion: str = Field(..., min_length=20, max_length=200, description="Descripción detallada de la compra")
    prioridad: Literal["baja", "media", "alta"]
    estado: str = Field(default="pendiente")

security = HTTPBasic()

def verificar_usuarios(credenciales: HTTPBasicCredentials = Depends(security)):
    userAuth = secrets.compare_digest(credenciales.username, "soporte")
    passAuth = secrets.compare_digest(credenciales.password, "4321")

    if not (userAuth and passAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no autorizadas"
        )
    return credenciales.username

@app.get("/tickets/", response_model=list[TicketCreate])
def listar_tickets(usuario: str = Depends(verificar_usuarios)):
    return ticket

@app.get("/tickets/{id}", response_model=TicketCreate)
def consultar_ticket(id: int, usuario: str = Depends(verificar_usuarios)):
    for t in ticket:
        if t["id"] == id:
            return t
    raise HTTPException(status_code=404, detail="Ticket no encontrado")

@app.post("/tickets/", response_model=TicketCreate)
def crear_ticket(nuevo_ticket: TicketCreate, usuario: str = Depends(verificar_usuarios)):
    for t in ticket:
        if t["id"] == nuevo_ticket.id:
            raise HTTPException(status_code=400, detail="El ticket ya existe")
    ticket.append(nuevo_ticket.dict())
    return nuevo_ticket

@app.put("/tickets/{id}", response_model=TicketCreate)
def cambiar_estado(id: int, nuevo_estado: str, usuario: str = Depends(verificar_usuarios)):
    for t in ticket:
        if t["id"] == id:
            t["estado"] = nuevo_estado
            return t
    raise HTTPException(status_code=404, detail="Ticket no encontrado")

@app.delete("/tickets/{id}")
def eliminar_ticket(id: int, usuario: str = Depends(verificar_usuarios)):
    for t in ticket:
        if t["id"] == id:
            ticket.remove(t)
            return {"mensaje": "Ticket eliminado"}
    raise HTTPException(status_code=404, detail="Ticket no encontrado")