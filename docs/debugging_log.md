# Debugging Log — Customer Behavior Shift Detection

## 1. Project Overview

This debugging log documents the important technical issues, validation steps, design corrections, and model/API consistency checks performed during the development of the Customer Behavior Shift Detection project.

The project aims to detect whether a customer's behavior has shifted significantly over time using transaction-based behavioral features.

The project compares customer behavior across time windows and uses machine learning to predict the `BehaviorShift` target.

The final pipeline includes:

1. Raw transaction data profiling
2. Data cleaning
3. Customer-level temporal aggregation
4. Behavioral feature engineering
5. Behavior-shift labeling
6. Time-based train/test splitting
7. XGBoost modeling
8. Hyperparameter tuning
9. Feature importance analysis
10. Removal of potentially dominant/non-behavioral features
11. Final model selection
12. Model serialization using `joblib`
13. FastAPI deployment
14. API endpoint validation
15. Independent API test validation


## 2. Dataset Profiling and Initial Data Issues

The selected dataset was the Online Retail II dataset.

The combined raw dataset contained:

- 1,067,371 transaction rows
- 8 original features
- Date range from December 2009 to December 2011
- 5,942 unique customers with Customer IDs
- 824,364 transactions with Customer IDs
- 243,007 transactions without Customer IDs
- Customer ID coverage: approximately 77.23%

Initial data-quality problems included:

- Missing Customer IDs
- Negative quantities
- Zero prices
- Negative prices
- Missing descriptions
- Duplicate transaction rows
- Cancellation transactions
- Non-commercial transactions

These issues had to be addressed before creating customer-level behavioral features.


## 3. Cancellation and Transaction Cleaning

Negative quantities were investigated instead of being removed blindly.

The analysis showed that many negative quantities were associated with cancellation invoices, especially invoices beginning with `C`.

The cleaning process therefore distinguished cancellation transactions from normal purchases.

Important results included:

- 22,950 rows initially had negative quantities.
- 19,493 negative-quantity rows were associated with cancellation invoices.
- Cancellation invoices were removed from the modeling data.
- Zero-price rows were also removed.
- Non-commercial transactions were removed.
- Transactions without Customer IDs were excluded because customer-level behavior could not be modeled reliably without customer identification.

After the cleaning process, the customer-level modeling data contained:

- 802,904 rows
- No missing Customer IDs
- No negative quantities
- No zero quantities
- No negative prices
- No zero prices

Duplicate records were also investigated during profiling. Different duplicate counts appeared during intermediate stages because duplicate rows and duplicate groups were measured separately. The final cleaning/profiling stage used the reconciled dataset rather than relying on the early intermediate counts.


## 4. Customer-Level Temporal Dataset

The project was changed from a transaction-level prediction problem into a temporal customer behavior problem.

Customer behavior was aggregated into fixed time windows.

The modeling dataset was saved as:

`online_retail_II_labeled_30.csv`

The final labeled dataset contained:

- 15,582 rows
- 34 columns

Each row represents a customer's behavior during a specific temporal window.

The dataset includes:

- Customer identifiers
- Window identifiers
- Window dates
- Current behavioral features
- Previous-window behavioral features
- Percentage-change features
- Future behavioral information used for labeling
- `BehaviorShift` target


## 5. Leakage Prevention

A major correctness issue in the modeling pipeline was preventing future information from entering the predictors.

The following columns were identified as leakage variables and removed from the model features:

- `next_orders`
- `next_spend`
- `future_orders_change`
- `future_spend_change`

These variables describe future customer behavior and therefore cannot be available when making a real prediction.

The target column was also excluded from the predictors:

- `BehaviorShift`

Identifier/date columns were excluded from the machine-learning feature matrix:

- `CustomerID`
- `window_id`
- `window_start`
- `window_end`
- `first_purchase`
- `last_purchase`

This ensured that the model learned from behavioral information rather than customer identity or future information.


## 6. Final Feature Set

The main XGBoost model initially used 23 features.

The feature set included current behavior, previous behavior, and behavioral-change variables.

The original feature list was:

- `orders`
- `spend`
- `totalQuantity`
- `unique_products`
- `active_days`
- `line_items`
- `avargeOrderValue`
- `items_per_order`
- `window_days`
- `prev_orders`
- `prev_spend`
- `prev_totalQuantity`
- `prev_avargeOrderValue`
- `prev_unique_products`
- `prev_active_days`
- `prev_items_per_order`
- `orders_change_pct`
- `spend_change_pct`
- `totalQuantity_change_pct`
- `avargeOrderValue_change_pct`
- `unique_products_change_pct`
- `active_days_change_pct`
- `items_per_order_change_pct`

The target distribution was:

- Class 0: 64.74%
- Class 1: 35.26%

Because the positive class was smaller, class weighting was used through XGBoost's `scale_pos_weight`.


## 7. Time-Based Train/Test Split

A random train/test split was avoided because this is a temporal behavior-prediction problem.

The data was ordered by customer and temporal window.

The split was based on `window_id`.

The 80th percentile of the window identifier was used as the split boundary:

`split_window = 19.0`

The final test set contained:

- 3,247 rows
- Window range: 19 to 23

The time-based split was important because a random split could allow information from later behavior periods to influence model training and produce overly optimistic results.


## 8. Initial XGBoost Model

An initial XGBoost classifier was trained using:

- `n_estimators = 300`
- `max_depth = 6`
- `learning_rate = 0.1`
- `scale_pos_weight = 1.8363`
- `eval_metric = logloss`
- `random_state = 42`

Initial test performance:

- Accuracy: 0.73
- ROC-AUC: 0.7918
- PR-AUC: 0.6606

Class 0:

- Precision: 0.82
- Recall: 0.75
- F1: 0.78

Class 1:

- Precision: 0.60
- Recall: 0.70
- F1: 0.65

Confusion matrix:

```text
[[1568  534]
 [ 338  807]]


9. MODEL FEATURE ALIGNMENT ISSUE

Problem:
The saved XGBoost model contained 22 features, while the API request schema initially contained only 21 features.

The saved model expected:

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

However, the API test initially provided only 21 features and was missing:

spend

Resolution:
The API request schema and test payload were updated to include the complete feature set expected by the saved model.

The final API therefore uses the same 22 features used during model training.


10. MODEL/API FEATURE ORDER VERIFICATION

Problem:
Having the same feature names is not sufficient for a production ML API. The order of the features must also match the order used during model training.

Resolution:
The API test was updated to inspect the feature names stored in the trained XGBoost model using the model's feature metadata.

The model feature list was compared against the API feature list.

This verification confirmed that the final API must construct the input DataFrame using the exact model feature order.

Final model feature order:

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

Resolution implemented:
The API input is aligned with the saved model rather than relying on arbitrary JSON field ordering.


11. MODEL VERSIONING AND API MODEL PATH

Problem:
The project initially referenced multiple model paths, including:

../models/xgboost/v1/xgboost_behavior_shift_30.pkl

and later:

models/xgboost/v1/model.joblib

This created ambiguity regarding which model was actually being served by the API.

Resolution:
The project was standardized around the versioned model:

models/xgboost/v1/model.joblib

The API and API testing workflow were updated to load this versioned model.

This provides a clearer model lifecycle and makes it possible to introduce future model versions without overwriting the existing production model.


12. JOBLIB MODEL SERIALIZATION

Problem:
The project originally used a .pkl filename in parts of the notebook/testing workflow, while the API used a Joblib model file.

Resolution:
The project standardized model serialization using Joblib.

Final model artifact:

models/xgboost/v1/model.joblib

The API loads the same versioned Joblib model used for inference testing.

This avoids maintaining multiple competing copies of the trained model.


13. REMOVING THE DEPENDENCY ON A SEPARATE FEATURE-NAMES FILE

Problem:
The API test initially attempted to load a separate file containing feature names:

xgboost_behavior_shift_30_features.pkl

That file was not part of the final versioned model structure.

Resolution:
The feature names are obtained directly from the saved XGBoost model metadata instead of depending on an additional feature-name artifact.

This reduces the number of required model files and prevents inconsistencies between the model and an externally stored feature list.


14. FINAL MODEL FEATURE COUNT

Final verification showed:

Model feature count: 22

The saved model expects exactly 22 input features.

The API was therefore updated to provide exactly the same 22 features.

This check became an important part of the API validation process because an incorrect number of features can cause inference failures or, worse, inconsistent predictions.


15. LEAKAGE PREVENTION

Problem:
The labeled dataset contained variables describing future customer behavior:

next_orders
next_spend
future_orders_change
future_spend_change

These variables were used to generate the target and therefore could leak future information into the model.

Resolution:
All future-looking variables were explicitly removed before training.

Removed leakage features:

next_orders
next_spend
future_orders_change
future_spend_change

The target variable was also excluded from the feature matrix.

This ensures that the model predicts behavior shift using information available at the prediction window rather than information from the future.


16. IDENTIFIER REMOVAL

Problem:
Customer and temporal identifiers were present in the dataset but should not be used as predictive features.

Resolution:
The following columns were excluded from the modeling feature matrix:

CustomerID
window_id
window_start
window_end
first_purchase
last_purchase

The model therefore focuses on behavioral and historical customer information rather than identifiers or raw date fields.


17. TARGET DISTRIBUTION

The final labeled dataset contained:

15,582 rows

Target:

BehaviorShift = 0: 64.74%
BehaviorShift = 1: 35.26%

The target was moderately imbalanced.

Resolution:
The XGBoost model used class weighting through:

scale_pos_weight

Calculated from the training data as:

scale_pos_weight = number of class 0 samples / number of class 1 samples

Final value:

1.8362842032651183

This gives additional importance to the minority behavior-shift class.


18. TIME-BASED TRAIN/TEST SPLIT

Problem:
A random train/test split would not be appropriate for this project because the goal is to detect future behavior shifts.

Random splitting could allow temporally later observations to influence training.

Resolution:
A time-based split was used.

The dataset was sorted by:

CustomerID
window_id

The 80th percentile of window_id was used as the split boundary.

Final split boundary:

split_window = 19.0

Training observations:

window_id < 19

Testing observations:

window_id >= 19

Final test set:

3,247 rows

Test window range:

19 to 23

This provides a more realistic evaluation of how the model performs on later customer behavior.


19. BASELINE XGBOOST MODEL

The initial XGBoost model used:

n_estimators = 300
max_depth = 6
learning_rate = 0.1
scale_pos_weight = 1.8362842032651183
eval_metric = logloss
random_state = 42
n_jobs = -1

Initial test results:

Class 0:
Precision = 0.82
Recall = 0.75
F1 = 0.78

Class 1:
Precision = 0.60
Recall = 0.70
F1 = 0.65

Accuracy = 0.73

ROC-AUC = 0.791834351979192

PR-AUC = 0.6606082369775408

Confusion matrix:

[[1568, 534],
 [338, 807]]

The baseline established a reasonable starting point for the behavior-shift detection task.


20. FEATURE IMPORTANCE INVESTIGATION

Problem:
The initial XGBoost model showed that the feature "orders" dominated the feature importance results.

Top feature:

orders = 0.659998

This raised a modeling concern because the project aims to investigate whether behavioral change information contributes meaningfully to detecting customer behavior shifts.

Resolution:
A controlled experiment was performed by removing the orders feature and retraining/evaluating the model.

This was treated as a feature-ablation experiment rather than simply accepting the initial model.


21. ORDERS FEATURE ABLATION

The model was retrained without:

orders

The remaining features included behavioral change variables such as:

orders_change_pct
spend_change_pct
totalQuantity_change_pct
avargeOrderValue_change_pct
unique_products_change_pct
active_days_change_pct
items_per_order_change_pct

The resulting model performance remained very close to the full-feature model.

Results without orders:

Accuracy = 0.74

ROC-AUC = 0.8111588464303074

PR-AUC = 0.6836320406452061

Class 1:

Precision = 0.61
Recall = 0.72
F1 = 0.66

This demonstrated that the model did not depend exclusively on the raw orders feature and that behavioral-change features retained substantial predictive information.


22. FEATURE IMPORTANCE AFTER REMOVING ORDERS

After removing orders, the most important features became:

orders_change_pct = 0.427218
active_days = 0.139432
spend = 0.103380
avargeOrderValue_change_pct = 0.043498
spend_change_pct = 0.038496
avargeOrderValue = 0.029110
line_items = 0.026191
prev_active_days = 0.025782
prev_orders = 0.020099

The strongest feature became:

orders_change_pct

This is particularly relevant to the project's objective because it represents behavioral change rather than simply the customer's current number of orders.


23. HYPERPARAMETER TUNING

RandomizedSearchCV was used to tune the XGBoost model.

Search space:

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

Search configuration:

n_iter = 30
cv = 5
scoring = average_precision
random_state = 42

The optimization metric was Average Precision / PR-AUC because the target is imbalanced and detecting the positive behavior-shift class is more important than relying only on accuracy.


24. BEST XGBOOST PARAMETERS

The first tuned model produced:

n_estimators = 200
max_depth = 6
learning_rate = 0.01
subsample = 1.0
colsample_bytree = 0.9

Best cross-validation Average Precision:

0.7081293994778317

The tuned model improved the test performance compared with the initial baseline.


25. FINAL MODEL AFTER TUNING

The final model was retrained without the raw orders feature and tuned using RandomizedSearchCV.

Best parameters:

n_estimators = 200
max_depth = 6
learning_rate = 0.01
subsample = 1.0
colsample_bytree = 0.9

Final cross-validation Average Precision:

0.7027214623950483

Final test results:

Accuracy = 0.74

ROC-AUC = 0.8111588464303074

PR-AUC = 0.6836320406452061

Class 0:
Precision = 0.83
Recall = 0.74
F1 = 0.79

Class 1:
Precision = 0.61
Recall = 0.72
F1 = 0.66

Confusion matrix:

[[1563, 539],
 [316, 829]]

The final model was selected as the production candidate because it maintains strong discrimination while relying on behavior-aware features rather than the raw orders feature.


26. API THRESHOLD

Problem:
The default classification threshold of 0.50 was not necessarily aligned with the project's objective of detecting behavior shifts.

Resolution:
The API was configured to use a threshold of:

0.30

The model still returns the raw probability, while the API converts the probability into a binary prediction using:

prediction = 1 if probability >= 0.30
prediction = 0 otherwise

This makes the threshold explicit and configurable in the API response.

The API response contains:

prediction
probability
threshold
model_version


27. FINAL API VALIDATION

The FastAPI application was successfully started using Uvicorn.

The API was available locally through:

http://127.0.0.1:8000

The prediction endpoint was:

POST /api/v1/predict

The API correctly rejected incomplete requests with HTTP 422 when required features were missing.

After supplying the complete feature set, the endpoint returned HTTP 200.

Example successful response:

{
  "prediction": 1,
  "probability": 0.3361409306526184,
  "threshold": 0.3,
  "model_version": "v1"
}

This confirms that:

1. FastAPI starts successfully.
2. The versioned XGBoost model can be loaded.
3. The API validates incoming request data.
4. The complete feature set is accepted.
5. The model generates a probability.
6. The configured threshold is applied.
7. The API returns a binary behavior-shift prediction.
8. The model version is exposed in the response.

The final API therefore provides a reproducible inference layer on top of the trained behavior-shift detection model.

Final production artifact:

models/xgboost/v1/model.joblib

Final endpoint:

POST /api/v1/predict

Final threshold:

0.30

Final test PR-AUC:

0.6836320406452061

Final test ROC-AUC:

0.8111588464303074

Final positive-class recall:

0.72

Final positive-class F1:

0.66