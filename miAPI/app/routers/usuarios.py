from fastapi import status,HTTPException,Depends,APIRouter
from app.models.usuario import usuario_create
from app.data.database import usuarios
from app.security.auth import verificar_Peticion
from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario as usuarioDB

router = APIRouter(
    prefix= "/v1/usuarios", tags=["CRUD HTTP"]
)


    
@router.get("/")  # Endpoint de inicio, todos los endpoints se acompañan de una función
async def leer_usuarios(db:Session= Depends(get_db)):
    queryUsers=db.query(usuarioDB).all()

    return {
        "status":"200",
        "total": len(queryUsers),
        "usuarios":queryUsers
        }  # Formato JSON

@router.post("/")  # Endpoint de inicio, todos los endpoints se acompañan de una función
async def crear_usuario(usuarioP:usuario_create,db:Session=Depends(get_db)):
    nuevoUsuario=usuarioDB(nombre=usuarioP.nombre, edad=usuarioP.edad)

    db.add(nuevoUsuario)
    db.commit()
    db.refresh(nuevoUsuario)
    return{
        "mensaje":"Usuario agregado",
        "Usuario":usuarioP
    }

@router.put("/{id}")  # Endpoint de inicio, todos los endpoints se acompañan de una función
async def actualizar_usuario(usuario: dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            usuarios.append(usuario)
            return{
                "status":"200",
                "mensaje":"Usuario actualizado",
                "Usuario":usuario
            }
    raise HTTPException(
        status_code=400,
        
        detail="El id no existe, no se puede actualizar"
    )

@router.delete("/{id}",status_code=status.HTTP_200_OK)  # Endpoint de inicio, todos los endpoints se acompañan de una función
async def eliminar_usuario(usuario: dict, userAuth:str= Depends(verificar_Peticion)):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            usuarios.remove(usuario)
            return{
                "status":"200",
                "mensaje":f"Usuario eliminado por {userAuth}",
                "Usuario":usuario
            }
    raise HTTPException(
        status_code=400,
        detail="El id no existe, no se puede eliminar"
    )