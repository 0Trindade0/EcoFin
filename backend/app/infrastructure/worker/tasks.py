# backend/app/infrastructure/worker/tasks.py
import random
from celery import shared_task
from app.infrastructure.db.config import SessionLocal
from app.infrastructure.db.repositories.stock_repository_impl import PostgresStockRepository
from app.application.stock_service import StockService

@shared_task(name="update_stock_price_task")
def update_stock_price_task(symbol: str):
    """
    Tarefa que roda em background.
    Ela simula buscar um preço novo e atualizar no banco.
    """
    print(f"🔄 WORKER: Iniciando atualização para {symbol}...")

    # 1. Configura o ambiente (Banco de dados)
    # Como o Celery roda em outro processo, precisamos criar uma nova sessão de banco
    db = SessionLocal()
    
    try:
        # 2. Monta a Arquitetura (Repo + Service)
        repo = PostgresStockRepository(db)
        service = StockService(repo)
        
        # 3. Simula buscar preço externo (Aqui entraria o Yahoo Finance depois)
        # Vamos gerar um preço aleatório entre 20 e 50
        fake_new_price = round(random.uniform(20.0, 50.0), 2)
        
        # 4. Busca a ação e atualiza
        # Nota: Precisaríamos de um método update no service, vamos improvisar usando a lógica do repository direto ou adaptar o service depois.
        # Por agora, vamos buscar e salvar de novo com preço novo.
        stock = repo.get_by_symbol(symbol)
        if stock:
            stock.update_price(fake_new_price)
            repo.save(stock)
            print(f"✅ WORKER: {symbol} atualizado para R$ {fake_new_price}")
        else:
            print(f"❌ WORKER: Ação {symbol} não encontrada.")
            
    except Exception as e:
        print(f"🔥 ERRO NO WORKER: {e}")
    finally:
        db.close()