from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
# Importa o Base do arquivo config.py que está na mesma pasta (.config)
from .config import Base

class StockModel(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    name = Column(String)
    sector = Column(String)
    price = Column(Float)
    change_percent = Column(Float, default=0.0)
    last_updated = Column(DateTime, default=datetime.utcnow)