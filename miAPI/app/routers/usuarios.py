from fastapi import status,HTTPException,Depends,APIRouter
from app.models.usuario import usuario_create
from app.data.database import usuarios
from app.security.auth import verificar_Peticion

router = APIRouter(
    prefix= "/v1/usuarios", tags=["CRUD HTTP"]
)


    
@router.get("/{id}")  # Endpoint de inicio, todos los endpoints se acompañan de una función
async def leer_usuarios():
    return {
        "status":"200",
        "total": len(usuarios),
        "usuarios":usuarios
        }  # Formato JSON

@router.post("/{id}")  # Endpoint de inicio, todos los endpoints se acompañan de una función
async def crear_usuario(usuario:usuario_create):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario)
    return{
        "mensaje":"Usuario agregado",
        "Usuario":usuario
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