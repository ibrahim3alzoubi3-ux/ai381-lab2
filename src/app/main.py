"""Lab 1 FastAPI skeleton: serves the model you saved from the notebook.

Run it by hand (this is Round 1 of the race):
    uvicorn app.main:app --port 8000
Then send predictions with curl (see sample_request.json).
"""
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field
import json
from pathlib import Path
MODEL_PATH = "model.joblib"   # where the notebook saves the model (yes, hard-coded on purpose)
FEATURES = ["tenure_months", "monthly_charges", "contract", "internet_service", "support_calls"]
class Customer(BaseModel):
    tenure_months: int = Field(ge=0)
    monthly_charges: float = Field(ge=0)
    contract: str
    internet_service: str
    support_calls: int = Field(ge=0)
app = FastAPI(title="AI381 Lab 1 churn API")
model = joblib.load(MODEL_PATH)


@app.get("/health")
def health():
    metadata_path = Path("metadata.json")

    if metadata_path.is_file():
        with metadata_path.open(encoding="utf-8") as f:
            metadata = json.load(f)

        return {
            "status": "ok",
            "model_version": str(metadata.get("mlflow_model_version", "unknown")),
            "model": metadata.get("model", "unknown"),
            "mlflow_run_id": metadata.get("mlflow_run_id", "unknown"),
        }

    return {
        "status": "ok",
        "model_version": "legacy",
    }

@app.post("/predict")
def predict(customer: Customer):
    X = pd.DataFrame([customer.model_dump()])[FEATURES]
    p = float(model.predict_proba(X)[0, 1])
    return {"churn_probability": round(p, 3)}
