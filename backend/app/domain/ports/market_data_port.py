from abc import ABC, abstractmethod
from typing import Optional
import pandas as pd # Precisamos adicionar o pandas na interface pois o retorno será um DataFrame

class MarketDataPort(ABC):
    @abstractmethod
    def get_historical_data(self, symbol: str, days: int = 30) -> Optional[pd.DataFrame]:
        """Retorna um DataFrame do Pandas com o histórico de preços."""
        pass