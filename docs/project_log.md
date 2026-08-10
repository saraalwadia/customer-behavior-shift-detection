# Project Log

## Project: AI-Based Customer Behavior Shift Detection

---

## 1. Data Profiling

### Objective

The objective of this stage was to understand the structure, quality, completeness, temporal coverage, customer coverage, and potential anomalies in the Online Retail II dataset before performing data cleaning and feature engineering.

---

### Dataset Source

The project uses the **Online Retail II** dataset from the UCI Machine Learning Repository.

The original workbook contains two sheets:

* `Year 2009-2010`
* `Year 2010-2011`

Both sheets contain the same 8 original features:

* Invoice
* StockCode
* Description
* Quantity
* InvoiceDate
* Price
* Customer ID
* Country

---

### Dataset Structure

The two sheets were loaded and combined programmatically.

#### Year 2009-2010

* Rows: 525,461
* Columns: 8

#### Year 2010-2011

* Rows: 541,910
* Columns: 8

#### Combined Dataset

* Rows: 1,067,371
* Columns: 8

The combined raw dataset was saved as:

`data/raw/online_retail_II.csv`

The raw dataset is kept separate from processed data.

---

## 2. Missing Values

Missing values were identified in two columns:

| Column      | Missing Rows | Missing Rate |
| ----------- | -----------: | -----------: |
| Customer ID |      243,007 |       22.77% |
| Description |        4,382 |        0.41% |

Customer ID is important for this project because the target is based on changes in individual customer behavior over time.

Transactions without Customer ID cannot be assigned to a specific customer and therefore cannot contribute to customer-level behavioral features.

Missing Description values are less critical because Description is not a primary feature used by the final customer-level modeling pipeline.

---

## 3. Duplicate Records

The combined dataset contains:

* Total duplicate rows: 34,335

Duplicates were also examined separately for each original sheet:

* Year 2009-2010: 6,865 duplicate rows
* Year 2010-2011: 5,268 duplicate rows

Rows duplicated across the two sheets:

* 23,221 rows

Unique rows duplicated across sheets:

* 22,202

These results indicate that duplication exists both within individual sheets and across the combined dataset and must be considered during data cleaning.

The raw dataset will not be modified directly. Any duplicate removal will be performed on a processed dataset and documented.

---

## 4. Customer Coverage

The combined dataset contains:

* Total transaction rows: 1,067,371
* Transactions with Customer ID: 824,364
* Transactions without Customer ID: 243,007
* Customer ID coverage: 77.23%

There are:

* 5,942 unique customers with Customer ID
* 5,796 customers with multiple transactions
* 2,890 customers active across multiple years

This confirms that the dataset contains sufficient repeated customer activity for temporal behavioral analysis.

---

## 5. Customer Transaction Distribution

The number of transactions per customer was examined.

Results:

* Mean: 138.74 transactions
* Median: 53 transactions
* Maximum: 13,097 transactions
* Minimum: 1 transaction

The distribution is highly uneven, with some customers having substantially more transactions than others.

This is important because customer activity is not uniformly distributed.

---

## 6. Customer Monthly Activity

The dataset contains:

* Unique customers: 5,942
* Unique months: 25
* Active customer-month observations: 26,993

Not every customer is active in every month.

Therefore, the number of observed customer-month combinations is much smaller than the theoretical:

`5,942 × 25 = 148,550`

This supports the decision to construct a customer-month behavioral dataset rather than treating individual transaction rows as the main modeling observations.

---

## 7. Transaction Quantity Analysis

Negative quantities:

* 22,950 rows

Zero quantities:

* 0 rows

Negative quantities were investigated to determine whether they represented cancellations or other business events.

Among negative-quantity transactions:

* 19,493 were associated with cancellation-style invoice numbers beginning with `C`.
* 3,457 negative-quantity rows were not associated with cancellation invoice numbers.

The non-cancellation negative-quantity records were inspected and included descriptions such as:

* `short`
* `lost`
* `damages`
* `sold as gold`
* `invcd as ...`

These records appear to represent operational adjustments, damaged/lost goods, or other non-standard transactions.

This finding will be considered during the data-cleaning stage.

---

## 8. Cancellation Analysis

Cancellation records were explicitly investigated.

Results:

* Cancellation rows: 19,494
* Cancellation invoices: 8,292
* Cancellation invoices with positive quantity: 1

The large majority of negative-quantity cancellation records therefore follow the expected pattern of representing returned/cancelled quantities.

---

## 9. Price Analysis

Negative-price rows:

* 5

All five negative-price records were manually inspected.

They had:

* Description: `Adjust bad debt`
* Quantity: 1
* Customer ID: missing
* Negative prices

These records represent financial adjustments rather than normal customer purchases.

Because they do not represent identifiable customer purchasing behavior and have no Customer ID, they should not contribute to customer-level behavioral modeling.

Zero-price rows:

* 6,202

The zero-price records were also investigated.

Among them:

* 6,131 had missing Customer ID

The quantity distribution of zero-price rows was also examined and showed that these records include both positive and negative quantities.

Zero-price records will therefore be handled carefully during data cleaning rather than automatically assuming that every zero-price row is a valid purchase.

---

## 10. Description Analysis

Missing descriptions:

* 4,382 rows

Several frequent non-product descriptions were identified, including:

* `check`
* `?`
* `damages`
* `damaged`
* `found`
* `missing`
* `adjustment`
* `dotcom`
* `amazon`
* `smashed`

These values suggest that some records contain operational notes or adjustments rather than standard product descriptions.

Since Description is not a primary modeling feature, missing descriptions alone are not considered sufficient reason to remove a transaction.

---

## 11. Temporal Coverage

The dataset spans:

* Minimum date: 2009-12-01 07:45:00
* Maximum date: 2011-12-09 12:50:00

There are:

* 47,635 unique `InvoiceDate` timestamps

The `InvoiceDate` column contains both date and time, so the number of unique timestamps is not equivalent to the number of unique calendar days.

The temporal coverage is sufficient for constructing monthly customer behavior features.

---

## 12. Monthly Transaction Activity

Transaction volume varies considerably across months.

Higher transaction volumes were observed around October-November, while some early-year months had lower activity.

December 2011 contains fewer transactions because the dataset ends on December 9, 2011, making it a partial month.

This is important when interpreting temporal patterns.

---

## 13. Monthly Customer ID Missingness

The missing Customer ID rate varies across months.

Examples:

* 2010-10: approximately 14.45%
* 2010-12: approximately 35.92%
* 2011-01: approximately 37.66%
* 2011-07: approximately 30.41%
* 2011-12: approximately 30.81%

This confirms that missing Customer ID values are not distributed uniformly over time.

Because Customer ID is required for customer-level behavioral analysis, transactions without Customer ID cannot be used to construct identifiable customer behavior histories.

---

## 14. Profiling Conclusions

The profiling stage confirmed that:

1. The dataset contains sufficient temporal information for behavior-shift analysis.
2. Customer ID is available for 77.23% of transaction rows.
3. There are 5,942 identifiable customers and 26,993 active customer-month observations.
4. Duplicate records exist and require explicit handling.
5. Negative quantities are mostly associated with cancellations, but some represent other operational events.
6. Negative-price records were identified as bad-debt adjustments rather than normal purchases.
7. Zero-price transactions require additional investigation before deciding how to handle them.
8. Customer activity varies substantially over time.
9. December 2011 is a partial month and must be considered when interpreting temporal patterns.
10. The raw dataset should remain unchanged, while cleaning and filtering should be performed on processed data.

---

## 15. Next Step

The next stage is **Data Cleaning**.

The cleaning process will define explicit rules for:

* customer identification,
* duplicate handling,
* cancellations and negative quantities,
* zero-price transactions,
* invalid or non-customer transactions,
* and preparation of the customer-level temporal dataset.

All cleaning decisions will be documented before model training to maintain a reproducible and leakage-aware pipeline.

## Data Cleaning & Validation

- Combined the two Online Retail II sheets into a single transaction-level dataset.
- Kept transactions with a valid Customer ID because customer-level behavior analysis requires customer identification.
- Removed cancellation transactions identified by negative quantities and cancellation invoice codes.
- Removed zero-price transactions because they do not represent normal positive-value purchases.
- Removed non-product transactions such as postage, bank charges, and discounts.
- Removed exact duplicate transaction rows.
- Added a monthly time feature (`Month`) derived from `InvoiceDate`.
- Performed final data-quality validation.

### Final Clean Dataset

- Rows: 776,844
- Columns: 9
- Missing values: 0
- Negative quantities: 0
- Zero quantities: 0
- Negative prices: 0
- Zero prices: 0
- Exact duplicates: 0
- Date range: December 2009 – December 2011
- Number of months: 25

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

Train and evaluate the baseline machine learning model.

# Project Notes

## 03 - Temporal Analysis & Feature Engineering

### What are we trying to do?

Our project is not directly predicting customer churn.

The goal is to detect whether a customer's behavior has changed significantly over time.

Instead of looking at one transaction, we convert the transaction-level dataset into **customer-month observations**.

---

## 1. Customer-Month

Each row represents:

> One customer during one active month.

For each customer-month, we calculate:

### `transaction_count`

How many transactions the customer made during that month.

### `total_quantity`

The total number of products/items purchased during that month.

### `total_spending`

The total amount spent during that month.

### `average_transaction_value`

The average value of the customer's transactions.

### `unique_products`

The number of different products purchased.

These features describe the customer's behavior during a specific month.

---

## 2. Why Do We Need Previous Behavior?

A single month's behavior does not tell us whether the customer changed.

For example:

```text
January spending = $500
February spending = $200
```

The important information is not just `$200`.

The important information is:

> Spending decreased compared with the previous period.

Therefore, we create previous-period features.

---

## 3. Previous Behavioral Features

For every customer-month where a previous observation exists, we retrieve the customer's previous behavioral values.

Features:

* `previous_transaction_count`
* `previous_total_quantity`
* `previous_total_spending`
* `previous_average_transaction_value`
* `previous_unique_products`

We also calculate:

### `months_since_previous`

This tells us how many months passed between the current observation and the previous active observation.

Example:

```text
2010-03 → 2010-06
months_since_previous = 3
```

---

## 4. Change Features

We calculate the difference between the current and previous behavior.

Example:

```text
Current spending = 200
Previous spending = 500

Change = 200 - 500
      = -300
```

A negative value means the behavior decreased.

A positive value means the behavior increased.

---

## 5. Percentage Change

Absolute change is not always enough.

For example:

```text
Customer A:
500 → 400
Change = -100

Customer B:
100 → 0
Change = -100
```

Both have the same absolute change, but the relative behavioral change is very different.

Therefore we also calculate percentage changes.

Conceptually:

```text
Percentage Change =
(Current - Previous) / Previous × 100
```

This allows us to measure behavioral change relative to the customer's previous level.

---

## 6. What is the Threshold?

The threshold is simply the boundary we use to decide:

> Is this change large enough to be considered a significant behavioral change?

For the core behavioral dimensions, we used:

```text
Threshold = 100%
```

The core dimensions are:

* `total_quantity`
* `total_spending`
* `average_transaction_value`
* `unique_products`

If the absolute percentage change exceeds the threshold, we count that dimension as having a large change.

---

## 7. `core_large_change_count`

This feature tells us:

> How many core behavioral dimensions changed by more than 100%?

Example:

```text
Spending change       = +150%  → large change
Quantity change       = +20%   → not large
Unique products       = -120%  → large change
Average value         = +10%   → not large
```

Therefore:

```text
core_large_change_count = 2
```

This information is then used to define the behavioral shift target.

---

## 8. Target: `behavior_shift`

The target tells the model what we want it to predict.

```text
behavior_shift = 0 → No significant behavioral shift
behavior_shift = 1 → Significant behavioral shift
```

Final distribution:

```text
No Shift  = 83.53%
Shift     = 16.47%
```

So the target is imbalanced.

This is important because accuracy alone will not be enough to evaluate our models.

---

## 9. Baseline vs Behavior-Aware

This is the main experiment in the project.

### Baseline

The Baseline uses only general historical information:

```text
historical_active_months
historical_transactions
historical_spending
```

The question is:

> Can we detect behavior shifts using only the customer's historical activity?

---

### Behavior-Aware

The Behavior-aware model adds recent behavioral information:

```text
Baseline features
+
previous_transaction_count
previous_total_quantity
previous_total_spending
previous_average_transaction_value
previous_unique_products
months_since_previous
```

The question is:

> Does adding recent behavioral context improve behavior-shift detection?

---

## 10. Why Compare Them?

We need the Baseline as a reference point.

If:

```text
Baseline performance = lower
Behavior-aware performance = higher
```

then we have evidence that temporal behavioral information adds predictive value.

This comparison is one of the main goals of the project.

---

## 11. Temporal Data Split

We cannot randomly split this dataset because the project is about behavior over time.

Instead, we use chronological splitting:

```text
Train:
2010-01 → 2011-05

Validation:
2011-06 → 2011-08

Test:
2011-09 → 2011-12
```

This better represents a real-world scenario:

> Train on the past → validate on a later period → test on an even later period.

---

## 12. Feature Skewness

Some features have highly right-skewed distributions.

For example:

```text
historical_spending = 13.41 skewness
previous_total_quantity = 30.10 skewness
```

This happens because most customers have relatively small values, while a small number of customers have extremely large values.

We identified features that may benefit from log transformation.

However, transformations must be applied inside the modeling pipeline and fitted using training data only.

---

## 13. Final Modeling Dataset

After temporal feature engineering:

```text
Rows = 19,651
Columns = 32
```

Saved as:

```text
data/processed/behavior_change_dataset.csv
```

Not all 32 columns are model features.

Some columns are used for:

* temporal analysis
* target construction
* debugging
* tracking
* customer/month identification

The actual model feature sets are much smaller.

---

## 14. Current Understanding

The whole feature-engineering pipeline can be summarized as:

```text
Transactions
      ↓
Customer-Month Aggregation
      ↓
Monthly Behavioral Features
      ↓
Previous Behavioral Features
      ↓
Behavior Changes
      ↓
Percentage Changes
      ↓
Threshold
      ↓
behavior_shift Target
      ↓
Baseline vs Behavior-Aware Features
      ↓
Temporal Train / Validation / Test
      ↓
Machine Learning
```

### Current Status

Feature engineering is complete.

Next:

**Train the Baseline model and establish the first performance benchmark.**
