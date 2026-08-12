from pydantic import BaseModel


class PredictionRequest(BaseModel):
    spend: float
    totalQuantity: float
    unique_products: float
    active_days: float
    line_items: float
    avargeOrderValue: float
    items_per_order: float
    window_days: float

    prev_orders: float
    prev_spend: float
    prev_totalQuantity: float
    prev_avargeOrderValue: float
    prev_unique_products: float
    prev_active_days: float
    prev_items_per_order: float

    orders_change_pct: float
    spend_change_pct: float
    totalQuantity_change_pct: float
    avargeOrderValue_change_pct: float
    unique_products_change_pct: float
    active_days_change_pct: float
    items_per_order_change_pct: float


class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    threshold: float
    model_version: str