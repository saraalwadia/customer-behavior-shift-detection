# Model Card
# XGBoost Customer Behavior Shift Detection — v1

---

## 1. Model Overview

| Item | Details |
|---|---|
| **Model Name** | Customer Behavior Shift Detection |
| **Model Type** | XGBoost Binary Classifier |
| **Model Version** | v1 |
| **Task** | Binary Classification |
| **Target** | `BehaviorShift` |
| **Framework** | XGBoost |
| **Serialization** | Joblib |
| **Model Artifact** | `models/xgboost/v1/model.joblib` |
| **Deployment** | FastAPI REST API |
| **API Version** | `v1` |
| **Prediction Threshold** | 0.30 |
| **Random State** | 42 |

---

# 2. Intended Use

The model is designed to detect significant shifts in customer purchasing behavior over time.

The intended use is to identify customers whose recent purchasing behavior differs significantly from their previous behavioral patterns.

The model is designed for:

- Customer behavior monitoring
- Behavioral shift detection
- Customer segmentation support
- Early identification of changing purchasing patterns
- Data-driven customer analysis

The model is not designed to directly predict customer churn.

The primary objective is to detect **behavioral change**, rather than simply determine whether a customer will stop purchasing.

---

# 3. Problem Definition

The model addresses the following question:

> Can historical and recent purchasing behavior be used to identify whether a customer's behavior has significantly shifted?

Customers are represented using temporal behavioral windows.

For each customer, current behavior is compared with previous behavior using both absolute behavioral features and percentage-change features.

The model then predicts:

```text
BehaviorShift = 1