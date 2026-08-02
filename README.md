# Customer Behavior Shift Detection

A machine learning project investigating whether **behavioral change features improve the detection of significant customer behavior shifts over time**.

## Project Overview

This project develops a **Machine Learning system for detecting meaningful changes in customer behavior over time**.

Instead of focusing only on whether a customer will churn, the system analyzes changes in customer activity and transaction behavior to identify significant behavioral shifts.

The project compares two approaches:

* **Baseline:** Static customer features
* **Behavior-aware model:** Static features combined with temporal behavioral change features

The goal is to determine whether incorporating behavioral changes provides a measurable improvement in detecting customer behavior shifts.

---

## Project Objective

The project aims to build and evaluate a practical ML pipeline that can:

1. Represent customer behavior over time.
2. Define and detect significant behavioral shifts.
3. Compare static customer information with temporal behavioral features.
4. Evaluate multiple classification models using appropriate metrics.
5. Tune and select a final model.
6. Analyze model errors.
7. Serve the selected model through a FastAPI REST API.
8. Maintain reproducible model versions and metadata.

---

## Dataset

**Dataset:** Online Retail II

**Source:** UCI Machine Learning Repository

The dataset contains transaction-level retail data covering the period from **December 2009 to December 2011**.

### Original Features

* `Invoice`
* `StockCode`
* `Description`
* `Quantity`
* `InvoiceDate`
* `Price`
* `Customer ID`
* `Country`

### Dataset Structure

The original dataset is provided as an Excel workbook containing two sheets:

* `Year 2009-2010`
* `Year 2010-2011`

The two sheets were programmatically combined into a single transaction-level dataset.

The raw dataset is excluded from version control and is kept locally. Dataset acquisition and preparation instructions will be documented to support reproducibility.

### Dataset Size

* **1,067,371 transactions**
* **8 original features**
* **5,942 customers with Customer ID**
* **77.23% of transactions have a Customer ID**
* **25 months of transaction data**

---

## Initial Data Profiling

Initial profiling was performed to assess data quality and determine whether the dataset is suitable for customer-level temporal behavioral analysis.

### Customer Coverage

* Unique customers: **5,942**
* Transactions with Customer ID: **824,364**
* Transactions without Customer ID: **243,007**
* Customer ID coverage: **77.23%**
* Customers with multiple transactions: **5,796**
* Customers active in multiple months: **4,212**
* Customers active in multiple years: **2,890**
* Active customer-month observations: **26,993**

### Temporal Coverage

* Start date: **December 1, 2009**
* End date: **December 9, 2011**
* Number of unique transaction timestamps: **47,635**
* Number of calendar months represented: **25**

The data contains transactions in every month across the observed period, providing sufficient temporal structure for behavioral analysis.

### Data Quality Findings

Initial profiling identified:

* Missing `Customer ID` values
* Missing product descriptions
* Exact duplicate records
* Negative quantities
* Cancellation transactions
* Zero-price transactions
* Negative-price accounting adjustments
* A partially observed final month

These issues will be addressed through a documented data-cleaning strategy before feature engineering and model development.

---

## Machine Learning Approach

The project follows a leakage-aware classification workflow:

```text
Raw Transaction Data
        ↓
Data Profiling & Quality Checks
        ↓
Data Cleaning
        ↓
Customer-Level Dataset
        ↓
Temporal Feature Engineering
        ↓
Behavior Shift Definition
        ↓
Leakage Analysis
        ↓
Train / Validation / Test Split
        ↓
Baseline Model
        ↓
Model Comparison
        ↓
Hyperparameter Tuning
        ↓
Error Analysis
        ↓
Model Versioning
        ↓
FastAPI REST API
        ↓
Testing & Reproducibility
```

---

## Behavioral Features

Behavioral features will be derived from customer transaction history over time.

Potential features include:

* Transaction frequency changes
* Spending changes
* Purchase quantity changes
* Recency
* Activity trends
* Changes in transaction frequency
* Changes in average transaction value
* Changes in purchase behavior over defined time windows

The final feature set will be determined after completing the data-cleaning strategy and defining the behavioral shift target.

---

## Baseline and Model Comparison

The project will establish a **static-feature baseline** and compare it with a **behavior-aware model** that incorporates temporal behavioral change features.

At least two classification models will be evaluated using the same leakage-aware data split.

The final model will be selected based on appropriate evaluation metrics and error analysis rather than accuracy alone.

---

## Model Evaluation

The project will not rely on **Accuracy alone**.

Evaluation metrics will be selected according to the final target definition and class distribution.

Potential metrics include:

* Precision
* Recall
* F1-score
* ROC-AUC
* PR-AUC

The baseline and candidate models will be evaluated using the same leakage-aware evaluation strategy.

---

## Leakage Prevention

Because the project focuses on behavioral changes over time, preventing temporal data leakage is a critical requirement.

Feature engineering and target construction will ensure that information from the future is not used to predict or define the earlier observation period.

The final train, validation, and test strategy will be documented in the project.

---

## Model Versioning

The project will maintain at least two model versions:

* `v1` — Initial/baseline model
* `v2` — Improved/final candidate model

One model version will be promoted as the **live model**.

Each prediction will include the corresponding `model_version`.

Each model version will have associated metadata describing the model, features, training configuration, and evaluation results.

---

## API

The final model will be exposed through a **FastAPI REST API**.

### Endpoints

| Endpoint    | Purpose                         |
| ----------- | ------------------------------- |
| `/health`   | API health check                |
| `/predict`  | Generate a prediction           |
| `/metadata` | Return model metadata           |
| `/versions` | Return available model versions |

The API will include input validation and return HTTP `422` for invalid input.

---

## Reproducibility

The project is designed to be reproducible by another user.

It will include:

* Fixed random seeds
* Pinned Python dependencies
* Versioned models
* Model metadata
* Automated tests
* Dataset preparation instructions
* Clone-and-run documentation
* Reproducible training and prediction workflow

---

## Repository Structure

```text
customer-behavior-shift-detection/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
├── src/
├── models/
├── outputs/
├── api/
├── tests/
├── docs/
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Project Status

**Current Stage:** Dataset Profiling Completed

### Completed

* [x] GitHub repository setup
* [x] Python virtual environment setup
* [x] Project structure created
* [x] Online Retail II dataset selected
* [x] Original Excel dataset inspected
* [x] Two dataset sheets identified
* [x] Sheets programmatically combined
* [x] Combined dataset created
* [x] Initial dataset inspection notebook created
* [x] Missing-value profiling
* [x] Duplicate analysis
* [x] Quantity and price validation
* [x] Cancellation analysis
* [x] Customer coverage analysis
* [x] Temporal activity analysis
* [x] Monthly customer activity analysis

### Next Steps

* [ ] Define data-cleaning strategy
* [ ] Implement data cleaning
* [ ] Define behavioral observation windows
* [ ] Define the behavior shift target
* [ ] Perform leakage analysis
* [ ] Engineer behavioral change features
* [ ] Build baseline model
* [ ] Compare candidate models
* [ ] Tune finalist model
* [ ] Perform error analysis
* [ ] Implement model versioning
* [ ] Build FastAPI API
* [ ] Add tests
* [ ] Complete Model Card
* [ ] Finalize documentation and clone test
