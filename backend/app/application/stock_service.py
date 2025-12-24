from app.domain.entities.stock import Stock
from app.domain.ports.stock_repository import StockRepository

class StockService:
    def __init__(self, repository: StockRepository):
        # Injeção de Dependência: O serviço recebe o repositório, ele não o cria.
        self.repository = repository

    def create_stock(self, symbol: str, name: str, sector: str, initial_price: float) -> Stock:
        # 1. Instancia a Entidade (aplica regras de domínio internas, como preço não negativo)
        new_stock = Stock(symbol=symbol, name=name, sector=sector, price=initial_price)
        
        # 2. Verifica se já existe (regra de negócio do caso de uso)
        existing_stock = self.repository.get_by_symbol(symbol)
        if existing_stock:
            raise ValueError(f"A ação {symbol} já está cadastrada.")

        # 3. Persiste usando o Porto (sem saber banco de dados é)
        return self.repository.save(new_stock)