# PSSAR Capstone Project — Master Context

## 1. Project Information

**Project:** AI-Based Customer Behavior Shift Detection

**Main idea:**
Build a Machine Learning system that detects whether a customer's behavior has changed significantly over time, rather than directly predicting whether the customer will churn.

The project compares:

1. **Baseline model** → uses static/customer-level features.
2. **Behavior-aware model** → uses static features + temporal behavioral change features.

The goal is to determine whether incorporating behavioral changes improves the detection of customer behavior shifts.

The final deliverable is a **defensible ML model behind a versioned REST API**, following the PSSAR capstone requirements.

---

# 2. Dataset

## Dataset

**Online Retail II — UCI**

The dataset was provided as an Excel workbook with two sheets representing different periods.

### Initial combined dataset

* Rows: **1,067,371**
* Features: **8**

### By period

* 2009–2010: **525,461 rows**
* 2010–2011: **541,910 rows**

### Customer information

* Transactions with Customer ID: **824,364**
* Transactions without Customer ID: **243,007**
* Customer ID coverage: **77.23%**
* Unique customers: **5,942**
* Customers active in multiple years: **2,890**

### Other initial profiling

* Negative quantities: **22,950**
* Zero quantities: **0**
* Negative prices: **0 initially reported**
* Zero prices: **6,202**
* Missing descriptions: **4,382**
* Exact duplicate rows: several counts were investigated during cleaning
* Date range:

  * Minimum: **2009-12-01 07:45:00**
  * Maximum: **2011-12-09 12:50:00**
* Unique dates: **47,635**
* Active customer-months: **26,993**
* Unique months: **25**

---

# 3. Data Cleaning

Negative quantities were investigated and found to be strongly associated with cancellations.

Negative quantity invoices:

* Cancellation invoices (`InvoiceNo` starts with C): **19,493**
* Non-cancellation negative quantity rows: **3,457**

Cleaning decisions included:

* Remove transactions without Customer ID.
* Remove cancellation transactions.
* Remove non-commercial/non-product rows.
* Remove zero-price transactions.
* Remove/handle duplicates according to the project cleaning procedure.
* Ensure quantities and prices used for modeling are valid.

### Important intermediate results

After filtering:

* Customer-level rows: **824,364**
* Rows removed because Customer ID was missing: **243,007**

Cancellation analysis:

* Cancellation rows: **18,744**
* Cancellation invoices: **7,901**
* Purchase rows after cancellation removal: **805,620**

After removing zero-price rows:

* **805,549 rows**
* Removed: **71**

After removing non-commercial transactions:

* Final cleaned transaction rows: **802,904**

Final profiling reported:

* Rows: **802,904**
* Missing Customer IDs: **0**
* Negative quantities: **0**
* Zero quantities: **0**
* Negative prices: **0**
* Zero prices: **0**

Duplicate counts were investigated during cleaning. Different stages showed:

* **26,060 exact duplicate rows** at one stage.
* Another analysis showed **24,652 duplicate groups / 50,712 duplicate rows**.

These numbers should NOT be mixed together; they correspond to different duplicate definitions/stages.

---

# 4. Important Dataset Columns

The original Online Retail II dataset contains columns such as:

* `InvoiceNo`
* `StockCode`
* `Description`
* `Quantity`
* `InvoiceDate`
* `UnitPrice`
* `Customer ID`
* `Country`

### Important clarification about Orders

There is not necessarily a raw column called `Orders`.

`InvoiceNo` represents an invoice/order identifier.

For the behavior-aware model, `InvoiceNo` can potentially be used to derive behavioral features such as:

* Number of unique orders
* Order frequency
* Change in order count
* Average order value
* Changes in purchasing frequency

**Do NOT automatically feed raw `InvoiceNo` into the ML model.**

If the teammate mentions an "Orders" feature, we need to determine whether she means a derived feature such as `order_count` / `number_of_orders`.

This is currently an item to verify.

---

# 5. Project Modeling Strategy

The project is specifically designed to compare:

## Baseline

Uses static/customer-level features.

The purpose is to establish how well customer behavior shifts can be detected without explicitly incorporating temporal behavior-change features.

## Behavior-aware model

Uses:

* Static/customer features
* Temporal behavioral change features

Examples of intended behavior-aware features:

* Login/activity changes
* Usage drop rate
* Session-duration changes
* Activity trends
* Days since last activity
* Transaction/interactions changes
* Order frequency changes
* Other temporal changes derived from customer activity

The central research question is:

> Do behavioral change features improve customer behavior shift detection compared with a static-feature baseline?

---

# 6. Train / Validation / Test Setup

The project uses separate:

* Training set
* Validation set
* Unseen test set

The validation set is used for:

* Model comparison
* Threshold tuning
* Model selection

The test set must remain untouched until the final evaluation.

Important rule:

> The test set must NOT be used for model selection or threshold selection.

---

# 7. Target / Class Imbalance

The target is a binary classification target representing whether a customer experienced a behavior shift.

The target is imbalanced.

Therefore:

**Accuracy is NOT the main model-selection metric.**

The main metric selected is:

> **F1-score**

because F1 balances:

* Precision
* Recall

Additional metrics being tracked:

* Accuracy
* Precision
* Recall
* F1-score
* ROC-AUC
* PR-AUC

---

# 8. Threshold Tuning

The default probability threshold of **0.50** is not assumed to be optimal.

For every model:

1. Generate validation probabilities.
2. Test multiple thresholds.
3. Convert probabilities to predictions using each threshold.
4. Calculate Precision, Recall and F1.
5. Select the threshold with the highest validation F1-score.

Thresholds tested included:

* 0.10
* 0.15
* 0.20
* 0.25
* 0.30
* 0.35
* 0.40
* ...
* 0.95

---

# 9. Three Original Models

The three models originally evaluated using the same behavior-aware features were:

1. **Logistic Regression**
2. **Random Forest**
3. **Gradient Boosting**

The original model comparison was:

| Model               | Best Threshold |  Precision |     Recall |         F1 |    ROC-AUC |     PR-AUC |
| ------------------- | -------------: | ---------: | ---------: | ---------: | ---------: | ---------: |
| Logistic Regression |           0.30 |     0.3935 |     0.5155 | **0.4463** |     0.7794 |     0.4347 |
| Random Forest       |           0.45 |     0.3390 |     0.5606 | **0.4225** |     0.7798 |     0.4140 |
| Gradient Boosting   |       **0.30** | **0.4138** | **0.5746** | **0.4811** | **0.8062** | **0.4638** |

---

# 10. Original Model Selection

Based on the validation results:

**Gradient Boosting was the original finalist.**

Reasons:

* Highest F1-score: **0.4811**
* Highest ROC-AUC: **0.8062**
* Highest PR-AUC: **0.4638**

Selected threshold:

**0.30**

The intended next step was:

> Evaluate the finalized Gradient Boosting model on the unseen test set using threshold 0.30.

---

# 11. XGBoost Experiment

After the three original models, we additionally tested:

**XGBoost**

The XGBoost model was trained using the behavior-aware training features:

```python
xgb_model.fit(
    X_train_behavior_aware,
    y_train
)

print("XGBoost model trained.")
```

Output:

```text
XGBoost model trained.
```

---

# 12. XGBoost Threshold Tuning

XGBoost validation probabilities were evaluated across thresholds.

Some results:

| Threshold |         Precision |     Recall |         F1 |
| --------: | ----------------: | ---------: | ---------: |
|      0.10 |            0.2038 |     0.9042 |     0.3326 |
|      0.15 |            0.2468 |     0.8141 |     0.3788 |
|      0.20 |            0.3031 |     0.7352 |     0.4293 |
|      0.25 |            0.3540 |     0.6423 |     0.4565 |
|      0.30 |            0.4004 |     0.5718 |     0.4710 |
|  **0.35** |        **0.4497** | **0.5042** | **0.4754** |
|      0.40 | continued testing |            |            |
|       ... |               ... |        ... |        ... |
|      0.95 |            1.0000 |     0.0056 |     0.0112 |

### Best XGBoost threshold

```text
Threshold: 0.35
Precision: 0.4497
Recall:    0.5042
F1 Score: 0.4754
```

---

# 13. XGBoost Validation Performance

Final XGBoost validation result:

```text
XGBoost Validation Performance:

Accuracy:  0.8453
Precision: 0.4497
Recall:    0.5042
F1 Score:  0.4754
ROC-AUC:   0.8040
PR-AUC:    0.4590
```

Important:

The XGBoost result uses the tuned threshold:

**0.35**

---

# 14. Current Comparison

Current known validation comparison:

| Model               | Best Threshold |  Precision | Recall |         F1 |    ROC-AUC |     PR-AUC |
| ------------------- | -------------: | ---------: | -----: | ---------: | ---------: | ---------: |
| Logistic Regression |           0.30 |     0.3935 | 0.5155 |     0.4463 |     0.7794 |     0.4347 |
| Random Forest       |           0.45 |     0.3390 | 0.5606 |     0.4225 |     0.7798 |     0.4140 |
| Gradient Boosting   |       **0.30** |     0.4138 | 0.5746 | **0.4811** | **0.8062** | **0.4638** |
| XGBoost             |       **0.35** | **0.4497** | 0.5042 | **0.4754** |     0.8040 |     0.4590 |

### Current interpretation

According to **F1-score**, Gradient Boosting is still slightly better:

* Gradient Boosting F1 = **0.4811**
* XGBoost F1 = **0.4754**

Difference:

**0.0057**

Gradient Boosting also has slightly higher:

* ROC-AUC: 0.8062 vs 0.8040
* PR-AUC: 0.4638 vs 0.4590

However, XGBoost has:

* Higher Precision: **0.4497 vs 0.4138**
* Lower Recall: **0.5042 vs 0.5746**

So XGBoost is NOT currently the winner based on the project's primary metric.

---

# 15. Important Previous XGBoost Error

At one point this code was used:

```python
y_validation_pred_xgb = xgb_model.predict(X_validation)
```

and produced:

```text
NameError: name 'X_validation' is not defined
```

The reason was that the project uses specifically named feature matrices such as:

```python
X_train_behavior_aware
X_validation_behavior_aware
X_test_behavior_aware
```

rather than a generic `X_validation`.

The correct prediction code should therefore use the behavior-aware validation matrix:

```python
y_validation_pred_xgb = xgb_model.predict(X_validation_behavior_aware)
```

when using the default model threshold.

For threshold tuning, use:

```python
y_validation_proba_xgb = xgb_model.predict_proba(
    X_validation_behavior_aware
)[:, 1]
```

---

# 16. Model Results Storage

We started creating a common results list:

```python
model_results = []

model_results.append({
    "model": "XGBoost",
    "accuracy": xgb_accuracy,
    "precision": xgb_precision,
    "recall": xgb_recall,
    "f1": xgb_f1
})
```

The intention is to eventually store the metrics for all models in one DataFrame and compare them.

The final comparison should ideally include:

* Model
* Threshold
* Accuracy
* Precision
* Recall
* F1
* ROC-AUC
* PR-AUC

---

# 17. Important Project Requirement

The project documentation requires:

* Establish a baseline.
* Compare at least **2 models**.
* Select an appropriate metric, not just accuracy.
* Check for data leakage.
* Tune the finalist.
* Evaluate the finalist on unseen test data.
* Build/version the REST API.
* Produce a defensible conclusion-first report.

Therefore, we should NOT jump directly to test evaluation before the model-comparison stage is fully documented.

---

# 18. Current Project Status

### Completed

* Dataset selected.
* Dataset combined.
* Dataset profiled.
* Cleaning performed.
* Customer-level data prepared.
* Behavior-aware features prepared.
* Baseline/behavior-aware modeling structure established.
* Logistic Regression evaluated.
* Random Forest evaluated.
* Gradient Boosting evaluated.
* Threshold tuning performed.
* Gradient Boosting originally selected as finalist.
* XGBoost additionally trained and evaluated.
* XGBoost threshold tuning completed.
* XGBoost validation metrics obtained.

### Current best model

**Gradient Boosting**

Best validation F1:

**0.4811**

Best threshold:

**0.30**

### XGBoost

Best validation F1:

**0.4754**

Best threshold:

**0.35**

Therefore:

> Gradient Boosting remains the current finalist based on F1-score.

---

# 19. What We Should NOT Forget

1. **Do not use accuracy as the main selection criterion.**
2. **F1-score is the primary metric.**
3. Threshold tuning is performed on the **validation set**.
4. The test set must remain unseen until final evaluation.
5. Gradient Boosting currently beats XGBoost by F1:

   * 0.4811 vs 0.4754.
6. XGBoost has better precision but worse recall.
7. Do not feed raw `InvoiceNo` into the model.
8. If someone mentions "Orders", determine whether they mean a derived `order_count` / order-frequency feature.
9. Keep the same feature set when comparing models unless explicitly documenting an experiment.
10. Keep model comparison fair by using the same train/validation split and same behavior-aware features.
11. Do not accidentally use `X_validation`; use the correctly defined behavior-aware validation matrix.
12. The final finalist still needs evaluation on the unseen test set.
13. After final model selection/evaluation, continue toward API/versioning and final report.

---

# 20. Immediate Next Step

Before moving to the test set:

### Step 1

Create one clean comparison DataFrame containing all four models:

* Logistic Regression
* Random Forest
* Gradient Boosting
* XGBoost

with:

* Best threshold
* Accuracy
* Precision
* Recall
* F1
* ROC-AUC
* PR-AUC

### Step 2

Confirm the winner using **F1-score**.

Current winner:

**Gradient Boosting — F1 = 0.4811**

### Step 3

Use Gradient Boosting as the finalist.

### Step 4

Evaluate the finalist on the unseen test set using:

**threshold = 0.30**

### Step 5

Document the final validation vs test performance.

### Step 6

Continue with the remaining capstone requirements:

* final model justification
* API
* model versioning
* final report
* README
* debugging log
