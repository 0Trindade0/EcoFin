# 📈 EcoFin: Real-Time Financial Dashboard & Automated Data Pipeline

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat-square&logo=fastapi)
![Next.js](https://img.shields.io/badge/Next.js-16-black?style=flat-square&logo=next.js)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=flat-square&logo=docker)
![Celery](https://img.shields.io/badge/Celery-Distributed_Task_Queue-37814A?style=flat-square&logo=celery)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat-square&logo=postgresql)

## 🔬 Executive Summary (R&D Perspective)

EcoFin is an end-to-end, event-driven financial monitoring system built with **Clean Architecture** principles. It was designed to solve the common bottlenecks of massive financial data ingestion by strictly decoupling the client-facing API from the background data processing workers.

Instead of blocking the main API thread to fetch third-party data, EcoFin utilizes **Celery and Redis** to orchestrate asynchronous pipelines. A dedicated **Celery Beat** service acts as a cron-scheduler, autonomously dispatching workers to ingest, calculate, and persist market variations (e.g., Yahoo Finance data) at high frequencies.

### Key Architectural Highlights:
* **Clean Architecture:** Strict separation between Domain Entities, Use Cases, and Infrastructure/Adapters.
* **Asynchronous Data Ingestion:** Background workers handle API rate limits, network latency, and complex calculations (percentage variations) without impacting the User Experience.
* **Environment Parity:** Full containerization ensuring the system runs identically across development, staging, and production environments.

---

## 🏗️ System Architecture

The ecosystem is composed of strictly isolated, containerized services:

1. **Frontend (`Next.js`):** A reactive dashboard providing real-time visual feedback (prices, red/green variation indicators).
2. **API (`FastAPI`):** High-performance, asynchronous REST API serving as the entry point for clients. Uses `Pydantic` for strict data validation.
3. **Database (`PostgreSQL`):** Relational persistence layer accessed via the Repository Pattern (`SQLAlchemy`).
4. **Message Broker (`Redis`):** In-memory datastore facilitating communication between the API and Workers.
5. **Worker (`Celery`):** Executes heavy lifting: fetches third-party data, calculates variations, and writes to the DB.
6. **Scheduler (`Celery Beat`):** The chronometer that triggers automated updates (e.g., every 30 seconds).

---

## 🚀 Quick Start Guide

EcoFin is fully containerized. You do not need to install Python, Node.js, or PostgreSQL on your local machine.

### Prerequisites
* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)

### 1. Clone the repository
```bash
git clone [https://github.com/your-username/ecofin.git](https://github.com/your-username/ecofin.git)
cd ecofin
2. Spin up the environment
Use Docker Compose to build and start all 6 microservices simultaneously.

Bash
docker-compose up --build
Note: The initial build might take a few minutes as it downloads the base images and installs dependencies.

3. Access the Services
Once the logs stabilize (look for Uvicorn running on http://0.0.0.0:8000), the services are available at:

Frontend Dashboard: http://localhost:3000

API Interactive Docs (Swagger): http://localhost:8000/docs

🛠️ Usage Example: Adding a new Stock
Since the database starts empty, you can seed it directly through the interactive API documentation.

Open http://localhost:8000/docs.

Navigate to the POST /stocks/ endpoint and click "Try it out".

Insert a JSON payload with a valid Yahoo Finance ticker (e.g., WEGE3, AAPL, PETR4):

JSON
{
  "symbol": "WEGE3",
  "name": "WEG S.A.",
  "sector": "Industrial",
  "price": 0.0 
}
Click Execute.

Go to the Frontend Dashboard (http://localhost:3000) and click Update.

Watch the Automation: Within 30 seconds, the Celery Beat scheduler will dispatch a task to the Worker. The Worker will fetch the real-time price and calculate the variation. Click Update again on the dashboard to see the live data populate automatically!

🔮 Future Roadmap (R&D Enhancements)
Implement WebSockets for true push-based UI updates (eliminating the manual "Update" button).

Integrate an Adapter Pattern for multiple data providers (e.g., Alpha Vantage, B3 APIs) as fallbacks.

Create a microservice for Time-Series Analysis (e.g., Moving Averages, RSI) using Pandas.
