from fastapi import FastAPI

from api.model_loader import load_model
from api.schemas import PredictionRequest, PredictionResponse


app = FastAPI(
    title="Customer Behavior Shift Detection API",
    description="REST API for detecting customer behavior shifts using XGBoost.",
    version="1.0.0",
)


# Load the versioned final model once when the API starts
model = load_model()


MODEL_NAME = "XGBoost"
MODEL_VERSION = "v1"
THRESHOLD = 0.30


# Exact feature order used during model training
MODEL_FEATURES = [
    "spend",
    "totalQuantity",
    "unique_products",
    "active_days",
    "line_items",
    "avargeOrderValue",
    "items_per_order",
    "window_days",
    "prev_orders",
    "prev_spend",
    "prev_totalQuantity",
    "prev_avargeOrderValue",
    "prev_unique_products",
    "prev_active_days",
    "prev_items_per_order",
    "orders_change_pct",
    "spend_change_pct",
    "totalQuantity_change_pct",
    "avargeOrderValue_change_pct",
    "unique_products_change_pct",
    "active_days_change_pct",
    "items_per_order_change_pct",
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
        "n_features": len(MODEL_FEATURES),
        "features": MODEL_FEATURES,
    }


@app.get("/versions")
def versions():
    """Return the available model versions."""
    return {
        "current_version": MODEL_VERSION,
        "available_versions": [MODEL_VERSION],
    }


@app.post("/api/v1/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    """Generate a behavior-shift prediction for a customer."""

    input_data = [[
        request.spend,
        request.totalQuantity,
        request.unique_products,
        request.active_days,
        request.line_items,
        request.avargeOrderValue,
        request.items_per_order,
        request.window_days,
        request.prev_orders,
        request.prev_spend,
        request.prev_totalQuantity,
        request.prev_avargeOrderValue,
        request.prev_unique_products,
        request.prev_active_days,
        request.prev_items_per_order,
        request.orders_change_pct,
        request.spend_change_pct,
        request.totalQuantity_change_pct,
        request.avargeOrderValue_change_pct,
        request.unique_products_change_pct,
        request.active_days_change_pct,
        request.items_per_order_change_pct,
    ]]

    probability = float(model.predict_proba(input_data)[0][1])

    prediction = int(probability >= THRESHOLD)

    return PredictionResponse(
        prediction=prediction,
        probability=probability,
        threshold=THRESHOLD,
        model_version=MODEL_VERSION,
    )