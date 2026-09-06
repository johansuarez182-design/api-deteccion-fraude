"""
Configuración de la conexión a la base de datos.

La cadena de conexión se lee de la variable de entorno DATABASE_URL
(definida en el archivo .env), nunca escrita directamente en el código.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise RuntimeError(
        "No se encontró la variable DATABASE_URL. "
        "Copia .env.example como .env y define tu cadena de conexión."
    )

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependencia de FastAPI: entrega una sesión de BD y la cierra al terminar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
