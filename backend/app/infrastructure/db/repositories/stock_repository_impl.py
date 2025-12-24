# backend/app/infrastructure/db/repositories/stock_repository_impl.py
from typing import Optional
from sqlalchemy.orm import Session
from app.domain.entities.stock import Stock
from app.domain.ports.stock_repository import StockRepository
from app.infrastructure.db.models import StockModel

class PostgresStockRepository(StockRepository):
    def __init__(self, db_session: Session):
        self.db = db_session

    def save(self, stock: Stock) -> Stock:
        # 1. Converter Domínio -> Modelo SQL (Mapper)
        stock_model = self.db.query(StockModel).filter(StockModel.symbol == stock.symbol).first()

        if stock_model:
            # Atualiza existente
            stock_model.price = stock.price
            stock_model.last_updated = stock.last_updated
        else:
            # Cria novo
            stock_model = StockModel(
                symbol=stock.symbol,
                name=stock.name,
                sector=stock.sector,
                price=stock.price,
                last_updated=stock.last_updated
            )
            self.db.add(stock_model)

        # 2. Persistir no Banco
        self.db.commit()
        self.db.refresh(stock_model)

        # 3. Converter Modelo SQL -> Domínio (Mapper Reverso)
        # O resto da aplicação só entende 'Stock', não 'StockModel'
        return Stock(
            symbol=stock_model.symbol,
            name=stock_model.name,
            sector=stock_model.sector,
            price=stock_model.price,
            last_updated=stock_model.last_updated
        )

    def get_by_symbol(self, symbol: str) -> Optional[Stock]:
        stock_model = self.db.query(StockModel).filter(StockModel.symbol == symbol).first()
        
        if not stock_model:
            return None
        
        return Stock(
            symbol=stock_model.symbol,
            name=stock_model.name,
            sector=stock_model.sector,
            price=stock_model.price,
            last_updated=stock_model.last_updated
        )