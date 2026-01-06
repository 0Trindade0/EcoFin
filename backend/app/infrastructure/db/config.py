import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# MUDANÇA AQUI: Adicionamos um valor padrão caso a variável de ambiente falhe
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://user:password@db:5432/ecofin_db"
)

# Se mesmo com o padrão vier vazio ou None (erro de sistema), lançamos erro claro
if not DATABASE_URL:
    raise ValueError("A variável DATABASE_URL não foi definida!")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()