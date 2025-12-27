# frontend/Dockerfile
FROM node:20-alpine

WORKDIR /app

# Copia os arquivos de dependências
COPY package*.json ./

# Instala as dependências
RUN npm install

# Copia o resto do código
COPY . .

# Expõe a porta do Next.js
EXPOSE 3000

# Comando de desenvolvimento (com Hot Reload)
CMD ["npm", "run", "dev"]