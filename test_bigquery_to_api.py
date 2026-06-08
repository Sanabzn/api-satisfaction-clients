from google.cloud import bigquery
import requests

client = bigquery.Client()

API_URL = "https://api-satisfaction-913270433936.europe-west1.run.app/predict"

query = """
SELECT txt_reponse
FROM `satisfaction-clients-478614.dataset_gold_modeling.dataset_gold`
WHERE txt_reponse IS NOT NULL
LIMIT 10
"""

rows = client.query(query).result()

for row in rows:
    text = row.txt_reponse

    response = requests.post(
        API_URL,
        json={"text": text}
    )

    print("Avis :", text[:100])
    print("Statut :", response.status_code)
    print("Réponse :", response.text)
    print("-" * 50)
