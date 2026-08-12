# Project Card
# AI-Based Customer Behavior Shift Detection

---

## 1. Project Overview

| Item | Details |
|---|---|
| **Project Name** | AI-Based Customer Behavior Shift Detection |
| **Project Type** | Machine Learning / Customer Behavior Analysis |
| **Project Goal** | Detect significant changes in customer purchasing behavior over time |
| **Dataset** | Online Retail II |
| **Final Model** | XGBoost Classifier |
| **Model Version** | v1 |
| **Deployment** | FastAPI REST API |
| **API Version** | v1 |
| **Prediction Threshold** | 0.30 |
| **Status** | Completed |

---

## 2. Problem Statement

Traditional customer analytics often focuses on static customer characteristics or churn prediction.

This project addresses a different problem:

> Can machine learning detect significant shifts in a customer's purchasing behavior over time?

The system analyzes historical customer activity, previous behavioral patterns, and percentage changes between behavioral periods to identify whether a customer is experiencing a significant behavioral shift.

The objective is therefore not simply to determine whether a customer will stop purchasing, but to detect meaningful changes in purchasing behavior as early as possible.

---

## 3. Proposed Solution

The project implements an end-to-end machine learning pipeline:

```text
Raw Transaction Data
        ↓
Data Profiling
        ↓
Data Cleaning
        ↓
Customer-Level Aggregation
        ↓
30-Day Behavioral Windows
        ↓
Historical & Previous-Window Features
        ↓
Behavior-Change Features
        ↓
BehaviorShift Label
        ↓
Leakage Control
        ↓
Time-Based Evaluation
        ↓
XGBoost Modeling
        ↓
Hyperparameter Tuning
        ↓
Final Model
        ↓
Joblib Model Versioning
        ↓
FastAPI REST API