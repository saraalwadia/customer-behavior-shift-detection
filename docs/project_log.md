# Project Log — Customer Behavior Shift Detection

## Project Overview

Project:
AI-Based Customer Behavior Shift Detection

Purpose:
Build a machine learning system that detects significant changes in customer purchasing behavior over time.

Dataset:
Online Retail II

Main objective:
Compare customer behavior information over time and build a model capable of detecting BehaviorShift while avoiding future-data leakage.

Final ML model:
XGBoost

Final API:
FastAPI

Model version:
v1

Final model artifact:
models/xgboost/v1/model.joblib


# 1. Project Initialization

The project was created as part of the PSSAR Advanced Technical Training capstone.

The initial objective was to build a defensible machine learning model behind a versioned REST API.

The project requirements included:

- Data profiling
- Data cleaning
- Feature engineering
- Target/label creation
- Baseline modeling
- Comparison of multiple models
- Evaluation using appropriate classification metrics
- Leakage detection
- Hyperparameter tuning
- Model serialization
- REST API development
- API testing
- Documentation


# 2. Dataset Selection

The Online Retail II dataset was selected.

The original combined dataset contained:

Rows:
1,067,371

Features:
8

The dataset contains online retail transactions including:

- Invoice
- StockCode
- Description
- Quantity
- InvoiceDate
- Price
- Customer ID
- Country

The two available periods/sheets were combined into a single dataset.


# 3. Initial Data Profiling

Important initial findings included:

Transactions:
1,067,371

Transactions with Customer ID:
824,364

Transactions without Customer ID:
243,007

Customer ID coverage:
77.23%

Unique customers:
5,942

Customers active in multiple years:
2,890

Negative quantities:
22,950

Zero quantities:
0

Negative prices:
0 after cleaning

Zero prices:
6,202

Missing descriptions:
4,382

Date range:
2009-12-01 to 2011-12-09


# 4. Data Cleaning

The cleaning process focused on creating a reliable customer-level behavioral dataset.

Cancellation transactions were identified using invoices beginning with "C".

Cancellation rows were removed.

Non-commercial transactions were also removed.

Rows with invalid zero prices were removed.

Transactions without Customer IDs were excluded because customer-level behavior modeling requires a known customer identifier.

The cleaned transaction-level dataset contained approximately:

802,904 rows

After cleaning:

Missing Customer IDs:
0

Negative quantities:
0

Zero quantities:
0

Negative prices:
0

Zero prices:
0


# 5. Behavioral Window Construction

Customer transactions were transformed into temporal behavioral windows.

A 30-day behavioral window was used.

For each customer/window, behavioral information was calculated.

Main behavioral features included:

- orders
- spend
- totalQuantity
- unique_products
- active_days
- line_items
- avargeOrderValue
- items_per_order
- window_days

Historical/previous-window information was also calculated.

Examples:

- prev_orders
- prev_spend
- prev_totalQuantity
- prev_avargeOrderValue
- prev_unique_products
- prev_active_days
- prev_items_per_order

Behavior-change features were calculated to capture changes between behavioral periods.

Examples:

- orders_change_pct
- spend_change_pct
- totalQuantity_change_pct
- avargeOrderValue_change_pct
- unique_products_change_pct
- active_days_change_pct
- items_per_order_change_pct


# 6. Target Definition

The target variable was:

BehaviorShift

The target represents whether a significant change in customer behavior occurred in the future.

Future behavior variables were used to construct the label, but they were not allowed to become model features.

This distinction was important to prevent target leakage.


# 7. Final Labeled Dataset

The final labeled modeling dataset contained:

Rows:
15,582

Features:
34 columns before modeling exclusions.

Target distribution:

BehaviorShift = 0:
64.74%

BehaviorShift = 1:
35.26%

The dataset therefore had moderate class imbalance.


# 8. Leakage Control

The following future-looking variables were removed before model training:

- next_orders
- next_spend
- future_orders_change
- future_spend_change

Identifier/date columns were also removed:

- CustomerID
- window_id
- window_start
- window_end
- first_purchase
- last_purchase

The final model therefore used information available at the prediction point.


# 9. Initial XGBoost Model

An initial XGBoost classifier was trained.

Configuration:

n_estimators = 300
max_depth = 6
learning_rate = 0.1
scale_pos_weight = 1.8362842032651183
eval_metric = logloss
random_state = 42
n_jobs = -1

Initial results:

Accuracy:
0.73

ROC-AUC:
0.791834

PR-AUC:
0.660608

Positive-class precision:
0.60

Positive-class recall:
0.70

Positive-class F1:
0.65


# 10. Feature Importance Investigation

The first model showed that:

orders

was by far the most important feature.

Feature importance:

orders:
0.659998

This raised an important modeling question because the project's goal is to detect behavioral changes rather than simply rely on the absolute number of orders.

A feature-ablation experiment was therefore performed.


# 11. Orders Feature Ablation

The raw:

orders

feature was removed.

The model was retrained using the remaining behavioral and change features.

The most important feature became:

orders_change_pct

with importance:

0.427218

Other important features included:

active_days:
0.139432

spend:
0.103380

avargeOrderValue_change_pct:
0.043498

spend_change_pct:
0.038496


# 12. Model Comparison After Removing Orders

The model without the raw orders feature achieved:

Accuracy:
0.74

ROC-AUC:
0.811159

PR-AUC:
0.683632

Positive-class precision:
0.61

Positive-class recall:
0.72

Positive-class F1:
0.66

This showed that behavioral-change features retained substantial predictive value.


# 13. Time-Based Evaluation

A time-based train/test strategy was used.

The data was sorted by:

CustomerID
window_id

The split boundary was:

window_id = 19

Training:

window_id < 19

Testing:

window_id >= 19

Test rows:

3,247

Test window range:

19–23

This approach was selected instead of a random split to better simulate future prediction.


# 14. Class Imbalance Handling

The positive behavior-shift class represented approximately:

35.26%

of the dataset.

XGBoost was configured with:

scale_pos_weight = 1.8362842032651183

This increased the model's focus on detecting the positive class.


# 15. Hyperparameter Tuning

RandomizedSearchCV was used for XGBoost tuning.

The search explored:

n_estimators:
100, 200, 300, 500

max_depth:
3, 4, 5, 6, 8

learning_rate:
0.01, 0.05, 0.1, 0.2

subsample:
0.7, 0.8, 0.9, 1.0

colsample_bytree:
0.7, 0.8, 0.9, 1.0

Configuration:

n_iter = 30
cv = 5
scoring = average_precision
random_state = 42


# 16. Best Hyperparameters

The selected configuration was:

n_estimators:
200

max_depth:
6

learning_rate:
0.01

subsample:
1.0

colsample_bytree:
0.9

The final tuned model was selected based on Average Precision rather than accuracy.


# 17. Final Model Evaluation

Final model:

XGBoost

Features:
Behavior-aware features without the raw orders feature.

Final test results:

Accuracy:
0.74

ROC-AUC:
0.8111588464303074

PR-AUC:
0.6836320406452061

Class 0:

Precision:
0.83

Recall:
0.74

F1:
0.79

Class 1:

Precision:
0.61

Recall:
0.72

F1:
0.66

Confusion matrix:

[[1563, 539],
 [316, 829]]


# 18. Final Model Interpretation

The final model demonstrated that behavioral change features provide meaningful predictive information.

The most important feature was:

orders_change_pct

followed by:

active_days
spend
avargeOrderValue_change_pct
spend_change_pct

This supports the project's core idea of detecting changes in customer behavior over time.


# 19. Model Serialization

The final model was serialized using Joblib.

Final model path:

models/xgboost/v1/model.joblib

Model version:

v1

Versioning was introduced to make the deployed model reproducible and allow future model versions to coexist.


# 20. FastAPI Development

A FastAPI REST API was developed to expose the trained model.

The API provides a prediction endpoint:

POST /api/v1/predict

The API validates the incoming request using a structured request schema.

The endpoint receives the behavioral features required by the model.


# 21. Final API Feature Set

The final API/model uses 22 features:

1. spend
2. totalQuantity
3. unique_products
4. active_days
5. line_items
6. avargeOrderValue
7. items_per_order
8. window_days
9. prev_orders
10. prev_spend
11. prev_totalQuantity
12. prev_avargeOrderValue
13. prev_unique_products
14. prev_active_days
15. prev_items_per_order
16. orders_change_pct
17. spend_change_pct
18. totalQuantity_change_pct
19. avargeOrderValue_change_pct
20. unique_products_change_pct
21. active_days_change_pct
22. items_per_order_change_pct


# 22. API Threshold

The API uses:

threshold = 0.30

The model first generates a probability.

The API then converts the probability into a binary prediction.

If:

probability >= 0.30

the prediction is:

1

Otherwise:

0


# 23. API Testing

The API was tested locally using:

Uvicorn

The application successfully started at:

http://127.0.0.1:8000

The prediction endpoint was tested through the FastAPI Swagger documentation.

Endpoint:

http://127.0.0.1:8000/api/v1/predict


# 24. Successful API Test

A complete valid request returned:

HTTP 200

Example response:

{
  "prediction": 1,
  "probability": 0.3361409306526184,
  "threshold": 0.3,
  "model_version": "v1"
}

This confirmed successful communication between:

Client
→ FastAPI
→ Versioned XGBoost model
→ Prediction
→ API response


# 25. API Validation

The API correctly rejected incomplete requests with:

HTTP 422

This confirmed that required model features are validated before inference.

A complete request containing all 22 model features successfully generated a prediction.


# 26. Final Project Structure

The project was organized around:

data/
    raw/
    processed/

models/
    xgboost/
        v1/
            model.joblib

notebooks/

api/
    main.py
    test_api.py

README.md

debugging_log.md

project_log.md


# 27. Final Project Status

Data preparation:
Completed

Data cleaning:
Completed

Behavioral feature engineering:
Completed

Target labeling:
Completed

Leakage control:
Completed

Time-based evaluation:
Completed

XGBoost modeling:
Completed

Feature ablation:
Completed

Hyperparameter tuning:
Completed

Final model selection:
Completed

Model serialization:
Completed

FastAPI implementation:
Completed

API validation:
Completed

Documentation:
In progress / finalized through README, Debugging Log, and Project Log


# Final Technical Summary

Dataset:
Online Retail II

Final modeling dataset:
15,582 rows

Final model:
XGBoost

Final model version:
v1

Final model artifact:
models/xgboost/v1/model.joblib

Final features:
22

Final test rows:
3,247

Final accuracy:
0.74

Final ROC-AUC:
0.8112

Final PR-AUC:
0.6836

Positive-class recall:
0.72

Positive-class F1:
0.66

API:
FastAPI

Endpoint:
POST /api/v1/predict

Threshold:
0.30

Status:
Model trained, versioned, serialized, and successfully integrated with a working FastAPI inference endpoint.