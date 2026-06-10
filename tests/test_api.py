import requests

API_URL = "https://api-satisfaction-913270433936.europe-west1.run.app"


def test_root_endpoint():
    response = requests.get(API_URL)

    assert response.status_code == 200
    assert "message" in response.json()


def test_predict_positive():
    response = requests.post(
        f"{API_URL}/predict",
        json={"text": "service excellent"}
    )

    assert response.status_code == 200

    data = response.json()

    assert "sentiment" in data
    assert "score" in data
    assert "text" in data


def test_predict_negative():
    response = requests.post(
        f"{API_URL}/predict",
        json={"text": "service très mauvais"}
    )

    assert response.status_code == 200

    data = response.json()

    assert "sentiment" in data
    assert "score" in data
    assert "text" in data
