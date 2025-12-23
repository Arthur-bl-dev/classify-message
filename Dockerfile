# Usa Python 3.11 como imagem base
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Define variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instala dependências do sistema (se necessário)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copia o código da aplicação
COPY app/ ./app/

# Baixa os dados do NLTK durante o build (stopwords)
RUN python -c "import nltk; nltk.download('stopwords', quiet=True)"

# Expõe a porta 8000
EXPOSE 8000

# Comando para executar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

