import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_predict_positive(monkeypatch):
    monkeypatch.setattr(main, "save_prediction", lambda text, sentiment, score: None)

    response = client.post(
        "/predict",
        json={"text": "service excellent"}
    )

    assert response.status_code == 200

    data = response.json()
    assert "sentiment" in data
    assert "score" in data
    assert "text" in data


def test_predict_negative(monkeypatch):
    monkeypatch.setattr(main, "save_prediction", lambda text, sentiment, score: None)

    response = client.post(
        "/predict",
        json={"text": "service très mauvais"}
    )

    assert response.status_code == 200

    data = response.json()
    assert "sentiment" in data
    assert "score" in data
    assert "text" in data
