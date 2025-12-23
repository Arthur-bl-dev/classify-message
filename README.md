# Classificador de Mensagens

API REST desenvolvida com FastAPI para classificar mensagens em português em diferentes categorias usando Machine Learning (Naive Bayes).

## 📋 Sobre o Projeto

Este projeto classifica mensagens de texto em três categorias principais:
- **Pergunta**: Mensagens que fazem perguntas sobre produtos, serviços ou informações
- **Problema**: Mensagens relacionadas a problemas técnicos ou dificuldades
- **Solicitação**: Mensagens que solicitam algo, como cupons de desconto

O modelo utiliza:
- **NLTK** para processamento de linguagem natural (stopwords em português)
- **scikit-learn** com Naive Bayes Multinomial para classificação
- **TF-IDF** para vetorização de texto

## 🚀 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip

### Passos

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
  "message": "Qual é o valor do produto X?"
}
```

#### Response
```json
{
  "classification": "pergunta",
  "probability": 0.95
}
```

### Exemplos de Uso

#### Usando cURL
```bash
curl -X POST "http://localhost:8000/classify" \
     -H "Content-Type: application/json" \
     -d '{"message": "Estou com problemas para realizar o pagamento"}'
```

#### Usando Python
```python
import requests

response = requests.post(
    "http://localhost:8000/classify",
    json={"message": "Gostaria de um cupom de desconto"}
)
print(response.json())
```

### Documentação Interativa

Quando o servidor estiver rodando, acesse:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🛠️ Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido para APIs
- **scikit-learn**: Biblioteca de Machine Learning
- **NLTK**: Biblioteca de processamento de linguagem natural
- **Uvicorn**: Servidor ASGI de alta performance

## 📁 Estrutura do Projeto

```
classify-message/
├── app/
│   ├── main.py          # Aplicação FastAPI e rotas
│   └── model.py         # Modelo de classificação e lógica ML
├── requirements.txt     # Dependências do projeto
├── makefile            # Comandos úteis
└── README.md           # Este arquivo
```

## 🔧 Comandos Disponíveis

- `make install`: Instala as dependências do projeto
- `make run`: Inicia o servidor de desenvolvimento com reload automático
- `make test`: Executa os testes (se configurados)

## 📝 Notas

- O modelo é treinado com um conjunto limitado de frases de exemplo
- Para melhorar a precisão, considere expandir o dataset de treinamento
- A primeira execução pode demorar um pouco devido ao download do corpus de stopwords do NLTK