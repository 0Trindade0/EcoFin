from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Stock:
    def __init__(self, symbol: str, name: str, price: float, sector: str = None, last_updated=None, id: int = None, change_percent: float = 0.0):
        self.id = id  # <--- ADICIONADO: O campo ID
        self.symbol = symbol
        self.name = name
        self.price = price
        self.sector = sector
        self.last_updated = last_updated
        self.change_percent = change_percent
    
    def update_price(self, new_price: float):
        """
        Regra de Negócio: O preço não pode ser negativo.
        Isso é uma regra de domínio, não de banco de dados.
        """
        if new_price < 0:
            raise ValueError("O preço da ação não pode ser negativo.")
        
        self.price = new_price
        self.last_updated = datetime.now()

    def is_renewable(self) -> bool:
        """Verifica se a ação é do setor de renováveis."""
        return self.sector == "ENERGY_RENEWABLE"