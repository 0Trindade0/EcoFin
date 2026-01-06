from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware # NOVO: Importação
from sqlalchemy.orm import Session
from typing import List

# Importações da Clean Architecture
from app.infrastructure.db.config import engine, Base, get_db
from app.infrastructure.db.repositories.stock_repository_impl import PostgresStockRepository
from app.application.stock_service import StockService
from app.infrastructure.worker.tasks import update_stock_price_task
# Importa o arquivo schemas que acabamos de criar
from app import schemas 
import app.infrastructure.db.models 

# Cria tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Isso permite que o Frontend (localhost:3000) fale com o Backend
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ----------------------------------

# --- ROTAS ---

@app.get("/stocks/", response_model=List[schemas.AssetResponse])
def list_stocks(db: Session = Depends(get_db)):
    repo = PostgresStockRepository(db)
    # O repositório retorna Stock, o Pydantic converte para AssetResponse
    return repo.find_all()

@app.get("/stocks/{symbol}", response_model=schemas.AssetResponse)
def get_stock(symbol: str, db: Session = Depends(get_db)):
    repo = PostgresStockRepository(db)
    stock = repo.get_by_symbol(symbol)
    if not stock:
        raise HTTPException(status_code=404, detail="Ação não encontrada")
    return stock

@app.post("/stocks/", response_model=schemas.AssetResponse)
def create_stock(request: schemas.AssetBase, db: Session = Depends(get_db)):
    repo = PostgresStockRepository(db)
    service = StockService(repo)
    try:
        # Aqui fazemos a conversão do Schema (JSON) para o Service
        new_stock = service.create_stock(
            symbol=request.symbol, 
            name=request.name,
            sector=request.sector or "Unknown", # Garante que não vá nulo se o banco exigir
            initial_price=request.price
        )
        return new_stock
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/stocks/{symbol}/refresh")
def refresh_stock(symbol: str):
    task = update_stock_price_task.delay(symbol)
    return {
        "message": f"Solicitação de atualização enviada para {symbol}",
        "task_id": task.id,
        "status": "Processing in background"
    }