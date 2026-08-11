# Debugging Log

## AI-Based Customer Behavior Shift Detection

This document records the main technical issues, methodological decisions, debugging findings, and model-development decisions made during the development of the **AI-Based Customer Behavior Shift Detection** project.

The purpose of this log is to keep the project development process **traceable, reproducible, and methodologically defensible**.

---

# 1. Dataset Preparation

## Raw Dataset Handling

The project uses the **Online Retail II** dataset.

The raw dataset was excluded from version control because of its size and because raw data is not required in the GitHub repository for reproducibility.

Generated and processed datasets are stored separately.

### Decision

The raw dataset was added to `.gitignore`.

### Lesson

Raw datasets and generated artifacts should be separated from source code and should not be unnecessarily committed to version control.

---

# 2. Dataset Inspection and Cleaning

The original dataset contained multiple data-quality issues, including:

* Missing Customer IDs
* Missing descriptions
* Duplicate records
* Negative quantities
* Negative prices
* Zero prices
* Cancellation transactions
* Non-commercial transactions

The dataset was inspected before feature engineering to identify and understand these issues.

### Key observations

* Original combined dataset: **1,067,371 rows**
* Transactions with Customer ID: **824,364**
* Transactions without Customer ID: **243,007**
* Unique customers: **5,942**
* Negative quantities were identified and investigated as part of cancellation handling.

### Decision

Customer-level modeling was restricted to transactions with valid `Customer ID` values because customer behavioral history cannot be reliably constructed without a customer identifier.

Cancellation and invalid/non-commercial transactions were removed according to the project's cleaning rules.

### Lesson

Data cleaning must be completed before constructing temporal customer features because invalid transactions can directly affect behavioral measurements.

---

# 3. Customer-Month Temporal Dataset

## Issue

The original dataset was transaction-level, while the project objective requires detecting changes in customer behavior over time.

### Fix

Transactions were aggregated at the:

```text
Customer × Month
```

level.

The following monthly behavioral features were created:

* `transaction_count`
* `total_quantity`
* `total_spending`
* `average_transaction_value`
* `unique_products`

The final temporal dataset used for modeling contained:

```text
19,651 rows
32 columns
```

### Lesson

Customer behavior is better represented through repeated customer-period observations than isolated transactions.

---

# 4. Previous-Period Behavioral Features

Previous observed customer behavior was calculated using chronological customer histories.

The following features were created:

```text
previous_transaction_count
previous_total_quantity
previous_total_spending
previous_average_transaction_value
previous_unique_products
months_since_previous
```

These features provide information about the customer's recent behavioral history without directly using future observations.

### Decision

Previous-period features were included in the behavior-aware model to test whether temporal information improves behavior-shift detection.

---

# 5. Behavioral Change Features and Target Construction

## Issue

The original dataset did not contain a target variable indicating whether a customer experienced a behavior shift.

### Fix

Behavioral change features were calculated by comparing current customer behavior with previous observed behavior.

Absolute changes included:

```text
change_transaction_count
change_total_quantity
change_total_spending
change_average_transaction_value
change_unique_products
```

Percentage changes included:

```text
pct_change_transaction_count
pct_change_total_quantity
pct_change_total_spending
pct_change_average_transaction_value
pct_change_unique_products
```

A core behavioral-change criterion was then used to construct the target:

```text
behavior_shift
```

with:

```text
0 = No Behavior Shift
1 = Behavior Shift
```

### Important leakage consideration

Features directly used to construct the target were not used as model inputs.

The following groups were excluded from model features:

```text
change_*
pct_change_*
behavior_shift_candidate
core_large_change_count
core_behavior_shift_candidate
```

### Lesson

When a supervised-learning target is engineered from behavioral rules, the target-defining variables must not be passed directly to the model.

---

# 6. Temporal Train / Validation / Test Split

## Issue

Random splitting would allow observations from different time periods to appear across training and evaluation sets, which is inappropriate for this temporal prediction problem.

### Fix

A chronological split was used.

| Dataset    | Period            |   Rows |
| ---------- | ----------------- | -----: |
| Train      | 2010-01 → 2011-05 | 12,832 |
| Validation | 2011-06 → 2011-08 |  2,553 |
| Test       | 2011-09 → 2011-12 |  4,266 |

### Decision

The Test set was kept separate from model selection and threshold selection.

### Lesson

Temporal problems require time-aware evaluation to reduce the risk of temporal leakage.

---

# 7. Target Imbalance

The target is moderately imbalanced.

### Training distribution

```text
No Shift:         10,745 (83.74%)
Behavior Shift:    2,087 (16.26%)
```

### Validation distribution

```text
No Shift:          2,198 (86.09%)
Behavior Shift:      355 (13.91%)
```

### Test distribution

```text
No Shift:          3,471 (81.36%)
Behavior Shift:      795 (18.64%)
```

### Decision

Accuracy was not used as the primary model-selection metric.

The main evaluation metrics were:

* Precision
* Recall
* F1-score
* ROC-AUC
* PR-AUC

F1-score was used for classification-threshold selection.

---

# 8. Feature Sets

Two feature sets were defined to evaluate whether behavioral information improves detection.

## Baseline Features

```python
[
    "historical_active_months",
    "historical_transactions",
    "historical_spending"
]
```

The baseline represents static/historical customer information.

## Behavior-Aware Features

```python
[
    "historical_active_months",
    "historical_transactions",
    "historical_spending",
    "previous_transaction_count",
    "previous_total_quantity",
    "previous_total_spending",
    "previous_average_transaction_value",
    "previous_unique_products",
    "months_since_previous"
]
```

The behavior-aware model extends the baseline with recent behavioral information.

---

# 9. Baseline Logistic Regression

The baseline Logistic Regression model was trained using the baseline feature set.

At the default classification threshold of `0.50`, the model produced:

```text
Precision: 0.0000
Recall:    0.0000
F1:        0.0000
ROC-AUC:   0.5763
PR-AUC:    0.1804
```

## Issue

The model probabilities were generally below `0.50`, causing almost all validation observations to be classified as the negative class.

### Fix

Classification thresholds were evaluated on the Validation set.

The best threshold by F1-score was:

```text
0.20
```

### Validation performance

```text
Precision: 0.1887
Recall:    0.4535
F1:        0.2666
ROC-AUC:   0.5763
PR-AUC:    0.1804
```

### Lesson

The default threshold of `0.50` is not necessarily appropriate for an imbalanced classification problem.

---

# 10. Behavior-Aware Logistic Regression

The behavior-aware Logistic Regression model was trained using the nine behavior-aware features.

The best validation threshold was:

```text
0.30
```

### Validation performance

```text
Precision: 0.3935
Recall:    0.5155
F1:        0.4463
ROC-AUC:   0.7794
PR-AUC:    0.4347
```

### Conclusion

Adding recent behavioral information substantially improved the model compared with the static baseline.

---

# 11. Random Forest

Random Forest was introduced as a nonlinear candidate model.

The model was evaluated using the same temporal split and validation-based threshold-selection procedure.

The best validation threshold was:

```text
0.45
```

### Validation performance

```text
Precision: 0.3390
Recall:    0.5606
F1:        0.4225
ROC-AUC:   0.7798
PR-AUC:    0.4140
```

### Conclusion

Random Forest achieved higher recall than the behavior-aware Logistic Regression model, but its F1-score and PR-AUC were lower.

Therefore, it was not selected as the final model.

---

# 12. Original XGBoost Model

XGBoost was introduced as an additional nonlinear candidate model.

The model was trained using the behavior-aware feature set.

### Validation threshold

The best threshold was:

```text
0.30
```

### Validation performance

```text
Precision: 0.3985
Recall:    0.5803
F1:        0.4725
ROC-AUC:   0.8022
PR-AUC:    0.4562
```

XGBoost achieved the strongest validation performance among the initial candidate models.

### Feature importance

The most important features were:

| Feature                      | Importance |
| ---------------------------- | ---------: |
| `previous_total_spending`    |     0.2550 |
| `previous_unique_products`   |     0.1815 |
| `previous_total_quantity`    |     0.1399 |
| `historical_spending`        |     0.0949 |
| `previous_transaction_count` |     0.0835 |

### Interpretation

Recent customer behavior, particularly previous spending, product diversity, and quantity, contributed strongly to the model's predictions.

These are model associations and should not be interpreted as causal effects.

---

# 13. Model Comparison

The initial validation comparison was:

| Model                              | Threshold | Precision | Recall |         F1 |    ROC-AUC |     PR-AUC |
| ---------------------------------- | --------: | --------: | -----: | ---------: | ---------: | ---------: |
| Baseline Logistic Regression       |      0.20 |    0.1887 | 0.4535 |     0.2666 |     0.5763 |     0.1804 |
| Behavior-Aware Logistic Regression |      0.30 |    0.3935 | 0.5155 |     0.4463 |     0.7794 |     0.4347 |
| Random Forest                      |      0.45 |    0.3390 | 0.5606 |     0.4225 |     0.7798 |     0.4140 |
| XGBoost                            |      0.30 |    0.3985 | 0.5803 | **0.4725** | **0.8022** | **0.4562** |

### Decision

XGBoost was selected as the leading candidate because it achieved the strongest validation F1-score, ROC-AUC, and PR-AUC among the initial models.

---

# 14. XGBoost Hyperparameter Tuning

## Objective

Hyperparameter tuning was performed to determine whether the original XGBoost configuration could be improved.

The search was performed using 3-fold cross-validation with F1-score as the optimization metric.

### Search space

```text
n_estimators: [100, 200, 300]
max_depth: [3, 5, 7]
learning_rate: [0.03, 0.05, 0.1]
subsample: [0.8, 1.0]
colsample_bytree: [0.8, 1.0]
```

The search evaluated:

```text
20 candidate configurations
60 total cross-validation fits
```

### Best configuration

```text
n_estimators = 300
max_depth = 7
learning_rate = 0.10
subsample = 0.8
colsample_bytree = 1.0
```

### Cross-validation result

```text
Best cross-validation F1: 0.3509
```

The tuned XGBoost model was then evaluated on the Validation set using multiple classification thresholds.

### Tuned validation threshold results

| Threshold |  Precision |     Recall |         F1 |
| --------: | ---------: | ---------: | ---------: |
|      0.10 |     0.2477 |     0.7549 |     0.3730 |
|      0.15 |     0.2825 |     0.6732 |     0.3980 |
|      0.20 |     0.3138 |     0.6169 |     0.4160 |
|      0.25 |     0.3379 |     0.5606 |     0.4216 |
|  **0.30** | **0.3690** | **0.5239** | **0.4331** |
|      0.35 |     0.3939 |     0.4704 |     0.4288 |
|      0.40 |     0.4107 |     0.4338 |     0.4219 |
|      0.45 |     0.4299 |     0.3972 |     0.4129 |
|      0.50 |     0.4460 |     0.3493 |     0.3918 |

### Comparison with original XGBoost

```text
Original XGBoost:
Validation F1 = 0.4725
Threshold = 0.30

Tuned XGBoost:
Validation F1 = 0.4331
Threshold = 0.30
```

### Decision

Hyperparameter tuning did not improve validation performance.

Therefore:

```text
Final model: Original XGBoost
Final threshold: 0.30
```

The tuned configuration was not adopted.

### Lesson

Hyperparameter tuning is not guaranteed to improve model performance. A tuned model should only replace the original model when it demonstrates better performance on the validation data under the same evaluation procedure.

---

# 15. Final XGBoost Evaluation

After model selection, the untouched Test set was used for final evaluation.

The selected model was:

```text
Original XGBoost
```

with:

```text
Classification threshold = 0.30
```

### Test performance

```text
Precision: 0.4681
Recall:    0.4805
F1:        0.4742
ROC-AUC:   0.7746
PR-AUC:    0.4790
```

### Test confusion matrix

```text
[[3037  434]
 [ 413  382]]
```

This corresponds to:

```text
True Negatives: 3037
False Positives: 434
False Negatives: 413
True Positives: 382
```

### Interpretation

The final model detects a meaningful portion of behavior-shift cases while maintaining substantially better precision than the baseline model.

---

# 16. Final Model vs Baseline

| Model                        |  Precision |     Recall |         F1 |    ROC-AUC |     PR-AUC |
| ---------------------------- | ---------: | ---------: | ---------: | ---------: | ---------: |
| Baseline Logistic Regression |     0.1887 |     0.4535 |     0.2666 |     0.5763 |     0.1804 |
| Final XGBoost                | **0.4681** | **0.4805** | **0.4742** | **0.7746** | **0.4790** |

### Improvement

Compared with the baseline, the final XGBoost model achieved:

* substantially higher Precision
* higher F1-score
* substantially higher ROC-AUC
* substantially higher PR-AUC

This supports the project's main hypothesis that incorporating behavioral information can improve customer behavior-shift detection.

---

# 17. Test Set Protection

The Test set was reserved for final evaluation.

It was not used to:

* select the model
* select the classification threshold
* tune hyperparameters
* compare tuning configurations

The classification threshold was selected using the Validation set and then applied unchanged to the Test set.

### Lesson

Keeping the Test set untouched until final evaluation provides a more reliable estimate of model generalization.

---

# 18. Current Project Status

The core machine-learning pipeline and model-serving components have been completed.

### Completed

* Dataset inspection and cleaning
* Customer-month temporal aggregation
* Historical and previous-period behavioral features
* Behavior-shift target construction
* Leakage analysis and feature exclusion
* Chronological train/validation/test split
* Baseline Logistic Regression
* Behavior-aware Logistic Regression
* Random Forest
* XGBoost
* Classification-threshold evaluation
* Model comparison
* XGBoost hyperparameter tuning
* Final model selection
* Final Test evaluation
* Final model versioning
* FastAPI model-serving API
* API request/response schemas
* Automated API tests
* Dependency and repository configuration

### Final Model

```text
Model: XGBoost
Threshold: 0.30
Version: v1
```

### Final Test Performance

```text
Precision: 0.4681
Recall:    0.4805
F1-score:  0.4742
ROC-AUC:   0.7746
PR-AUC:    0.4790
```

The final model was selected based on validation performance and evaluated once on the untouched Test set.

---

# 19. API Validation

The final XGBoost model was exposed through a versioned FastAPI REST API.

### Implemented Endpoints

```text
GET  /health
GET  /metadata
GET  /versions
POST /predict
```

The `/predict` endpoint accepts the nine behavior-aware features and returns:

```text
prediction
probability
threshold
model_version
```

### API Verification

A real Test-set observation was used to validate the API prediction against the notebook prediction.

The results matched:

```text
Notebook probability: 0.14841708540916443
API probability:      0.14841708540916443

Notebook prediction:  0
API prediction:       0
```

This confirmed that the deployed model produces the same prediction as the saved model used during evaluation.

### Input Validation

The API was also tested against invalid requests, including:

* Missing required features
* Invalid data types

FastAPI correctly returned HTTP `422` validation responses.

---

# 20. Automated API Testing

Automated tests were added to verify the main API functionality.

The test suite covers:

```text
Health endpoint
Metadata endpoint
Versions endpoint
Valid prediction
Missing prediction feature
Invalid prediction input type
```

Test execution result:

```text
6 passed
```

This provides automated verification of the main API behavior and input-validation logic.

---

# 21. Final Error Analysis

The final model should be further examined through its prediction errors.

The analysis should focus on:

* False Positives
* False Negatives
* True Positives
* True Negatives

The purpose is to determine whether specific customer behavioral patterns are associated with incorrect predictions and whether the model has systematic weaknesses.

Error analysis should be performed on the Test set without changing the selected model or threshold based on those results.

---

# 22. Model Interpretation

Model interpretation will be used to understand which behavioral features contribute most strongly to the final XGBoost predictions.

The interpretation should focus on the relationship between the model's predictions and features such as:

```text
previous_total_spending
previous_unique_products
previous_total_quantity
historical_spending
previous_transaction_count
```

Feature importance and SHAP-based analysis, if included, should be interpreted as model-level associations rather than causal relationships.

---

# 23. Documentation

The final project documentation should clearly describe:

* Project objective
* Dataset and preprocessing
* Feature engineering
* Target construction
* Leakage prevention
* Temporal evaluation strategy
* Baseline and candidate models
* Model comparison
* Threshold selection
* Hyperparameter tuning
* Final Test results
* API usage
* Testing
* Reproducibility instructions
* Project limitations
* Final conclusion

The documentation should remain consistent with the final implementation and reported evaluation results.

---

# 24. Reproducibility

The project maintains reproducibility through:

* Version-controlled source code
* A documented feature-generation pipeline
* Versioned model artifacts
* Explicit classification threshold
* Saved model metadata
* API schemas
* Automated API tests
* Dependency specification
* Git ignore rules for local and generated artifacts

The raw dataset is intentionally excluded from version control.

---

# 25. Final Project Conclusion

The project investigated whether incorporating temporal customer behavior can improve the detection of significant customer behavior shifts compared with a static historical baseline.

The final XGBoost model achieved:

```text
F1-score:  0.4742
ROC-AUC:   0.7746
PR-AUC:    0.4790
```

compared with the baseline Logistic Regression:

```text
F1-score:  0.2666
ROC-AUC:   0.5763
PR-AUC:    0.1804
```

The results support the project's main hypothesis: **behavior-aware features provide substantially more useful predictive information for customer behavior-shift detection than the static baseline alone.**

The final model is versioned as `v1`, uses a classification threshold of `0.30`, and is exposed through a tested FastAPI REST API.

The project should be considered complete after finalizing model interpretation, error analysis, and the remaining project documentation.
