import joblib
from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    
    
def test_predict_valid_customer():
    customer = {
        "tenure_months": 12,
        "monthly_charges": 89.9,
        "contract": "month-to-month",
        "internet_service": "fiber",
        "support_calls": 3
    }

    response = client.post("/predict", json=customer)

    assert response.status_code == 200
    assert "churn_probability" in response.json()

    probability = response.json()["churn_probability"]
    assert 0 <= probability <= 1
    
def test_predict_negative_tenure():
    customer = {
        "tenure_months": -5,
        "monthly_charges": 89.9,
        "contract": "month-to-month",
        "internet_service": "fiber",
        "support_calls": 3
    }

    response = client.post("/predict", json=customer)

    assert response.status_code == 422
    
def test_model_loading():
    model = joblib.load("model.joblib")

    assert model is not None
    assert hasattr(model, "predict_proba")
    
def test_predict_deterministic():
    customer = {
        "tenure_months": 12,
        "monthly_charges": 89.9,
        "contract": "month-to-month",
        "internet_service": "fiber",
        "support_calls": 3
    }

    response1 = client.post("/predict", json=customer)
    response2 = client.post("/predict", json=customer)

    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response1.json() == response2.json()