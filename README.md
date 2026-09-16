# Personalized-Insurance-Premium

A Machine Learning-powered web application that predicts health insurance premiums based on customer demographics, health conditions, and lifestyle factors. The application provides premium, risk analysis, plan recommendations, and interactive visual analytics through a Streamlit dashboard.

---

## 📌 Project Overview

Insurance companies calculate premiums using multiple factors such as age, BMI, medical history, smoking habits, and family size.

This project uses Machine Learning to:

✅ Predict insurance premium cost

✅ Analyze customer risk level

✅ Recommend suitable insurance plans

✅ Visualize premium trends and customer insights

✅ Generate downloadable premium reports

---

## 🎯 Problem Statement

Manual premium estimation can be time-consuming and inconsistent.

The goal of this project is to develop an intelligent system capable of predicting premiums accurately and providing personalized recommendations for customers.

---

## 🚀 Features

### Premium Prediction
Predicts insurance premium using Machine Learning.

### Risk Assessment
Classifies customers into:

- Low Risk
- Medium Risk
- High Risk

### Insurance Plan Recommendation

Based on customer profile:

- Silver Health Plan
- Gold Health Plan
- Platinum Health Plan

### Interactive Dashboard

Includes:

- Premium Distribution
- Premium vs Age Analysis
- Disease Impact Analysis
- Smoking Impact Analysis
- Risk Gauge Visualization
- Donut Charts
- Radar Charts

### Download Report

Generate and download insurance reports in CSV format.

---

## 🏗️ System Architecture

User Input
↓
Data Preprocessing
↓
Machine Learning Model
(Random Forest Regressor)
↓
Premium Prediction
↓
Risk Analysis
↓
Plan Recommendation

---

## 📊 Dataset Features

| Feature | Description |
|----------|-------------|
| Age | Customer age |
| Gender | Male/Female |
| BMI | Body Mass Index |
| Children | Number of dependents |
| Smoker | Yes/No |
| Region | Residential region |
| Existing Disease | Medical history |
| Premium | Target variable |

---

## 🤖 Machine Learning Model

### Algorithm Used

Random Forest Regressor

### Preprocessing

- One-Hot Encoding
- Pipeline-Based Training
- Automatic Feature Transformation

### Model Performance

| Metric | Value |
|----------|----------|
| R² Score | 0.9595 |
| MAE | ₹821.35 |

### Interpretation

The model explains approximately **96% of the variance** in premium values and predicts premiums with an average error of approximately **₹821**.

---

## 🖥️ Technology Stack

### Frontend

- Streamlit
- HTML/CSS Styling

### Backend

- Python

### Machine Learning

- Scikit-Learn
- Random Forest Regressor

### Data Visualization

- Plotly
- Pandas

### Model Persistence

- Joblib

---
