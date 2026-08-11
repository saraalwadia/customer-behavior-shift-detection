from fastapi import FastAPI

from api.model_loader import load_model
from api.schemas import PredictionRequest, PredictionResponse


app = FastAPI(
    title="Customer Behavior Shift Detection API",
    description="REST API for detecting customer behavior shifts using XGBoost.",
    version="1.0.0",
)


# Load the versioned model
model = load_model()

MODEL_NAME = "XGBoost"
MODEL_VERSION = "v1"
THRESHOLD = 0.30

MODEL_FEATURES = [
    "historical_active_months",
    "historical_transactions",
    "historical_spending",
    "previous_transaction_count",
    "previous_total_quantity",
    "previous_total_spending",
    "previous_average_transaction_value",
    "previous_unique_products",
    "months_since_previous",
]


@app.get("/health")
def health():
    """Check whether the API and model are available."""
    return {
        "status": "healthy",
        "model": MODEL_NAME,
        "version": MODEL_VERSION,
    }


@app.get("/metadata")
def metadata():
    """Return metadata about the deployed model."""
    return {
        "model": MODEL_NAME,
        "version": MODEL_VERSION,
        "threshold": THRESHOLD,
        "features": MODEL_FEATURES,
    }


@app.get("/versions")
def versions():
    """Return the available model versions."""
    return {
        "current_version": MODEL_VERSION,
        "available_versions": [MODEL_VERSION],
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    """Generate a behavior-shift prediction for a customer."""
    
    input_data = [[
        request.historical_active_months,
        request.historical_transactions,
        request.historical_spending,
        request.previous_transaction_count,
        request.previous_total_quantity,
        request.previous_total_spending,
        request.previous_average_transaction_value,
        request.previous_unique_products,
        request.months_since_previous,
    ]]

    probability = float(model.predict_proba(input_data)[0][1])

    prediction = int(probability >= THRESHOLD)

    return PredictionResponse(
        prediction=prediction,
        probability=probability,
        threshold=THRESHOLD,
        model_version=MODEL_VERSION,
    )
