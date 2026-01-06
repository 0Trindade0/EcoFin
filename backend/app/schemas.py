from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Base para dados comuns
class AssetBase(BaseModel):
    symbol: str   # <--- MUDOU DE 'ticker' PARA 'symbol'
    name: str
    price: float
    sector: Optional[str] = None

# Usado para criar
class AssetCreate(AssetBase):
    pass

# Usado para responder (inclui ID e datas)
class AssetResponse(AssetBase):
    id: int
    change_percent: float  
    last_updated: datetime

    class Config:
        from_attributes = True