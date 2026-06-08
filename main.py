from fastapi import FastAPI
from pydantic import BaseModel
from google.cloud import bigquery
from datetime import datetime
import uuid
import mlflow.sklearn
import numpy as np

app = FastAPI(title="API Satisfaction Clients")

bq_client = bigquery.Client()

MODEL_PATH = "model"
model = mlflow.sklearn.load_model(MODEL_PATH)


class Avis(BaseModel):
    text: str


def save_prediction(text: str, sentiment: str, score: float):
    table_id = "satisfaction-clients-478614.dataset_gold_modeling.predictions_sentiment"

    rows_to_insert = [
        {
            "id": str(uuid.uuid4()),
            "text": text,
            "sentiment": sentiment,
            "score": score,
            "prediction_date": datetime.utcnow().isoformat()
        }
    ]

    errors = bq_client.insert_rows_json(table_id, rows_to_insert)

    if errors:
        print("Erreur insertion BigQuery :", errors)


def sigmoid(x: float) -> float:
    return 1 / (1 + np.exp(-x))


def get_model_score(text: str) -> float:
    decision = model.decision_function([text])

    if isinstance(decision, np.ndarray):
        decision_value = float(np.max(np.abs(decision)))
    else:
        decision_value = float(abs(decision))

    score = sigmoid(decision_value)
    return round(float(score), 4)


@app.get("/")
def root():
    return {"message": "API Satisfaction Clients OK - modèle SVM intégré"}


@app.post("/predict")
def predict_sentiment(avis: Avis):
    prediction = model.predict([avis.text])[0]
    sentiment = str(prediction)

    score = get_model_score(avis.text)

    save_prediction(avis.text, sentiment, score)

    return {
        "sentiment": sentiment,
        "score": score,
        "text": avis.text
    }
