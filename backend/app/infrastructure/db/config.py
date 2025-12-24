# backend/app/infrastructure/db/config.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Lembra que colocamos isso no docker-compose? O Python pega de lá.
DATABASE_URL = os.getenv("DATABASE_URL")

# Cria o motor de conexão
engine = create_engine(DATABASE_URL)

# Cria a fábrica de sessões. Cada requisição vai abrir uma sessão e fechar depois.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para criar as tabelas
Base = declarative_base()

# Função auxiliar para pegar o banco (Dependency Injection do FastAPI usa isso)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()