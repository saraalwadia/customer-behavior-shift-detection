from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["model"] == "XGBoost"
    assert data["version"] == "v1"


def test_metadata():
    response = client.get("/metadata")

    assert response.status_code == 200

    data = response.json()

    assert data["model"] == "XGBoost"
    assert data["version"] == "v1"
    assert data["threshold"] == 0.30
    assert len(data["features"]) == 9


def test_versions():
    response = client.get("/versions")

    assert response.status_code == 200

    data = response.json()

    assert data["current_version"] == "v1"
    assert "v1" in data["available_versions"]


def test_valid_prediction():
    payload = {
        "historical_active_months": 5.0,
        "historical_transactions": 6.0,
        "historical_spending": 3402.39,
        "previous_transaction_count": 1.0,
        "previous_total_quantity": 277.0,
        "previous_total_spending": 584.91,
        "previous_average_transaction_value": 26.586818181818185,
        "previous_unique_products": 22.0,
        "months_since_previous": 2.0,
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["prediction"] in [0, 1]
    assert 0 <= data["probability"] <= 1
    assert data["threshold"] == 0.30
    assert data["model_version"] == "v1"


def test_prediction_missing_feature():
    payload = {
        "historical_active_months": 5.0,
        "historical_transactions": 6.0,
        "historical_spending": 3402.39,
        "previous_transaction_count": 1.0,
        "previous_total_quantity": 277.0,
        "previous_total_spending": 584.91,
        "previous_average_transaction_value": 26.586818181818185,
        "previous_unique_products": 22.0,
        # months_since_previous is intentionally missing
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_prediction_invalid_type():
    payload = {
        "historical_active_months": "five",
        "historical_transactions": 6.0,
        "historical_spending": 3402.39,
        "previous_transaction_count": 1.0,
        "previous_total_quantity": 277.0,
        "previous_total_spending": 584.91,
        "previous_average_transaction_value": 26.586818181818185,
        "previous_unique_products": 22.0,
        "months_since_previous": 2.0,
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 422