from pydantic import BaseModel


class PredictionRequest(BaseModel):
    historical_active_months: float
    historical_transactions: float
    historical_spending: float
    previous_transaction_count: float
    previous_total_quantity: float
    previous_total_spending: float
    previous_average_transaction_value: float
    previous_unique_products: float
    months_since_previous: float


class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    threshold: float
    model_version: str