from abc import ABC, abstractmethod
import pandas as pd

class IndicatorStrategy(ABC):
    """
    Interface Strategy: Define como um indicador técnico é calculado.
    """
    @abstractmethod
    def calculate(self, data: pd.DataFrame) -> float:
        pass

class SimpleMovingAverageStrategy(IndicatorStrategy):
    def __init__(self, window: int = 5):
        self.window = window

    def calculate(self, data: pd.DataFrame) -> float:
        """
        Recebe o DataFrame do Pandas e calcula a média dos últimos X fechamentos.
        """
        if data is None or data.empty:
            return 0.0
            
        # Pega a coluna 'Close' (Fechamento)
        closes = data['Close']
        
        # Calcula a média dos últimos 'self.window' dias
        sma = closes.tail(self.window).mean()
        
        return round(float(sma), 2)