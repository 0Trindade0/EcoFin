# EcoFin

Dashboard para acompanhar cotações de ativos. O projeto reúne uma interface Next.js, uma API FastAPI, PostgreSQL e tarefas em segundo plano com Celery e Redis.

## Requisitos

- Docker Desktop com Docker Compose

## Iniciar o projeto

Na raiz do repositório, rode:

```bash
docker compose up --build
```

Serviços disponíveis:

- Dashboard: http://localhost:3000
- API e documentação interativa: http://localhost:8000/docs
- PostgreSQL: porta 5432
- Redis: porta 6379

O Celery Beat agenda a consulta dos ativos a cada 15 minutos. Também é possível solicitar uma atualização individual pelo dashboard ou por `POST /stocks/{symbol}/refresh`. A tarefa busca o histórico no Yahoo Finance, atualiza o último preço disponível e grava a variação percentual em relação ao preço anteriormente salvo. A consulta da tarefa fica disponível em `GET /tasks/{task_id}`.

## Cadastrar ativos

Use o botão **Adicionar ativo** no dashboard ou envie uma requisição para `POST /stocks/`:

```json
{
  "symbol": "PETR4.SA",
  "name": "Petrobras PN",
  "sector": "Energia",
  "price": 0
}
```

O preço inicial pode ser zero quando o ativo ainda não tem uma cotação armazenada. A primeira atualização grava o preço; a variação percentual começa a ser calculada a partir de uma cotação anterior maior que zero.

## Componentes

- `frontend/`: aplicação Next.js e interface do dashboard.
- `backend/app/domain/`: entidades, contratos e estratégia de média móvel.
- `backend/app/application/`: serviços da aplicação.
- `backend/app/infrastructure/`: API, integração com Yahoo Finance, persistência PostgreSQL e tarefas Celery.
- `docker-compose.yml`: ambiente local com banco, Redis, API, worker, agendador e dashboard.

Para apontar o frontend a outra API, defina `NEXT_PUBLIC_API_URL` antes da compilação, por exemplo `http://localhost:8000`.
