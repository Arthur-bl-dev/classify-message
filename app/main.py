from fastapi import FastAPI
from pydantic import BaseModel
from .model import classify_message

app = FastAPI(title="Classify Message", description="Classify messages into categories")

class MessageRequest(BaseModel):
    message: str


class ClassificationResponse(BaseModel):
    classification: str
    probability: float


@app.post("/classify", response_model=ClassificationResponse)
def classify(data: MessageRequest):
    classification, probability = classify_message(data.message)

    return {
        "classification": classification,
        "probability": round(probability, 2)
    }