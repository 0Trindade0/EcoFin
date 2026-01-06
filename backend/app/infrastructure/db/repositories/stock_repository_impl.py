from sqlalchemy.orm import Session
from typing import Optional, List
from app.domain.entities.stock import Stock
from app.domain.ports.stock_repository import StockRepository
from app.infrastructure.db.models import StockModel

class PostgresStockRepository(StockRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, stock: Stock) -> Stock:
        # Se o stock já tem ID, é uma atualização. Se não, é criação.
        # Por simplificação, aqui tratamos como um "Upsert" básico ou criação nova
        
        # Tenta buscar se já existe pelo Símbolo (para atualizar preço)
        db_stock = self.db.query(StockModel).filter(StockModel.symbol == stock.symbol).first()
        
        if db_stock:
            # Atualiza existente
            db_stock.price = stock.price
            db_stock.change_percent = stock.change_percent
            db_stock.name = stock.name
            db_stock.sector = stock.sector
            db_stock.last_updated = stock.last_updated
        else:
            # Cria novo
            db_stock = StockModel(
                symbol=stock.symbol,
                name=stock.name,
                sector=stock.sector,
                price=stock.price,
                change_percent=stock.change_percent,
                last_updated=stock.last_updated
            )
            self.db.add(db_stock)
        
        self.db.commit()
        self.db.refresh(db_stock)
        
        # IMPORTANTE: Retorna a entidade com o ID do banco
        return Stock(
            id=db_stock.id,  # <--- O ID VEM DAQUI
            symbol=db_stock.symbol,
            name=db_stock.name,
            sector=db_stock.sector,
            price=db_stock.price,
            last_updated=db_stock.last_updated
        )

    def get_by_symbol(self, symbol: str) -> Optional[Stock]:
        db_stock = self.db.query(StockModel).filter(StockModel.symbol == symbol).first()
        if db_stock:
            return Stock(
                id=db_stock.id, # <--- OBRIGATÓRIO PASSAR O ID
                symbol=db_stock.symbol,
                name=db_stock.name,
                sector=db_stock.sector,
                price=db_stock.price,
                last_updated=db_stock.last_updated
            )
        return None

    def find_all(self) -> List[Stock]:
        db_stocks = self.db.query(StockModel).all()
        return [
            Stock(
                id=s.id, # <--- OBRIGATÓRIO PASSAR O ID
                symbol=s.symbol,
                name=s.name,
                sector=s.sector,
                price=s.price,
                last_updated=s.last_updated
            )
            for s in db_stocks
        ]