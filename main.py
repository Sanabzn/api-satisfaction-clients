from fastapi import FastAPI
from pydantic import BaseModel
from google.cloud import bigquery
from datetime import datetime
import uuid

app = FastAPI(title="API Satisfaction Clients")

bq_client = bigquery.Client()

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
    bq_client.insert_rows_json(table_id, rows_to_insert)

@app.get("/")
def root():
    return {"message": "API Satisfaction Clients OK"}

@app.post("/predict")
def predict_sentiment(avis: Avis):
    text_lower = avis.text.lower()

    if "lent" in text_lower or "nul" in text_lower or "mauvais" in text_lower:
        sentiment = "Negative"
        score = 0.15
    else:
        sentiment = "Positive"
        score = 0.85

    save_prediction(avis.text, sentiment, score)

    return {
        "sentiment": sentiment,
        "score": score,
        "text": avis.text
    }
