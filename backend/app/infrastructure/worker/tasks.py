from app.infrastructure.worker.celery_app import celery_app
from app.infrastructure.db.config import SessionLocal
from app.infrastructure.db.repositories.stock_repository_impl import PostgresStockRepository
from app.infrastructure.adapters.yfinance_adapter import YahooFinanceAdapter
# Importa a estratégia
from app.domain.strategies.indicator_strategy import SimpleMovingAverageStrategy

@celery_app.task(name="update_stock_price_task")
def update_stock_price_task(symbol: str):
    print(f"🔄 WORKER: Analisando ativo {symbol}...")
    
    db = SessionLocal()
    try:
        repo = PostgresStockRepository(db)
        market_data = YahooFinanceAdapter()
        
        # 1. Busca Histórico (30 dias)
        history_df = market_data.get_historical_data(symbol)
        
        if history_df is None or history_df.empty:
            print(f"❌ WORKER: Sem dados para {symbol}")
            return

        # 2. Pega o preço atual (o último fechamento disponível)
        current_price = round(float(history_df['Close'].iloc[-1]), 2)

        # 3. Aplica Strategy: Calcula Média Móvel de 5 dias
        strategy = SimpleMovingAverageStrategy(window=5)
        sma_value = strategy.calculate(history_df)
        
        # 4. Atualiza no banco
        stock = repo.get_by_symbol(symbol)
        if stock:
            stock.update_price(current_price)
            repo.save(stock)
            
            # AQUI ESTÁ A MÁGICA DO PANDAS SENDO LOGADA
            print(f"✅ ANÁLISE COMPLETA {symbol}:")
            print(f"   💰 Preço Atual: R$ {current_price}")
            print(f"   📈 Média Móvel (5d): R$ {sma_value}")
            
            if current_price > sma_value:
                print("   🚀 SINAL: TENDÊNCIA DE ALTA (Preço acima da média)")
            else:
                print("   🔻 SINAL: TENDÊNCIA DE BAIXA (Preço abaixo da média)")
                
        else:
            print(f"⚠️ WORKER: Ativo {symbol} não encontrado no banco.")
            
    except Exception as e:
        print(f"🔥 ERRO NO WORKER: {e}")
    finally:
        db.close()