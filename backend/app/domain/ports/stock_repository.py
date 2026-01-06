from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.stock import Stock

class StockRepository(ABC):
    """
    Interface (Contrato) que define como armazenar e buscar ações.
    O Domínio NÃO sabe se isso vai ser salvo no Postgres, num arquivo TXT ou na memória.
    """

    @abstractmethod
    def save(self, stock: Stock) -> Stock:
        """Salva ou atualiza uma ação."""
        pass

    @abstractmethod
    def get_by_symbol(self, symbol: str) -> Optional[Stock]:
        """Busca uma ação pelo símbolo (ticker)."""
        pass

    @abstractmethod
    def find_all(self) -> list[Stock]:
        """Retorna todas as ações cadastradas."""
        pass