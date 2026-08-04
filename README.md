# Customer Behavior Shift Detection

A machine learning study investigating whether behavioral change features improve customer behavior shift detection.

## Project Overview

This project develops a **Machine Learning system for detecting significant changes in customer behavior over time**.

Instead of focusing only on whether a customer will churn, the system analyzes changes in customer activity and transaction behavior to identify meaningful behavioral shifts.

The project compares two approaches:

* **Baseline:** Static customer features
* **Behavior-aware model:** Static features combined with temporal behavioral change features

The goal is to determine whether incorporating behavioral changes provides a measurable improvement in detecting customer behavior shifts.

---

## Project Objective

The main objective is to build and evaluate a practical ML pipeline that can:

1. Represent customer behavior over time.
2. Detect significant changes in that behavior.
3. Compare static customer information with temporal behavioral features.
4. Evaluate different classification models using appropriate metrics.
5. Select and tune a final model.
6. Serve the selected model through a FastAPI REST API.

---

## Dataset

**Dataset:** Online Retail II

**Source:** UCI Machine Learning Repository

The dataset contains transaction-level retail data covering multiple periods between 2009 and 2011.

### Original Features

* `Invoice`
* `StockCode`
* `Description`
* `Quantity`
* `InvoiceDate`
* `Price`
* `Customer ID`
* `Country`

### Original Dataset Size

* **1,067,371 transactions**
* **8 original features**
* **5,942 unique customers with Customer ID**
* **77.23% Customer ID coverage**
* Transaction timestamps spanning **December 2009 – December 2011**

The original dataset is provided as an Excel workbook containing two sheets. The sheets were programmatically combined into a single dataset for analysis.

The raw dataset is excluded from version control and is kept locally. Dataset acquisition and preparation instructions will be documented to support reproducibility.

---

## Data Cleaning

A documented data-cleaning process was applied before temporal analysis and feature engineering.

### Cleaning Steps

The following data-quality issues were addressed:

* Removed transactions without `Customer ID`.
* Removed cancellation invoices.
* Removed zero-price transactions.
* Removed negative-price transactions.
* Removed non-commercial transactions such as postage, bank charges, and discounts.
* Removed exact duplicate transactions.
* Validated transaction quantities and prices.
* Validated missing values.
* Validated transaction dates.
* Audited suspicious transaction descriptions.

### Final Cleaned Dataset

After cleaning:

* **776,844 transactions**
* **8 features**
* **5,942 unique customers**
* **25 months of transaction history**
* **No missing values**
* **No negative quantities**
* **No zero quantities**
* **No negative prices**
* **No zero prices**
* **No exact duplicate rows**
* **No suspicious transaction descriptions**
* **Date range:** December 2009 – December 2011

The cleaned dataset is stored locally and excluded from version control.

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
Customer-Month Dataset
        ↓
Temporal Feature Engineering
        ↓
Behavior Shift Definition
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
* Changes in average transaction value
* Changes in product diversity
* Changes in customer activity over time

The final feature set and observation windows will be determined through temporal analysis and documented based on the dataset characteristics.

---

## Temporal Analysis

The cleaned transaction data will be transformed into a **customer-month level dataset**.

Each customer-month observation will summarize customer behavior using features such as:

* Transaction count
* Total quantity
* Total spending
* Average transaction value
* Number of unique products

These monthly behavioral observations will be used to calculate changes and trends over time.

The temporal analysis will also be used to define a defensible **behavior shift target** while avoiding information leakage.

---

## Behavior Shift Definition

The project focuses on detecting **behavioral change**, rather than directly predicting customer churn.

The behavior shift target will be defined based on measurable changes in customer activity and transaction behavior over time.

The final target definition will be selected after analyzing the temporal behavior distribution and will be documented together with the reasoning behind the chosen threshold or rule.

---

## Model Evaluation

The project will not rely on **Accuracy alone**.

Evaluation metrics will be selected according to the final target definition and class distribution.

Candidate metrics include:

* Precision
* Recall
* F1-score
* ROC-AUC
* PR-AUC

The baseline and candidate models will be evaluated using the same leakage-aware data split.

---

## Baseline vs Behavior-Aware Model

The project will compare:

### Baseline Model

Uses static or non-temporal customer information.

### Behavior-Aware Model

Uses static customer information combined with temporal behavioral change features.

The main research question is:

> **Do temporal behavioral change features improve the detection of customer behavior shifts compared with a baseline using static customer information?**

---

## Model Versioning

The project will maintain at least two model versions:

* `v1` — Initial/baseline model
* `v2` — Improved/final candidate model

One model version will be promoted as the **live model**.

Each prediction will include the corresponding model version.

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

It includes:

* Fixed random seeds
* Pinned Python dependencies
* Versioned models
* Model metadata
* Automated tests
* Dataset preparation instructions
* Clone-and-run documentation

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
│   ├── 01_data_profiling.ipynb
│   ├── 02_data_cleaning.ipynb
│   └── 03_temporal_analysis.ipynb
│
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

**Current Stage:** Temporal Analysis & Feature Engineering

### Completed

* [x] GitHub repository setup
* [x] Python virtual environment setup
* [x] Project structure created
* [x] Requirements file created
* [x] Online Retail II dataset selected
* [x] Original Excel dataset inspected
* [x] Two dataset sheets identified
* [x] Sheets programmatically combined
* [x] Combined dataset created
* [x] Initial dataset profiling
* [x] Data quality assessment
* [x] Customer ID filtering
* [x] Cancellation handling
* [x] Zero-price and negative-price handling
* [x] Non-commercial transaction filtering
* [x] Duplicate validation
* [x] Suspicious description audit
* [x] Date validation
* [x] Final cleaned dataset validation
* [x] Final cleaned dataset saved locally

### In Progress

* [ ] Temporal behavior analysis
* [ ] Customer-month dataset construction
* [ ] Behavioral feature engineering
* [ ] Behavior shift definition
* [ ] Leakage analysis
* [ ] Baseline model
* [ ] Behavior-aware model
* [ ] Model comparison
* [ ] Hyperparameter tuning
* [ ] Error analysis
* [ ] Model versioning
* [ ] FastAPI deployment

---

## Current Next Step

The next stage is to construct the **Customer-Month Dataset** from the final cleaned transaction data and analyze customer behavior over time.

This dataset will serve as the foundation for temporal behavioral features and the final behavior-shift detection target.
