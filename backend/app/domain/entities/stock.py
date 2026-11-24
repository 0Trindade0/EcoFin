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

        # A variação compara a cotação nova com a última cotação persistida.
        # Sem um preço anterior válido (por exemplo, um ativo cadastrado a R$ 0),
        # não existe uma base para calcular a porcentagem.
        if self.price > 0:
            self.change_percent = round(((new_price - self.price) / self.price) * 100, 2)
        else:
            self.change_percent = 0.0

        self.price = new_price
        self.last_updated = datetime.now()

    def is_renewable(self) -> bool:
        """Verifica se a ação é do setor de renováveis."""
        return self.sector == "ENERGY_RENEWABLE"
