import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Garante que o corpus de stopwords do NLTK esteja disponível
nltk.download('stopwords')

# Carrega a lista de stopwords em português
stop_words_portugues = stopwords.words('portuguese')

ask_phrases = [
    "Qual é o valor do produto X?",
    "Quanto custa o plano mensal?",
    "Como funciona o pagamento?",
    "Qual o prazo de entrega?",
    "Vocês aceitam cartão de crédito?",
]

problem_phrases = [
    "Estou com problemas para realizar o pagamento",
    "Não consigo finalizar a compra",
    "O site está com erro",
    "O pagamento foi recusado",
    "Meu pedido não foi processado"
]

request_phrases = [
    "Gostaria de um cupom de desconto",
    "Gostaria de um cupom de desconto",
]

phrases = [
    *ask_phrases,
    *problem_phrases,
    *request_phrases,
]

labels = [
    *["pergunta"] * len(ask_phrases),
    *["problema"] * len(problem_phrases),
    *["solicitação"] * len(request_phrases),
]

# Opcional: Você pode inspecionar as primeiras palavras da lista
# print(stop_words_portugues[:20])

# Inicializa o TfidfVectorizer com a lista de stop words
# É uma boa prática converter a lista para um conjunto (set) para melhor performance na verificação
# e também usar strip_accents='unicode' e lowercase=True para um pré-processamento básico.
vectorizer = TfidfVectorizer(
    stop_words=stop_words_portugues,
    strip_accents='unicode',
    lowercase=True
)

X = vectorizer.fit_transform(phrases)

model = MultinomialNB()

model.fit(X, labels)

# Classifica uma mensagem e retorna a categoria
def classify_message(message):
    msg = vectorizer.transform([message])
    probs = model.predict_proba(msg)[0]

    classes = model.classes_
    result = dict(zip(classes, probs))

    classification = max(result, key=result.get)
    probability = result[classification]

    return classification, probability