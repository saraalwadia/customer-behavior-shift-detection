import pandas as pd
import numpy as np
import joblib
import requests


# ============================================================
# Configuration
# ============================================================

DATA_PATH = "data/processed/online_retail_II_labeled_30.csv"

MODEL_PATH = "models/xgboost/v1/model.joblib"

API_URL = "http://127.0.0.1:8000/api/v1/predict"

THRESHOLD = 0.30


# ============================================================
# Load Dataset
# ============================================================

df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)


# ============================================================
# Define API Features
# ============================================================

api_features = [
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


print("\nNumber of API features:", len(api_features))

print("\nAPI features:")

for i, feature in enumerate(api_features, start=1):
    print(f"{i:02d}. {feature}")


# ============================================================
# Check API Features Exist in Dataset
# ============================================================

missing_features = [
    feature
    for feature in api_features
    if feature not in df.columns
]

if missing_features:

    print("\nMissing API features:")

    for feature in missing_features:
        print("-", feature)

    raise ValueError(
        "Some API features do not exist in the dataset."
    )

print("\nAll API features exist in the dataset.")


# ============================================================
# Sort Dataset
# ============================================================

df = df.sort_values(
    ["CustomerID", "window_id"]
).reset_index(drop=True)


# ============================================================
# Time-Based Train/Test Split
# ============================================================

split_window = df["window_id"].quantile(0.8)

test_mask = df["window_id"] >= split_window

test_df = df[test_mask].copy()

print("\nSplit window:", split_window)

print("Test rows:", len(test_df))

print(
    "Test window range:",
    test_df["window_id"].min(),
    "to",
    test_df["window_id"].max()
)


# ============================================================
# Get One Real Test Sample
# ============================================================

api_test_sample = test_df[api_features].iloc[0]

print("\nReal test sample:")

print(api_test_sample)


# ============================================================
# Prepare API Payload
# ============================================================

api_payload = api_test_sample.to_dict()

print("\nAPI payload:")

print(api_payload)


# ============================================================
# Load Versioned Model
# ============================================================

api_model = joblib.load(MODEL_PATH)

print("\nModel loaded successfully:")

print(MODEL_PATH)


# ============================================================
# Verify Model Feature Names
# ============================================================

if hasattr(api_model, "feature_names_in_"):

    saved_features = list(
        api_model.feature_names_in_
    )

    print(
        "\nModel feature count:",
        len(saved_features)
    )

    print("\nModel features:")

    for i, feature in enumerate(
        saved_features,
        start=1
    ):
        print(
            f"{i:02d}. {feature}"
        )

else:

    raise ValueError(
        "The saved model does not contain "
        "feature_names_in_."
    )


# ============================================================
# Verify Feature Compatibility
# ============================================================

if saved_features != api_features:

    print("\nWARNING: Feature mismatch!")

    print("\nModel features:")

    print(saved_features)

    print("\nAPI features:")

    print(api_features)

    raise ValueError(
        "API features do not exactly match "
        "the features used by the saved model."
    )

print(
    "\nFeature compatibility check: PASSED"
)


# ============================================================
# Prepare Sample for Model Prediction
# ============================================================

X_sample = api_test_sample.to_frame().T


# ============================================================
# Notebook / Local Model Prediction
# ============================================================

notebook_probability = float(
    api_model.predict_proba(X_sample)[0][1]
)

notebook_prediction = int(
    notebook_probability >= THRESHOLD
)


print("\n" + "=" * 60)

print("LOCAL MODEL / NOTEBOOK RESULT")

print("=" * 60)

print(
    "Probability:",
    notebook_probability
)

print(
    "Threshold:",
    THRESHOLD
)

print(
    "Prediction:",
    notebook_prediction
)


# ============================================================
# Send Request to FastAPI
# ============================================================

print("\n" + "=" * 60)

print("FASTAPI REQUEST")

print("=" * 60)

try:

    response = requests.post(
        API_URL,
        json=api_payload,
        timeout=30
    )

except requests.exceptions.ConnectionError:

    raise RuntimeError(
        "Could not connect to FastAPI. "
        "Make sure the server is running with:\n\n"
        "uvicorn api.main:app --reload"
    )


print(
    "HTTP status:",
    response.status_code
)


# ============================================================
# Validate FastAPI Response
# ============================================================

if response.status_code != 200:

    print(
        "\nFastAPI error response:"
    )

    print(
        response.text
    )

    raise RuntimeError(
        "FastAPI returned an error."
    )


api_result = response.json()


print(
    "\nFastAPI response:"
)

print(api_result)


# ============================================================
# Extract API Results
# ============================================================

api_probability = float(
    api_result["probability"]
)

api_prediction = int(
    api_result["prediction"]
)

api_threshold = float(
    api_result["threshold"]
)

model_version = api_result.get(
    "model_version"
)


# ============================================================
# Compare Notebook vs FastAPI
# ============================================================

print("\n" + "=" * 60)

print("NOTEBOOK VS FASTAPI COMPARISON")

print("=" * 60)

print(
    "\nNotebook probability:",
    notebook_probability
)

print(
    "FastAPI probability:",
    api_probability
)

print(
    "\nNotebook prediction:",
    notebook_prediction
)

print(
    "FastAPI prediction:",
    api_prediction
)

print(
    "\nNotebook threshold:",
    THRESHOLD
)

print(
    "FastAPI threshold:",
    api_threshold
)

print(
    "\nFastAPI model version:",
    model_version
)


# ============================================================
# Probability Comparison
# ============================================================

probability_difference = abs(
    notebook_probability - api_probability
)

print(
    "\nProbability difference:",
    probability_difference
)


# ============================================================
# Final Validation
# ============================================================

prediction_match = (
    notebook_prediction == api_prediction
)

threshold_match = (
    abs(api_threshold - THRESHOLD) < 1e-9
)

probability_match = (
    probability_difference < 1e-6
)


print("\n" + "=" * 60)

print("FINAL VALIDATION")

print("=" * 60)

print(
    "\nPrediction match:",
    prediction_match
)

print(
    "Threshold match:",
    threshold_match
)

print(
    "Probability match:",
    probability_match
)


if prediction_match and threshold_match and probability_match:

    print(
        "\nSUCCESS: "
        "Notebook and FastAPI predictions match."
    )

else:

    print(
        "\nWARNING: "
        "Notebook and FastAPI results do not fully match."
    )