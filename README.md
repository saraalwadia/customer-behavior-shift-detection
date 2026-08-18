# AI-Based Customer Behavior Shift Detection

An end-to-end Machine Learning system for detecting significant changes in customer purchasing behavior over time using transactional data.

> **Note:** This project focuses on **behavior shift detection**, not traditional customer churn prediction.

## Overview

The project uses the **Online Retail II** dataset to identify whether a customer's current purchasing behavior represents a significant shift compared with previous behavior.

The workflow includes:

* Data cleaning and preprocessing
* Customer-level temporal aggregation
* Behavioral and change-based feature engineering
* Rule-based target labeling
* Time-based train/test splitting
* Model comparison and XGBoost tuning
* Model evaluation and serialization
* FastAPI REST API deployment

## Dataset

**Online Retail II** — transactional retail data containing approximately **1.07M transactions** across 2009–2011.

After cleaning and filtering invalid transactions, customer behavior was transformed into sequential time windows for modeling.

### Target

`BehaviorShift`

* `0` — No significant behavior shift
* `1` — Significant behavior shift

The target is based on a **30% decrease in future orders or spending**.

## Feature Engineering

The model combines current and previous-period behavioral information, including:

* Spending and quantity
* Order frequency
* Unique products
* Active days
* Average order value
* Items per order
* Percentage changes between periods

Future-derived variables were excluded from the model to prevent **data leakage**.

## Modeling

Several approaches were evaluated, including:

* Logistic Regression
* Random Forest
* XGBoost

The final model is a tuned **XGBoost Classifier** using 22 behavioral and temporal features.

Hyperparameter tuning was performed using `RandomizedSearchCV` with **Average Precision** as the optimization metric.

## Final Results

Performance on the held-out chronological test set:

| Metric              |     Score |
| ------------------- | --------: |
| Accuracy            |  **0.74** |
| ROC-AUC             | **0.811** |
| PR-AUC              | **0.684** |
| Precision (Class 1) |  **0.61** |
| Recall (Class 1)    |  **0.72** |
| F1-score (Class 1)  |  **0.66** |

The model achieved approximately **72% recall** for customers experiencing a significant behavior shift.

An important experiment showed that removing the raw `orders` feature maintained similar performance while making `orders_change_pct` the dominant predictor. This supports the project's focus on **behavioral change over time** rather than absolute order volume.

## API

The trained model is serialized with `joblib` and served through a **FastAPI REST API**.

### Model

```text
Algorithm: XGBoost
Version: v1
Features: 22
Decision Threshold: 0.30
```

### Run locally

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

Prediction endpoint:

```text
POST /api/v1/predict
```

## Project Structure

```text
customer-behavior-shift-detection/
│
├── api/
│   ├── main.py
│   └── test_api.py
├── data/
│   ├── raw/
│   └── processed/
├── models/
│   └── xgboost/
│       └── v1/
│           └── model.joblib
├── notebooks/
├── requirements.txt
└── README.md
```

## Technologies

**Python · Pandas · NumPy · Scikit-learn · XGBoost · FastAPI · Joblib · Git · GitHub · Jupyter**

## Key Takeaway

The project demonstrates an end-to-end approach to detecting customer behavior shifts using temporal behavioral features, from raw transactional data through model development and evaluation to a deployable REST API.
