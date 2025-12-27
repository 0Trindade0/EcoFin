import yfinance as yf
import pandas as pd
from typing import Optional
from app.domain.ports.market_data_port import MarketDataPort

class YahooFinanceAdapter(MarketDataPort):
    def get_historical_data(self, symbol: str, days: int = 30) -> Optional[pd.DataFrame]:
        try:
            print(f"🌍 BUSCANDO HISTÓRICO NO YAHOO: {symbol} ({days} dias)")
            
            # Baixa o histórico. 'period' define o range (ex: 1mo, 1y)
            # Vamos simplificar e pegar '1mo' (um mês) para cobrir os 30 dias
            ticker = yf.Ticker(symbol)
            history = ticker.history(period="1mo")
            
            if history.empty:
                return None
                
            return history
        except Exception as e:
            print(f"⚠️ Erro ao buscar no Yahoo Finance: {e}")
            return None