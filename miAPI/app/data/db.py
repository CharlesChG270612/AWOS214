from sqlalchemy  import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

#1. definimos la url de la base de datos
DATABASE_URL = os.getenv(
    "DATABASE_URL"
    "postgresql://admin:123456@postgres:5434/DB_miapi"
)
#2. Creamos el motor de la conexion
engine = create_engine(DATABASE_URL)

#3. Creamos el gestionador de sesiones
SessionLocal= sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)