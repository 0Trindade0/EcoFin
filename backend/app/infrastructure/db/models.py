# backend/app/infrastructure/db/models.py
from sqlalchemy import Column, String, Float, DateTime, Integer
from datetime import datetime
from app.infrastructure.db.config import Base

class StockModel(Base):
    """
    Representação da tabela 'stocks' no banco de dados.
    """
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True) # O banco precisa de ID, o domínio talvez não
    symbol = Column(String, unique=True, index=True)
    name = Column(String)
    sector = Column(String)
    price = Column(Float)
    last_updated = Column(DateTime, default=datetime.now)