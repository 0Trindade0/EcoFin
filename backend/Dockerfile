# Usa uma versão leve do Python
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala dependências do sistema necessárias para o PostgreSQL e Pandas
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala as dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código (faremos isso depois)
COPY . .

# Comando para rodar a aplicação (ajustaremos conforme avançarmos)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]