# Debugging Log

## AI-Based Customer Behavior Shift Detection

This document records important technical issues, debugging steps, methodological decisions, and fixes encountered during the development of the **AI-Based Customer Behavior Shift Detection** project.

The purpose of this log is to make the development process traceable and reproducible.

---

# 1. Project Setup

## Issue: Raw Dataset and Generated Files

The raw Online Retail II dataset was large and should not be committed to GitHub.

### Decision

The raw dataset was excluded from version control using `.gitignore`.

Generated and processed datasets are stored separately from the raw data.

### Lesson

Large raw datasets and sensitive/unnecessary generated files should not be committed to the repository.

---

# 2. Dataset Inspection

## Issue: Dataset Stored Across Multiple Excel Sheets

The Online Retail II dataset was provided as an Excel workbook containing multiple sheets.

### Fix

The sheets were inspected and programmatically combined into a single transaction-level dataset.

### Result

The combined raw dataset contained approximately:

* 1,067,371 transactions
* 8 original features

### Lesson

Before feature engineering, the original dataset structure must be understood and standardized.

---

# 3. Dataset Quality Issues

The initial profiling identified several data-quality issues.

### Findings

* Missing Customer IDs
* Missing descriptions
* Duplicate rows
* Negative quantities
* Negative prices
* Zero prices

### Important statistics

* Transactions with Customer ID: 824,364
* Transactions without Customer ID: 243,007
* Customer ID coverage: 77.23%
* Unique customers: 5,942
* Negative quantities: 22,950
* Zero quantities: 0
* Negative prices: 5
* Zero prices: 6,202
* Missing descriptions: 4,382
* Duplicate rows: 34,335

### Decision

The project focuses on identifiable customers because customer-level temporal behavior cannot be reliably constructed without `Customer ID`.

### Lesson

Data-quality problems must be identified before constructing customer-level behavioral features.

---

# 4. Customer-Level Temporal Dataset

## Issue: Transaction-Level Data Was Not Directly Suitable for Behavioral Change Detection

The original data contains individual transactions, while the project requires behavioral changes over time.

### Fix

Transactions were aggregated at the:

```text
Customer × Month
```

level.

### Monthly behavioral features

The following features were created:

* Transaction count
* Total quantity
* Total spending
* Average transaction value
* Unique products
* Previous-period values
* Changes between periods
* Percentage changes
* Months since previous activity

### Result

The processed customer-month dataset contained approximately:

```text
19,651 rows
32 columns
```

### Lesson

Temporal behavior needs to be represented using repeated observations for each customer rather than isolated transactions.

---

# 5. Behavior Shift Definition

## Issue: No Direct Target Variable Existed

The dataset did not contain a label indicating whether a customer experienced a behavior shift.

### Fix

A behavior-shift target was engineered using significant changes across multiple behavioral dimensions.

The target was designed to identify meaningful changes rather than simply predicting customer churn.

### Target

```text
behavior_shift
```

### Classes

```text
0 = No Shift
1 = Behavior Shift
```

### Lesson

When a supervised-learning target does not exist, the target definition must be explicit, reproducible, and justified.

---

# 6. Target Imbalance

The target was imbalanced.

### Training distribution

```text
No Shift:        10,745 (83.74%)
Behavior Shift:   2,087 (16.26%)
```

### Validation distribution

```text
No Shift:         2,198 (86.09%)
Behavior Shift:     355 (13.91%)
```

### Test distribution

```text
No Shift:         3,471 (81.36%)
Behavior Shift:     795 (18.64%)
```

### Decision

Accuracy was not used as the primary model-selection metric.

The project uses:

* Precision
* Recall
* F1-score
* ROC-AUC
* PR-AUC

F1 and PR-AUC are particularly important because the positive class is relatively small.

---

# 7. Leakage Analysis

## Risk

Temporal behavioral prediction can easily suffer from data leakage if future information is used to predict earlier observations.

### Fix

The dataset was split chronologically rather than randomly.

The model only uses information available before or at the prediction point.

### Important principle

Future observations must not influence training or validation predictions.

### Lesson

Temporal ML problems require time-aware splitting and careful feature construction.

---

# 8. Train / Validation / Test Split

The final chronological split was:

### Training

```text
2010-01 → 2011-05
12,832 rows
```

### Validation

```text
2011-06 → 2011-08
2,553 rows
```

### Test

```text
2011-09 → 2011-12
4,266 rows
```

### Decision

The Test set was kept untouched during model comparison and threshold selection.

### Lesson

The validation set is used for model selection and threshold tuning.

The test set is reserved for final evaluation.

---

# 9. Notebook State and Missing Variables

## Error

Several `NameError` exceptions occurred during notebook development.

Example:

```text
NameError: name 'X_train_behavior_aware' is not defined
```

### Cause

The required feature-matrix creation cell had not been executed or the notebook kernel state had been reset.

### Fix

The behavior-aware feature matrices were recreated:

```python
X_train_behavior_aware = train_df[behavior_aware_features].copy()

X_validation_behavior_aware = validation_df[
    behavior_aware_features
].copy()

X_test_behavior_aware = test_df[
    behavior_aware_features
].copy()
```

### Lesson

Jupyter notebooks depend on execution state.

Important preprocessing cells should be organized clearly and rerun after a kernel restart.

---

# 10. Missing `ColumnTransformer` Import

## Error

```text
NameError: name 'ColumnTransformer' is not defined
```

### Cause

`ColumnTransformer` was used before being imported.

### Fix

```python
from sklearn.compose import ColumnTransformer
```

### Lesson

All sklearn components used in preprocessing must be explicitly imported.

---

# 11. Missing `LogisticRegression` Import

## Error

```text
NameError: name 'LogisticRegression' is not defined
```

### Cause

The Logistic Regression class had not been imported.

### Fix

```python
from sklearn.linear_model import LogisticRegression
```

### Lesson

A `NameError` involving an sklearn estimator commonly means the estimator was not imported or the corresponding cell was not executed.

---

# 12. Inconsistent Variable Names

## Error

During model comparison, variables such as:

```text
y_validation_baseline_pred_threshold
y_validation_proba_baseline
```

were referenced even though those exact variables had not been created.

### Cause

Prediction variables were created using different naming conventions.

### Fix

Existing variables were inspected and the actual variable names were reused.

### Lesson

Consistent naming conventions are especially important when comparing several models.

Recommended pattern:

```text
y_validation_<model>_proba
y_validation_<model>_pred
y_validation_<model>_pred_threshold
```

---

# 13. Baseline Logistic Regression

## Initial Result

At the default threshold of `0.50`:

```text
Precision: 0.0000
Recall:    0.0000
F1:        0.0000
ROC-AUC:   0.5763
PR-AUC:    0.1804
```

### Issue

The model predicted almost all observations as the negative class at the default threshold.

### Investigation

Validation probability distributions were examined.

The probabilities were generally below `0.50`.

### Decision

Threshold tuning was introduced rather than relying on the default `0.50` threshold.

---

# 14. Threshold Selection

## Issue

Using a fixed threshold of `0.50` was not appropriate for this imbalanced classification problem.

### Fix

Multiple thresholds were evaluated on the validation set.

The threshold with the highest F1-score was selected.

### Important principle

The threshold must be selected using the Validation set.

It must not be optimized using the Test set.

### Lesson

The classification threshold is a model-decision parameter and can have a large effect on Precision, Recall, and F1.

---

# 15. Behavior-Aware Logistic Regression

The behavior-aware model added previous behavioral information.

### Important features

* Previous transaction count
* Previous total quantity
* Previous total spending
* Previous average transaction value
* Previous unique products
* Months since previous activity

### Validation

Best threshold:

```text
0.30
```

Results:

```text
Precision: 0.3935
Recall:    0.5155
F1:        0.4463
ROC-AUC:   0.7794
PR-AUC:    0.4347
```

### Conclusion

Adding temporal behavioral information substantially improved performance compared with the static baseline.

---

# 16. Test Evaluation of Behavior-Aware Logistic Regression

The selected validation threshold of `0.30` was applied to the untouched Test set.

### Test results

```text
Precision: 0.4395
Recall:    0.4201
F1:        0.4296
ROC-AUC:   0.7474
PR-AUC:    0.4494
```

### Confusion Matrix

```text
[[3045  426]
 [ 461  334]]
```

### Lesson

The Test set provides an estimate of how the selected model generalizes to future unseen observations.

---

# 17. Error Analysis

A dedicated test-results dataset was created.

It contained:

* Actual target
* Predicted target
* Predicted probability
* Error type

### Error types

```text
True Positive
True Negative
False Positive
False Negative
```

### Test distribution

```text
True Negative: 3045 (71.38%)
False Negative: 461 (10.81%)
False Positive: 426 (9.99%)
True Positive: 334 (7.83%)
```

### Observations

False Negatives generally showed substantial changes in transaction quantity and spending.

True Positives also showed strong behavioral changes.

False Positives tended to have longer gaps since previous activity.

### Important methodological note

These are observed associations.

They should not automatically be interpreted as causal relationships.

---

# 18. Random Forest

Random Forest was introduced as a second candidate model.

### Configuration

```python
RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)
```

### Validation at threshold 0.50

```text
Precision: 0.3570
Recall:    0.4817
F1:        0.4101
ROC-AUC:   0.7798
PR-AUC:    0.4140
```

### Best threshold

```text
0.45
```

### Final validation metrics

```text
Precision: 0.3390
Recall:    0.5606
F1:        0.4225
ROC-AUC:   0.7798
PR-AUC:    0.4140
```

### Conclusion

Random Forest improved recall but did not outperform Behavior-Aware Logistic Regression in F1 or PR-AUC.

---

# 19. Gradient Boosting

Gradient Boosting was introduced as the third candidate model.

### Configuration

```python
GradientBoostingClassifier(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=3,
    random_state=42
)
```

### Validation at threshold 0.50

```text
Precision: 0.5784
Recall:    0.3014
F1:        0.3963
ROC-AUC:   0.8062
PR-AUC:    0.4638
```

### Threshold tuning

The best validation threshold was:

```text
0.30
```

### Final validation metrics

```text
Precision: 0.4138
Recall:    0.5746
F1:        0.4811
ROC-AUC:   0.8062
PR-AUC:    0.4638
```

### Confusion Matrix

```text
[[1909  289]
 [ 151  204]]
```

### Conclusion

Gradient Boosting became the current finalist because it achieved the strongest overall validation performance.

---

# 20. Current Model Comparison

| Model                   | Threshold | Precision | Recall |         F1 |    ROC-AUC |     PR-AUC |
| ----------------------- | --------: | --------: | -----: | ---------: | ---------: | ---------: |
| Behavior-Aware Logistic |      0.30 |    0.3935 | 0.5155 |     0.4463 |     0.7794 |     0.4347 |
| Random Forest           |      0.45 |    0.3390 | 0.5606 |     0.4225 |     0.7798 |     0.4140 |
| Gradient Boosting       |      0.30 |    0.4138 | 0.5746 | **0.4811** | **0.8062** | **0.4638** |

### Current decision

Gradient Boosting is the finalist.

The current validation threshold is:

```text
0.30
```

### Important

This threshold is NOT yet considered permanently final.

It may change after hyperparameter tuning.

---

# 21. Threshold 0.30 vs 0.50

For Gradient Boosting:

| Threshold | Precision | Recall |         F1 |
| --------: | --------: | -----: | ---------: |
|      0.30 |    0.4138 | 0.5746 | **0.4811** |
|      0.50 |    0.5784 | 0.3014 |     0.3963 |

### Interpretation

A threshold of `0.50` is more conservative.

It produces higher Precision but misses more actual behavior shifts.

A threshold of `0.30` produces higher Recall and the best F1-score.

### Decision

Because the project aims to detect behavior shifts and F1 is the main threshold-selection criterion, `0.30` is currently preferred.

---

# 22. Test Set Protection

The Test set must not be repeatedly used during:

* model selection
* threshold selection
* hyperparameter tuning
* feature selection

### Reason

Repeated use of the Test set can cause indirect overfitting to the test data and produce overly optimistic final results.

### Rule

The Test set should only be used after the final model and threshold are selected using the Training and Validation sets.

---

# 23. Current Project Status

Completed:

* Project setup
* Dataset acquisition
* Dataset inspection
* Dataset profiling
* Data cleaning
* Customer-level temporal dataset
* Behavior-shift target definition
* Temporal feature engineering
* Leakage-aware splitting
* Baseline Logistic Regression
* Behavior-aware Logistic Regression
* Random Forest
* Gradient Boosting
* Threshold selection
* Model comparison
* Initial error analysis
* Behavior-aware model Test evaluation

Current stage:

```text
Gradient Boosting → Finalist
```

---

# 24. Next Steps

## Step 1 — Hyperparameter Tuning

Tune the Gradient Boosting finalist using the training/validation workflow.

Potential parameters:

* `n_estimators`
* `learning_rate`
* `max_depth`
* `min_samples_split`
* `min_samples_leaf`
* `subsample`

The validation set will be used to evaluate the tuned candidate.

---

## Step 2 — Final Threshold Selection

After tuning, evaluate thresholds again.

Select the threshold using Validation F1.

---

## Step 3 — Final Test Evaluation

Only after the model and threshold are finalized:

* Generate Test probabilities.
* Apply the selected threshold.
* Calculate Precision.
* Calculate Recall.
* Calculate F1.
* Calculate ROC-AUC.
* Calculate PR-AUC.
* Generate confusion matrix.
* Generate classification report.

---

## Step 4 — Final Error Analysis

Analyze the final model's:

* False Positives
* False Negatives
* True Positives
* Important behavioral patterns

---

## Step 5 — Model Interpretation

Analyze feature importance and determine which behavioral features contribute most to detecting shifts.

---

## Step 6 — Model Versioning

Save the selected model as a versioned artifact.

Example:

```text
v1 = baseline model
v2 = behavior-aware finalist/final model
```

Store:

* model
* preprocessing
* threshold
* feature list
* model metadata
* training information

---

## Step 7 — FastAPI

Expose the final model through:

```text
/health
/predict
/metadata
/versions
```

The API must validate inputs and return HTTP `422` for invalid inputs.

---

## Step 8 — Testing

Add tests for:

* preprocessing
* model loading
* prediction
* threshold application
* API endpoints
* invalid inputs
* health endpoint

---

## Step 9 — Documentation

Update:

* README
* methodology
* model comparison
* final results
* reproducibility instructions
* API documentation
* project conclusion

---

# 25. General Lessons Learned

### Lesson 1

A high Accuracy score does not necessarily mean a good classifier when the target is imbalanced.

### Lesson 2

Temporal ML problems require strict leakage prevention.

### Lesson 3

The classification threshold is separate from the model itself and can significantly change Precision, Recall, and F1.

### Lesson 4

Threshold selection must be performed on Validation data, not Test data.

### Lesson 5

Comparing multiple models using the same split and metrics makes the comparison more defensible.

### Lesson 6

Error analysis helps explain where the model succeeds and fails.

### Lesson 7

Notebook execution order matters because variables depend on previous cells.

### Lesson 8

The final Test set should remain untouched until the final evaluation.

---

# 26. Final Debugging Principle

When an error occurs:

1. Read the full traceback.
2. Identify the exact failing variable/function/class.
3. Check whether it was imported.
4. Check whether the required previous cell was executed.
5. Check variable names for consistency.
6. Fix the smallest necessary part.
7. Re-run the affected cell.
8. Verify the output before continuing.

The goal is not only to make the code run, but to understand why the error happened and why the fix works.

# Debugging Log

## 03 - Temporal Analysis & Feature Engineering

### 1. Cleaned Dataset

After data cleaning and duplicate removal:

* Rows: **776,844**
* Columns: **8**
* Missing values: **0**
* Negative quantities: **0**
* Zero quantities: **0**
* Negative prices: **0**
* Zero prices: **0**
* Exact duplicate rows: **0**

Date range:

* Minimum date: **2009-12-01 07:45:00**
* Maximum date: **2011-12-09 12:50:00**
* Number of months: **25**

A `Month` column was added to support customer-month temporal aggregation.

---

### 2. Transaction-Level Feature

A `TotalPrice` feature was created:

```text
TotalPrice = Quantity × Price
```

Validation showed:

* Negative `TotalPrice`: 0
* Zero `TotalPrice`: 0

The cleaned transaction-level dataset contained:

* Rows: **776,844**
* Columns: **10** after adding `TotalPrice` and `Month`

---

### 3. Customer-Month Aggregation

Transaction-level data was aggregated into customer-month observations.

The following behavioral features were created:

* `transaction_count`
* `total_quantity`
* `total_spending`
* `average_transaction_value`
* `unique_products`

Final customer-month dataset:

* Customer-month observations: **25,504**
* Unique customers: **5,853**
* Unique months: **25**
* Duplicate customer-month pairs: **0**
* Missing values: **0**

---

### 4. Previous-Period Features

Customer-month observations were sorted by customer and month.

Previous behavioral values were created using the customer's previous observed month:

* `previous_transaction_count`
* `previous_total_quantity`
* `previous_total_spending`
* `previous_average_transaction_value`
* `previous_unique_products`

A temporal gap feature was also created:

* `months_since_previous`

There were:

* Customer-month observations with a previous month: **19,651**
* Unique customers with a previous month: **4,094**

For consecutive months:

* Consecutive customer-month observations: **9,330**
* Unique customers with consecutive months: **2,425**

---

### 5. Behavioral Change Features

Absolute changes between the current and previous observations were calculated:

* `change_transaction_count`
* `change_total_quantity`
* `change_total_spending`
* `change_average_transaction_value`
* `change_unique_products`

Percentage changes were then calculated:

* `pct_change_transaction_count`
* `pct_change_total_quantity`
* `pct_change_total_spending`
* `pct_change_average_transaction_value`
* `pct_change_unique_products`

Extreme percentage changes were inspected. Large values were observed because percentage change can become very large when the previous value is small.

The 1st and 99th percentiles were inspected to understand the distribution.

---

### 6. Behavioral Shift Threshold

A percentage-change threshold was used to identify large behavioral changes.

The main threshold selected for the core behavioral dimensions was:

```text
100%
```

The core behavioral dimensions were:

* `total_quantity`
* `total_spending`
* `average_transaction_value`
* `unique_products`

The number of core dimensions exceeding the threshold was counted using:

```python
core_large_change_count
```

The distribution was:

| Number of large changes | Observations | Percentage |
| ----------------------: | -----------: | ---------: |
|                       0 |       13,513 |     68.76% |
|                       1 |        2,901 |     14.76% |
|                       2 |        1,340 |      6.82% |
|                       3 |        1,790 |      9.11% |
|                       4 |          107 |      0.54% |

The target variable `behavior_shift` was then created from the behavioral shift criteria.

Final target distribution:

* No shift (`0`): **16,414 (83.53%)**
* Shift (`1`): **3,237 (16.47%)**

Overall shift rate:

**16.47%**

---

### 7. Temporal Shift Analysis

Shift rates were examined across months.

Results:

* Minimum monthly shift rate: **7.17%**
* Maximum monthly shift rate: **23.99%**
* Average monthly shift rate: **15.99%**

The shift rate varied over time, with higher rates observed in some periods such as September-November 2010 and September-November 2011.

---

### 8. Final Temporal Dataset

The final dataset used for modeling contains:

* Rows: **19,651**
* Columns: **32**

Saved to:

```text
../data/processed/behavior_change_dataset.csv
```

---

### 9. Feature Sets

#### Baseline Features

The baseline model uses historical customer-level information:

```python
[
    "historical_active_months",
    "historical_transactions",
    "historical_spending"
]
```

#### Behavior-Aware Features

The behavior-aware model uses the baseline features plus previous-period behavioral information:

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

Target:

```text
behavior_shift
```

---

### 10. Train / Validation / Test Split

A chronological split was used to avoid temporal leakage.

| Dataset    | Period             |   Rows |
| ---------- | ------------------ | -----: |
| Train      | 2010-01 to 2011-05 | 12,832 |
| Validation | 2011-06 to 2011-08 |  2,553 |
| Test       | 2011-09 to 2011-12 |  4,266 |

Target distributions:

* Train: **83.74% no shift / 16.26% shift**
* Validation: **86.09% no shift / 13.91% shift**
* Test: **81.36% no shift / 18.64% shift**

The target remains imbalanced across all three splits.

---

### 11. Feature Distribution and Skewness

Feature distributions were inspected before modeling.

Strong right-skew was observed, especially in spending, quantity, and transaction-related features.

Baseline skewness included:

* `historical_active_months`: 1.35
* `historical_transactions`: 6.37
* `historical_spending`: 13.41

Behavior-aware features showed even stronger skewness in some variables, including:

* `previous_total_quantity`: 30.10
* `previous_average_transaction_value`: 17.45
* `previous_total_spending`: 13.09
* `previous_transaction_count`: 8.19

A skewness threshold of `1.0` was used as a diagnostic to identify highly right-skewed features.

The final log-transformation candidates were explicitly defined as:

#### Baseline

```python
[
    "historical_transactions",
    "historical_spending"
]
```

#### Behavior-Aware

```python
[
    "historical_transactions",
    "historical_spending",
    "previous_transaction_count",
    "previous_total_quantity",
    "previous_total_spending",
    "previous_average_transaction_value",
    "previous_unique_products"
]
```

`historical_active_months` and `months_since_previous` were not included in the final log-transformation lists because they are small count/gap variables with a more constrained range.

---

### 12. Data Leakage Considerations

The following columns were used to construct the target and therefore are not used directly as model features:

* `change_*`
* `pct_change_*`
* `behavior_shift_candidate`
* `core_large_change_count`
* `core_behavior_shift_candidate`

This prevents the model from directly receiving information that was used to define the target.

Preprocessing and transformations should be fitted on the training data only and then applied to validation and test data.

---

### 13. Current Status

Completed:

* Data cleaning
* Temporal aggregation
* Customer-month feature engineering
* Previous-period features
* Behavioral change features
* Behavioral shift target construction
* Temporal train/validation/test split
* Baseline feature definition
* Behavior-aware feature definition
* Feature distribution analysis
* Skewness analysis
* Log-transformation feature selection

Next step:

**Train and evaluate the baseline machine learning model.**
