from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.db.config import engine, Base, get_db
from app.infrastructure.db.repositories.stock_repository_impl import PostgresStockRepository
from app.application.stock_service import StockService
from pydantic import BaseModel
from app.infrastructure.worker.tasks import update_stock_price_task

# 1. Cria as tabelas no banco (Em prod usamos Alembic, mas aqui serve o create_all)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# DTO (Data Transfer Object) - Modelo de entrada da API (Isso não é Domínio!)
class StockCreateRequest(BaseModel):
    symbol: str
    name: str
    sector: str
    price: float

@app.post("/stocks/")
def create_stock(request: StockCreateRequest, db: Session = Depends(get_db)):
    # 2. Montando as peças (Injeção de Dependência Manual)
    
    # Camada Infra (Banco)
    repo = PostgresStockRepository(db)
    
    # Camada Aplicação (Service) recebe a Infra
    service = StockService(repo)
    
    try:
        # Camada Aplicação executa a lógica
        new_stock = service.create_stock(
            symbol=request.symbol,
            name=request.name,
            sector=request.sector,
            initial_price=request.price
        )
        return {"message": "Ação criada com sucesso", "stock": new_stock}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/stocks/{symbol}")
def get_stock(symbol: str, db: Session = Depends(get_db)):
    repo = PostgresStockRepository(db)
    stock = repo.get_by_symbol(symbol)
    if not stock:
        raise HTTPException(status_code=404, detail="Ação não encontrada")
    return stock

@app.post("/stocks/{symbol}/refresh")
def refresh_stock(symbol: str):
    """
    Endpoint assíncrono. Ele não atualiza o preço.
    Ele apenas manda um recado para o Worker: "Atualize aí!"
    """
    # .delay() é o comando mágico que envia para o Redis em vez de executar na hora
    task = update_stock_price_task.delay(symbol)
    
    return {
        "message": f"Solicitação de atualização enviada para {symbol}",
        "task_id": task.id,
        "status": "Processing in background"
    }