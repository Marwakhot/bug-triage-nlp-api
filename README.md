# Automated Bug Triage System

This project is an end-to-end machine learning application designed to automate the process of bug report triage. It uses Natural Language Processing (NLP) to read a bug report's description and metadata, and predicts both the responsible engineering team (**Component**) and the bug's **Priority**.

This repository contains two different web applications that use the same trained model:
1.  A simple **Flask** app for single predictions via a web form.
2.  An advanced **Streamlit** dashboard for bulk predictions and analytics.

---
## Key Features

* **Dual Prediction:** Predicts both the responsible `Component` and `Priority` for each bug report.
* **Advanced ML Pipeline:** Uses a `LightGBM` model with a `scikit-learn` pipeline that combines text features (TF-IDF with n-grams) and categorical features (One-Hot Encoding).
* **Data Cleaning:** Includes a notebook that systematically cleans the raw data and handles the real-world problem of a highly imbalanced target variable.
* **Flask Web App:** A simple, user-friendly web form for submitting a single bug report and seeing the instant prediction.
* **Streamlit Analytics Dashboard:** A powerful tool for business insights, featuring:
    * Bulk prediction via CSV upload.
    * A flexible, interactive column-mapping interface to handle various CSV formats.
    * `Plotly` visualizations to analyze prediction results.
* **Containerized with Docker:** The entire application is containerized with a `Dockerfile`, allowing for easy, reproducible deployment.

---
## Project Structure
├── data/  
│   ├── Eclipse.csv  
│   └── cleaned_bug_reports.csv  
├── models/  
│   └── final_multimodel.pkl  
├── notebooks/  
│   ├── 01-data-cleaning.ipynb  
│   └── 02-model-training.ipynb  
├── templates/  
│   └── index.html  
├── app.py  
├── dashboard.py  
├── Dockerfile  
├── requirements.txt  
└── test_api.py  
