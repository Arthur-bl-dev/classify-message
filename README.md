# Message Classifier

REST API developed with FastAPI to classify messages in Portuguese into different categories using Machine Learning (Naive Bayes).

## 📋 About the Project

This project classifies text messages into three main categories:
- **Question**: Messages that ask questions about products, services, or information
- **Problem**: Messages related to technical issues or difficulties
- **Request**: Messages that request something, such as discount coupons

The model uses:
- **NLTK** for natural language processing (Portuguese stopwords)
- **scikit-learn** with Multinomial Naive Bayes for classification
- **TF-IDF** for text vectorization

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip

### Steps

1. Clone the repository (or navigate to the project directory)

2. Install dependencies:
```bash
make install
```
or
```bash
pip install -r requirements.txt
```

3. Start the server:
```bash
make run
```

The server will be available at `http://localhost:8000`

## 📖 API Usage

### Classification Endpoint

**POST** `/classify`

Classifies a message and returns the most likely category along with the probability.

#### Request Body
```json
{
  "message": "What is the price of product X?"
}
```

#### Response
```json
{
  "classification": "pergunta",
  "probability": 0.95
}
```

### Usage Examples

#### Using cURL
```bash
curl -X POST "http://localhost:8000/classify" \
     -H "Content-Type: application/json" \
     -d '{"message": "I am having problems processing the payment"}'
```

#### Using Python
```python
import requests

response = requests.post(
    "http://localhost:8000/classify",
    json={"message": "I would like a discount coupon"}
)
print(response.json())
```

### Interactive Documentation

When the server is running, access:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🛠️ Technologies Used

- **FastAPI**: Modern and fast web framework for APIs
- **scikit-learn**: Machine Learning library
- **NLTK**: Natural language processing library
- **Uvicorn**: High-performance ASGI server

## 📁 Project Structure

```
classify-message/
├── app/
│   ├── main.py          # FastAPI application and routes
│   └── model.py         # Classification model and ML logic
├── requirements.txt     # Project dependencies
├── makefile            # Useful commands
└── README.md           # This file
```

## 🔧 Available Commands

- `make install`: Installs project dependencies
- `make run`: Starts the development server with automatic reload
- `make test`: Runs tests (if configured)

## 📝 Notes

- The model is trained with a limited set of example phrases
- To improve accuracy, consider expanding the training dataset
- The first run may take a while due to downloading the NLTK stopwords corpus
