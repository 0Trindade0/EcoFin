from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Stock:
    symbol: str  # Ex: PETR4
    name: str    # Ex: Petrobras PN
    sector: str  # Ex: ENERGY_FOSSIL ou ENERGY_RENEWABLE
    price: float # Preço atual
    last_updated: datetime = field(default_factory=datetime.now)

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