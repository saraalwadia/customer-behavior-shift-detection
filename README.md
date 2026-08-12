# AI-Based Customer Behavior Shift Detection

## Project Overview

This project develops an end-to-end Machine Learning system for detecting significant changes in customer purchasing behavior over time.

The main objective is not traditional customer churn prediction. Instead, the system identifies whether a customer's current purchasing behavior represents a significant **behavior shift** compared with their previous behavior.

The project uses the **Online Retail II** transactional dataset and follows a complete Machine Learning workflow:

1. Data profiling
2. Data cleaning
3. Customer-level behavioral aggregation
4. Time-window construction
5. Behavioral change feature engineering
6. Target labeling
7. Time-based train/test splitting
8. Baseline and behavior-aware modeling
9. XGBoost modeling
10. Hyperparameter tuning
11. Feature importance analysis
12. Model serialization
13. FastAPI deployment
14. API testing

The final system exposes the trained XGBoost model through a REST API using FastAPI.

---

# 1. Project Objective

The project investigates whether historical and behavioral-change features can be used to detect significant changes in customer behavior.

The key research question is:

> Can customer behavioral changes over time improve the detection of significant customer behavior shifts?

Instead of looking only at static customer characteristics, the project incorporates temporal information such as:

- Changes in spending
- Changes in order frequency
- Changes in quantity purchased
- Changes in product diversity
- Changes in activity
- Changes in average order value
- Changes in items per order

The final model predicts:

- `0` → No significant behavior shift
- `1` → Significant behavior shift

---

# 2. Dataset

## Dataset Name

**Online Retail II**

The dataset contains transactional records from an online retail store.

The raw dataset initially contained:

- **1,067,371 transaction rows**
- **8 original features**

The original data covered approximately:

- December 2009
- December 2010
- December 2011

The original columns included transaction-level information such as:

- Invoice
- StockCode
- Description
- Quantity
- InvoiceDate
- Price
- Customer ID
- Country

---

# 3. Data Profiling

Initial profiling identified several important data-quality issues.

## Initial Dataset

```text
Rows: 1,067,371
Columns: 8
```

## Customer ID Coverage

```text
Transactions with Customer ID:    824,364
Transactions without Customer ID: 243,007
Customer ID coverage:             77.23%
```

Since the project focuses on customer behavior, transactions without a Customer ID could not be reliably associated with a customer and were therefore excluded from customer-level modeling.

## Customers

```text
Unique customers: 5,942
Customers active in multiple years: 2,890
```

## Quantity Issues

```text
Negative quantities: 22,950
Zero quantities: 0
```

Negative quantities were investigated and were primarily associated with cancellation transactions.

The analysis showed:

```text
Negative-quantity cancellation invoices: 19,493
Negative-quantity non-cancellation rows: 3,457
```

## Price Issues

```text
Negative prices: 0 after cleaning
Zero prices: 6,202 initially
```

## Missing Values

```text
Missing Description values: 4,382
Missing Customer IDs: 243,007
```

## Duplicate Records

Duplicate records were also investigated during profiling and cleaning.

Different stages of the cleaning analysis identified duplicate rows/groups, with the final cleaned dataset being checked to ensure that duplicated transactional records did not distort the customer-level behavioral features.

---

# 4. Data Cleaning

The cleaning process was designed to preserve valid commercial transactions while removing records that could introduce noise or invalid behavior signals.

The major cleaning operations were:

1. Remove transactions without Customer ID.
2. Identify cancellation transactions.
3. Remove cancellation transactions.
4. Remove non-commercial/non-product records.
5. Remove zero-price transactions.
6. Remove or handle duplicate transactional records.
7. Convert transaction dates into usable temporal variables.
8. Aggregate transactions at the customer/time-window level.

After cleaning:

```text
Rows after removing transactions without Customer ID: 824,364
Purchase rows after cancellation filtering:            805,620
After removing zero-price rows:                        805,549
After removing non-commercial transactions:            802,904
```

The final cleaned transactional dataset contained:

```text
802,904 rows
```

with:

```text
Missing Customer IDs: 0
Negative quantities: 0
Zero quantities: 0
Negative prices: 0
Zero prices: 0
```

---

# 5. Behavioral Time Windows

Customer behavior was transformed from individual transactions into sequential customer-level time windows.

The project uses approximately 30-day behavioral windows.

Each customer can therefore have multiple observations representing different periods of their purchasing behavior.

A window contains information such as:

- Number of orders
- Total spending
- Total quantity
- Number of unique products
- Number of active days
- Number of line items
- Average order value
- Items per order
- Previous-period behavior
- Percentage change from the previous period

This transformation allows the model to learn temporal behavioral patterns instead of treating every transaction independently.

---

# 6. Modeling Dataset

The final labeled modeling dataset used for the XGBoost model was:

```text
Shape: 15,582 rows × 34 columns
```

The target variable is:

```text
BehaviorShift
```

Target distribution:

```text
Class 0: 64.74%
Class 1: 35.26%
```

Therefore, the dataset is moderately imbalanced.

Because of this imbalance, the modeling process did not rely only on accuracy.

The main evaluation metrics were:

- Precision
- Recall
- F1-score
- ROC-AUC
- PR-AUC / Average Precision

---

# 7. Target Variable

The target column is:

```text
BehaviorShift
```

Interpretation:

```text
0 = No significant behavior shift
1 = Significant behavior shift
```

The target was constructed using future customer behavior.

Because future information is used to define the target, future-derived columns must never be provided to the model as input features.

---

# 8. Leakage Prevention

The following future-looking columns were explicitly removed from the modeling features:

```text
next_orders
next_spend
future_orders_change
future_spend_change
```

These variables describe future behavior and would cause target leakage if used as predictors.

Identifier and date columns were also excluded:

```text
CustomerID
window_id
window_start
window_end
first_purchase
last_purchase
```

The target itself was also removed from the input features.

This ensures that the model predicts the behavior shift using information available at the prediction point.

---

# 9. Final XGBoost Features

The original behavior-aware model initially used 23 features.

However, an additional experiment was performed to determine whether the `orders` feature dominated the model.

The final selected model excludes:

```text
orders
```

The final model therefore uses **22 features**.

The final feature list is:

```text
spend
totalQuantity
unique_products
active_days
line_items
avargeOrderValue
items_per_order
window_days
prev_orders
prev_spend
prev_totalQuantity
prev_avargeOrderValue
prev_unique_products
prev_active_days
prev_items_per_order
orders_change_pct
spend_change_pct
totalQuantity_change_pct
avargeOrderValue_change_pct
unique_products_change_pct
active_days_change_pct
items_per_order_change_pct
```

> Note: `avargeOrderValue` is intentionally kept with this spelling because it is the column name used in the processed dataset and trained model.

---

# 10. Time-Based Train/Test Split

A chronological split was used instead of a random split.

The dataset was sorted by:

```text
CustomerID
window_id
```

The split boundary was determined using the 80th percentile of `window_id`.

The resulting test set contained:

```text
Test rows: 3,247
Test window range: 19 to 23
```

This approach is important because the model should simulate a real-world prediction scenario where historical data is used to predict future behavior.

A random split could allow information from later periods to appear in the training data and produce overly optimistic results.

---

# 11. Initial XGBoost Model

The first XGBoost model was trained using the behavior-aware feature set.

The model configuration was:

```python
XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.1,
    scale_pos_weight=scale_pos_weight,
    eval_metric="logloss",
    random_state=42,
    n_jobs=-1
)
```

The class imbalance was handled using:

```text
scale_pos_weight = 1.8363
```

This was calculated from the training data:

```text
number of class 0 samples
-------------------------
number of class 1 samples
```

---

# 12. Initial XGBoost Results

The initial model achieved:

```text
Accuracy: 0.73
```

Class 0:

```text
Precision: 0.82
Recall:    0.75
F1-score:  0.78
```

Class 1:

```text
Precision: 0.60
Recall:    0.70
F1-score:  0.65
```

Overall:

```text
ROC-AUC: 0.7918
PR-AUC:  0.6606
```

Confusion matrix:

```text
[[1568, 534],
 [ 338, 807]]
```

The model was able to identify a substantial proportion of behavior-shift cases while maintaining reasonable precision.

---

# 13. Initial Feature Importance

The initial XGBoost model showed that `orders` was by far the most important feature.

Top feature importances:

```text
orders                         0.659998
prev_active_days               0.043648
avargeOrderValue_change_pct    0.037769
spend                          0.022218
spend_change_pct               0.017253
line_items                     0.014897
avargeOrderValue               0.014622
prev_avargeOrderValue          0.014212
totalQuantity                  0.014002
prev_items_per_order           0.013904
prev_orders                    0.013652
prev_totalQuantity             0.013519
items_per_order_change_pct     0.013462
unique_products_change_pct     0.013274
prev_spend                     0.013247
```

This raised an important modeling question:

> Is the model actually learning behavioral change, or is it relying heavily on the raw number of orders?

To investigate this, a second experiment removed the `orders` feature.

---

# 14. Hyperparameter Tuning

Hyperparameter optimization was performed using:

```text
RandomizedSearchCV
```

The search used:

```text
30 parameter combinations
5-fold cross-validation
150 total fits
```

The optimization metric was:

```text
average_precision
```

This metric was selected because the target classes are imbalanced and PR-AUC is more informative than accuracy alone for the positive behavior-shift class.

The parameter search included:

```python
n_estimators:
[100, 200, 300, 500]

max_depth:
[3, 4, 5, 6, 8]

learning_rate:
[0.01, 0.05, 0.1, 0.2]

subsample:
[0.7, 0.8, 0.9, 1.0]

colsample_bytree:
[0.7, 0.8, 0.9, 1.0]
```

---

# 15. Tuned Model With Orders

The best hyperparameters were:

```text
n_estimators:     200
max_depth:        6
learning_rate:    0.01
subsample:        1.0
colsample_bytree: 0.9
```

Best cross-validation Average Precision:

```text
0.7081
```

Test results after tuning:

```text
Accuracy: 0.74
```

Class 0:

```text
Precision: 0.84
Recall:    0.75
F1-score:  0.79
```

Class 1:

```text
Precision: 0.61
Recall:    0.73
F1-score:  0.67
```

Overall:

```text
ROC-AUC: 0.8124
PR-AUC:  0.6893
```

The tuned model improved over the initial model:

```text
ROC-AUC: 0.7918 → 0.8124
PR-AUC:  0.6606 → 0.6893
```

---

# 16. Experiment Without the Orders Feature

Because `orders` dominated the initial model, a second experiment removed it.

The resulting model used 22 features.

The model achieved:

```text
Accuracy: 0.74
```

Class 0:

```text
Precision: 0.83
Recall:    0.74
F1-score:  0.79
```

Class 1:

```text
Precision: 0.61
Recall:    0.72
F1-score:  0.66
```

Overall:

```text
ROC-AUC: 0.8112
PR-AUC:  0.6836
```

Confusion matrix:

```text
[[1563, 539],
 [ 316, 829]]
```

---

# 17. Feature Importance Without Orders

After removing `orders`, the model relied much more strongly on behavioral-change features.

The most important features were:

```text
orders_change_pct              0.427218
active_days                    0.139432
spend                          0.103380
avargeOrderValue_change_pct    0.043498
spend_change_pct               0.038496
avargeOrderValue               0.029110
line_items                     0.026191
prev_active_days               0.025782
prev_orders                    0.020099
active_days_change_pct         0.015778
prev_avargeOrderValue          0.015746
items_per_order_change_pct     0.013724
unique_products_change_pct     0.013244
prev_totalQuantity             0.012250
totalQuantity                  0.012232
```

This experiment is particularly important for the project's research objective.

After removing `orders`, the model's strongest predictor became:

```text
orders_change_pct
```

This supports the idea that the model is detecting behavioral changes rather than simply relying on the absolute number of orders.

---

# 18. Final Hyperparameter Tuning Without Orders

A second RandomizedSearchCV was performed after removing `orders`.

The best parameters were again:

```text
n_estimators:     200
max_depth:        6
learning_rate:    0.01
subsample:        1.0
colsample_bytree: 0.9
```

Best cross-validation Average Precision:

```text
0.7027
```

The final model therefore uses the tuned XGBoost configuration without the raw `orders` feature.

---

# 19. Final Model Performance

The final selected model achieved:

```text
Accuracy: 0.74
ROC-AUC:  0.8112
PR-AUC:   0.6836
```

For the positive class (`BehaviorShift = 1`):

```text
Precision: 0.61
Recall:    0.72
F1-score:  0.66
```

The final confusion matrix was:

```text
[[1563, 539],
 [ 316, 829]]
```

This means:

```text
True Negatives:  1563
False Positives: 539
False Negatives: 316
True Positives:  829
```

The final model successfully identifies a large proportion of behavior-shift cases, with a recall of approximately 72% for the positive class.

---

# 20. Why PR-AUC Was Used

The target distribution is:

```text
Class 0: 64.74%
Class 1: 35.26%
```

Because the dataset is not perfectly balanced, accuracy alone is not sufficient to evaluate the model.

The project therefore emphasizes:

```text
PR-AUC
ROC-AUC
Precision
Recall
F1-score
```

PR-AUC is particularly useful because the project is interested in correctly identifying customers experiencing a behavior shift.

---

# 21. Final Model Serialization

The final XGBoost model is saved using `joblib`.

Current model path:

```text
models/xgboost/v1/model.joblib
```

The model can be loaded using:

```python
import joblib

model = joblib.load(
    "models/xgboost/v1/model.joblib"
)
```

The serialized model is the version used by the FastAPI application.

---

# 22. FastAPI Deployment

The trained model was integrated into a FastAPI REST API.

The API application is located under:

```text
api/
```

The application can be started locally using:

```bash
uvicorn api.main:app --reload
```

The server runs locally at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

The prediction endpoint is:

```text
POST /api/v1/predict
```

Full local endpoint:

```text
http://127.0.0.1:8000/api/v1/predict
```

---

# 23. API Prediction Logic

The API loads the versioned XGBoost model and receives the model features as JSON.

The API returns:

```json
{
  "prediction": 1,
  "probability": 0.3361409306526184,
  "threshold": 0.3,
  "model_version": "v1"
}
```

The prediction is determined using:

```text
probability >= 0.30
```

Therefore:

```text
probability >= 0.30 → BehaviorShift = 1
probability <  0.30 → BehaviorShift = 0
```

The threshold was selected as part of the project's classification decision process rather than relying blindly on the default 0.50 threshold.

---

# 24. API Input Features

The final API must match the exact feature set used by the serialized model.

The final model expects **22 features**:

```text
spend
totalQuantity
unique_products
active_days
line_items
avargeOrderValue
items_per_order
window_days
prev_orders
prev_spend
prev_totalQuantity
prev_avargeOrderValue
prev_unique_products
prev_active_days
prev_items_per_order
orders_change_pct
spend_change_pct
totalQuantity_change_pct
avargeOrderValue_change_pct
unique_products_change_pct
active_days_change_pct
items_per_order_change_pct
```

The order of the features must also be handled consistently with the trained model.

---

# 25. Example API Request

A valid request should contain all 22 features.

Example:

```json
{
  "spend": 584.91,
  "totalQuantity": 277,
  "unique_products": 22,
  "active_days": 1,
  "line_items": 22,
  "avargeOrderValue": 584.91,
  "items_per_order": 22,
  "window_days": 30,
  "prev_orders": 1,
  "prev_spend": 382.52,
  "prev_totalQuantity": 196,
  "prev_avargeOrderValue": 382.52,
  "prev_unique_products": 18,
  "prev_active_days": 1,
  "prev_items_per_order": 18,
  "orders_change_pct": 0.0,
  "spend_change_pct": 0.5290965,
  "totalQuantity_change_pct": 0.4132653,
  "avargeOrderValue_change_pct": 0.5290965,
  "unique_products_change_pct": 0.2222222,
  "active_days_change_pct": 0.0,
  "items_per_order_change_pct": 0.2222222
}
```

Example successful response:

```json
{
  "prediction": 1,
  "probability": 0.3361409306526184,
  "threshold": 0.3,
  "model_version": "v1"
}
```

---

# 26. API Validation

An API testing script was created:

```text
api/test_api.py
```

The purpose of this script is to:

1. Load the labeled modeling dataset.
2. Verify that API features exist in the dataset.
3. Reproduce the time-based test split.
4. Select a real test observation.
5. Construct an API payload.
6. Load the same serialized model used by FastAPI.
7. Verify the model's expected feature names.
8. Run a local prediction.
9. Compare the model output with the API output.

This helps verify that the model used in the notebook and the model exposed by FastAPI are consistent.

---

# 27. API Testing Issue Identified

During the latest API validation, an important feature mismatch was identified.

The saved model reports:

```text
Model feature count: 22
```

and expects:

```text
spend
totalQuantity
unique_products
active_days
line_items
avargeOrderValue
items_per_order
window_days
prev_orders
prev_spend
prev_totalQuantity
prev_avargeOrderValue
prev_unique_products
prev_active_days
prev_items_per_order
orders_change_pct
spend_change_pct
totalQuantity_change_pct
avargeOrderValue_change_pct
unique_products_change_pct
active_days_change_pct
items_per_order_change_pct
```

The API test initially constructed only 21 features and omitted:

```text
spend
```

This caused the validation script to report:

```text
ValueError:
API features do not exactly match the features used by the saved model.
```

The correct solution is **not to remove `spend` from the model**.

Instead, the API input schema and test payload must be updated so that `spend` is included and the API contains exactly the same 22 features as the saved model.

This is an important consistency requirement between:

```text
Training → Saved Model → FastAPI → API Test
```

---

# 28. API Status

The FastAPI server itself successfully starts with:

```bash
uvicorn api.main:app --reload
```

The application starts successfully:

```text
Application startup complete.
```

The prediction endpoint has also successfully returned a `200` response for a valid payload.

An earlier invalid request returned:

```text
422 Unprocessable Content
```

because the required:

```text
spend
```

field was missing.

After adding `spend`, the API successfully returned:

```text
200 OK
```

with:

```json
{
  "prediction": 1,
  "probability": 0.3361409306526184,
  "threshold": 0.3,
  "model_version": "v1"
}
```

The remaining validation work is to ensure that `api/test_api.py` uses the exact same 22-feature schema as the FastAPI endpoint and serialized model.

---

# 29. Project Structure

The project follows a structured ML project layout:

```text
customer-behavior-shift-detection/
│
├── api/
│   ├── main.py
│   └── test_api.py
│
├── data/
│   ├── raw/
│   │   └── online_retail_II.csv
│   │
│   └── processed/
│       ├── online_retail_II_labeled_30.csv
│       └── ...
│
├── models/
│   └── xgboost/
│       └── v1/
│           └── model.joblib
│
├── notebooks/
│   ├── ...
│   └── 06_XGBoost.ipynb
│
├── README.md
│
├── .gitignore
│
└── requirements.txt
```

The exact contents of the `notebooks` and `data/processed` directories may vary as intermediate experiments and datasets are added.

---

# 30. Technologies Used

## Programming Language

```text
Python
```

## Data Processing

```text
pandas
numpy
```

## Machine Learning

```text
scikit-learn
XGBoost
```

## Model Serialization

```text
joblib
```

## API

```text
FastAPI
Uvicorn
```

## Development

```text
Jupyter Notebook
VS Code
Git
GitHub
Python virtual environment
```

---

# 31. Main Machine Learning Pipeline

The complete pipeline can be summarized as:

```text
Raw Online Retail II Dataset
            │
            ▼
      Data Profiling
            │
            ▼
       Data Cleaning
            │
            ▼
 Customer-Level Aggregation
            │
            ▼
   30-Day Time Windows
            │
            ▼
 Behavioral Feature Engineering
            │
            ▼
      Target Labeling
            │
            ▼
 Leakage Removal
            │
            ▼
 Time-Based Train/Test Split
            │
            ▼
     XGBoost Baseline
            │
            ▼
 Feature Importance Analysis
            │
            ▼
 Remove Dominant "orders" Feature
            │
            ▼
 RandomizedSearchCV
            │
            ▼
      Final XGBoost
            │
            ▼
       joblib Model
            │
            ▼
         FastAPI
            │
            ▼
      REST Prediction API
```

---

# 32. Key Findings

The modeling experiments produced several important findings.

### Finding 1 — Behavioral features are useful

The model achieved:

```text
ROC-AUC ≈ 0.81
PR-AUC  ≈ 0.68
```

showing that customer behavior features contain useful predictive information for detecting behavior shifts.

### Finding 2 — Raw order count dominated the first model

The first XGBoost model assigned approximately:

```text
65.99%
```

of feature importance to:

```text
orders
```

This indicated that the model could potentially rely too heavily on the absolute number of orders.

### Finding 3 — Removing `orders` still produced strong performance

After removing `orders`:

```text
ROC-AUC: 0.8112
PR-AUC:  0.6836
Accuracy: 0.74
```

The performance remained very similar to the model containing `orders`.

This is important because it suggests that the model does not require the raw order count to achieve useful predictive performance.

### Finding 4 — Behavioral change became the dominant signal

After removing `orders`, the most important feature became:

```text
orders_change_pct
```

with importance:

```text
0.427218
```

Other important behavioral features included:

```text
active_days
spend
avargeOrderValue_change_pct
spend_change_pct
```

This supports the project's central idea that **changes in customer behavior over time are useful signals for detecting behavior shifts**.

---

# 33. Limitations

Several limitations should be considered.

## 1. Dataset limitations

The project uses a historical retail dataset from one business context.

Therefore, model performance may not generalize directly to:

- Other retailers
- Other industries
- Subscription businesses
- Digital products
- Different customer populations

## 2. Customer ID availability

A significant portion of the original transactions did not contain Customer IDs.

These transactions were excluded because they could not reliably contribute to customer-level behavioral modeling.

## 3. Target definition

The `BehaviorShift` target is based on a rule-based definition of future behavioral change.

Therefore, the target represents the project's operational definition of behavior shift rather than a universally established ground truth.

## 4. Temporal data limitations

The dataset contains a finite historical period.

More recent real-world customer behavior may differ from the patterns observed in this dataset.

## 5. Feature importance interpretation

XGBoost feature importance indicates predictive contribution within the trained model.

It does not prove causal relationships.

For example:

```text
orders_change_pct
```

being highly important does not mean that it directly causes a customer behavior shift.

---

# 34. Reproducibility

The project uses:

```text
random_state = 42
```

for the main XGBoost models and randomized hyperparameter searches.

The model is saved using:

```text
joblib
```

and versioned under:

```text
models/xgboost/v1/model.joblib
```

This allows the FastAPI service to use the same trained model that was evaluated during the modeling stage.

---

# 35. Running the Project

## Step 1 — Create virtual environment

Windows:

```bash
python -m venv .venv
```

Activate:

```bash
.venv\Scripts\activate
```

---

## Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

If required packages are missing, they can be installed inside the active `.venv`.

For example:

```bash
pip install pandas numpy scikit-learn xgboost joblib fastapi uvicorn
```

---

# 36. Run the FastAPI Application

From the project root:

```bash
uvicorn api.main:app --reload
```

The server should start at:

```text
http://127.0.0.1:8000
```

Open the Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

Then use:

```text
POST /api/v1/predict
```

to test the model.

---

# 37. Run API Validation

After starting the API, the validation script can be executed from the project root:

```bash
python api/test_api.py
```

The validation script should confirm:

```text
Dataset loaded successfully
API features exist
Model loaded successfully
Model feature count = 22
API feature count = 22
Feature names match
Prediction generated successfully
```

The final validation should use exactly the same 22 features expected by:

```text
models/xgboost/v1/model.joblib
```

---

# 38. Important Model/API Consistency Rule

The following three components must always use the same feature schema:

```text
1. Training notebook
2. FastAPI request schema
3. API test script
```

The final model expects:

```text
22 features
```

Therefore, changing the API feature list without retraining/re-saving the model can cause:

```text
Feature mismatch
```

The feature:

```text
spend
```

must remain included because it is part of the final serialized model's feature set.

---

# 39. Current Final Model

The current final model is:

```text
Algorithm: XGBoost Classifier
Model version: v1
File: models/xgboost/v1/model.joblib
Features: 22
Threshold: 0.30
```

Final test performance:

```text
Accuracy: 0.74
ROC-AUC:  0.8112
PR-AUC:   0.6836
```

Positive-class performance:

```text
Precision: 0.61
Recall:    0.72
F1-score:  0.66
```

---

# 40. Final Conclusion

This project developed an end-to-end Machine Learning system for detecting customer behavior shifts from transactional data.

The project demonstrated that temporal behavioral features can provide meaningful predictive information beyond static customer characteristics.

The final XGBoost model achieved:

```text
Accuracy = 0.74
ROC-AUC  = 0.8112
PR-AUC   = 0.6836
```

with approximately:

```text
72% recall
```

for customers classified as experiencing a behavior shift.

An important modeling experiment showed that the raw `orders` feature dominated the initial model. After removing it, the model maintained similar performance, while `orders_change_pct` became the dominant feature.

This provides stronger evidence that the final system is capturing **changes in customer behavior over time**, which is the central objective of the project.

The trained model was serialized using `joblib` and integrated into a versioned FastAPI REST API.

The resulting system provides an end-to-end pipeline:

```text
Transactional Data
        ↓
Cleaning
        ↓
Customer Behavioral Windows
        ↓
Behavior Change Features
        ↓
BehaviorShift Label
        ↓
XGBoost
        ↓
Model Evaluation
        ↓
joblib Model
        ↓
FastAPI REST API
        ↓
Behavior Shift Prediction
```

The project therefore satisfies the core objective of building a defensible Machine Learning model and exposing it through a versioned REST API.