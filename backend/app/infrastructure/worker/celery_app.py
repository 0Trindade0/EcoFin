# backend/app/infrastructure/worker/celery_app.py
import os
from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# 1. Remova o include daqui para evitar o ciclo imediato
celery_app = Celery(
    "ecofin_worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

# 2. Configure as importações e outras configs aqui
celery_app.conf.update(
    # Aqui dizemos ao Worker quais módulos ele deve carregar ao iniciar
    imports=['app.infrastructure.worker.tasks'],
    
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="America/Sao_Paulo",
    enable_utc=True,
)