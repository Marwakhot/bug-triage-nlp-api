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

---

## How to Run
### 1. Local Setup (Without Docker)
**Step 1: Clone the repository and set up the environment**
```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/Marwakhot/bug-triage-nlp-api.git)
cd bug-triage-nlp-api

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt 
```
**Step 2: Generate the Model File**  
Before you can run the applications, you must generate the model file.  
Open and run the `notebooks/01-data-cleaning.ipynb` notebook from top to bottom.   
Then, open and run the `notebooks/02-model-training.ipynb` notebook. This will create the `final_multimodel.pkl` file.

**Step 3: Run an Application**
You can now run either the Flask app or the Streamlit dashboard.
- To run the Streamlit Dashboard (Recommended):
  ```bash
  streamlit run dashboard.py
  ```
  Then open your browser to http://localhost:8501

- To run the Flask App:
  ```bash
  python app.py
  ```
  Then open your browser to http://localhost:8080

### 2. Docker Setup (Recommended)
Prerequisite: You must have Docker Desktop installed and running.  
Step 1: Build the Docker image
In your terminal, from the project's root directory, run:
```bash
docker build -t bug-triage-dashboard .
```
Step 2: Run the Docker container
This will start the Streamlit dashboard.
```bash
docker run -p 8501:8501 bug-triage-dashboard
```
Now, open your web browser and go to http://localhost:8501
  
