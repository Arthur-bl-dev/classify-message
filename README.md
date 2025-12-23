# Message Classifier - Multi-Tenant

REST API desenvolvida com FastAPI para classificação de mensagens em múltiplos idiomas usando Machine Learning (Naive Bayes) com suporte multi-tenant.

## 📋 Sobre o Projeto

Este projeto classifica mensagens de texto em diferentes categorias com suporte multi-tenant:
- Cada tenant possui suas próprias **phrases**, **labels** e **idioma**
- Cada tenant tem seu próprio modelo de ML treinado
- Suporte a múltiplos idiomas (português, inglês, espanhol, francês)

O modelo usa:
- **NLTK** para processamento de linguagem natural (stopwords por idioma)
- **scikit-learn** com Multinomial Naive Bayes para classificação
- **TF-IDF** para vetorização de texto

## 🚀 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip
- Docker e Docker Compose (opcional, para usar Docker)

### Opção 1: Usando Docker (Recomendado)

1. Clone o repositório (ou navegue até o diretório do projeto)

2. Construa e inicie o container:
```bash
docker-compose up --build
```

Ou apenas inicie (se já construiu antes):
```bash
docker-compose up
```

3. O servidor estará disponível em `http://localhost:8000`

**Comandos úteis:**
```bash
# Construir a imagem
docker build -t classify-message .

# Executar o container
docker run -p 8000:8000 classify-message

# Parar o container
docker-compose down
```

### Opção 2: Instalação Local

1. Clone o repositório (ou navegue até o diretório do projeto)

2. Instale as dependências:
```bash
make install
```
ou
```bash
pip install -r requirements.txt
```

3. Inicie o servidor:
```bash
make run
```

O servidor estará disponível em `http://localhost:8000`

## 📖 Uso da API

### Endpoint de Classificação

**POST** `/classify`

Classifica uma mensagem e retorna a categoria mais provável junto com a probabilidade.

#### Request Body
```json
{
  "message": "Qual é o valor do produto X?",
  "tenant_id": "default"
}
```

#### Response
```json
{
  "classification": "pergunta",
  "probability": 0.95,
  "tenant_id": "default"
}
```

### Endpoints de Gerenciamento de Tenants

#### Criar Tenant
**POST** `/tenants`
```json
{
  "tenant_id": "empresa_abc",
  "language": "english",
  "phrases": ["What is the price?", "I have a problem"],
  "labels": ["question", "problem"]
}
```

#### Listar Tenants
**GET** `/tenants`

#### Obter Tenant
**GET** `/tenants/{tenant_id}`

#### Atualizar Tenant
**PUT** `/tenants/{tenant_id}`
```json
{
  "language": "portuguese",
  "phrases": ["Qual o preço?", "Tenho um problema"],
  "labels": ["pergunta", "problema"]
}
```

#### Deletar Tenant
**DELETE** `/tenants/{tenant_id}`

### Exemplos de Uso

#### Usando cURL
```bash
# Classificar mensagem
curl -X POST "http://localhost:8000/classify" \
     -H "Content-Type: application/json" \
     -d '{"message": "Estou com problemas para realizar o pagamento", "tenant_id": "default"}'

# Criar um novo tenant
curl -X POST "http://localhost:8000/tenants" \
     -H "Content-Type: application/json" \
     -d '{
       "tenant_id": "empresa_xyz",
       "language": "english",
       "phrases": ["What is the price?", "I have a problem"],
       "labels": ["question", "problem"]
     }'
```

#### Usando Python
```python
import requests

# Classificar mensagem
response = requests.post(
    "http://localhost:8000/classify",
    json={
        "message": "Gostaria de um cupom de desconto",
        "tenant_id": "default"
    }
)
print(response.json())

# Criar um novo tenant
response = requests.post(
    "http://localhost:8000/tenants",
    json={
        "tenant_id": "empresa_abc",
        "language": "portuguese",
        "phrases": ["Qual o preço?", "Tenho um problema"],
        "labels": ["pergunta", "problema"]
    }
)
print(response.json())
```

### Documentação Interativa

Quando o servidor estiver rodando, acesse:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

## 🛠️ Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido para APIs
- **scikit-learn**: Biblioteca de Machine Learning
- **NLTK**: Biblioteca de processamento de linguagem natural
- **Uvicorn**: Servidor ASGI de alta performance
- **Docker**: Containerização da aplicação

## 📁 Estrutura do Projeto

```
classify-message/
├── app/
│   ├── __init__.py         # Inicialização do pacote
│   ├── main.py             # Aplicação FastAPI e rotas
│   ├── model.py            # Modelo de classificação e lógica ML
│   └── tenant_manager.py   # Gerenciador de tenants
├── requirements.txt        # Dependências do projeto
├── Dockerfile              # Configuração Docker
├── docker-compose.yml      # Configuração Docker Compose
├── .dockerignore           # Arquivos ignorados no Docker
├── makefile                # Comandos úteis
└── README.md               # Este arquivo
```

## 🔧 Comandos Disponíveis

### Comandos Make
- `make install`: Instala as dependências do projeto
- `make run`: Inicia o servidor de desenvolvimento com reload automático
- `make test`: Executa os testes (se configurado)

### Comandos Docker
- `docker-compose up --build`: Constrói e inicia o container
- `docker-compose up`: Inicia o container
- `docker-compose down`: Para o container
- `docker build -t classify-message .`: Constrói a imagem Docker
- `docker run -p 8000:8000 classify-message`: Executa o container

## 📝 Notas

- O modelo é treinado com um conjunto limitado de frases de exemplo
- Para melhorar a precisão, considere expandir o dataset de treinamento
- A primeira execução pode demorar devido ao download do corpus de stopwords do NLTK
- Cada tenant possui seu próprio modelo treinado isoladamente
- Os dados dos tenants são armazenados em memória (perdidos ao reiniciar)
