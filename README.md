<div align="center">

# 🎯 YouTube Comments Sentiment Analysis

### End-to-End MLOps Pipeline · Chrome Extension · Production Deployment on AWS

<br/>

> **A fully production-grade, end-to-end ML system** that classifies YouTube comments into sentiments in real time — surfaced directly inside YouTube via a custom Chrome Extension, powered by a LightGBM model trained with Optuna HPO and served through a Dockerized Flask API on AWS EC2.

</div>

---

## 📈 Key Results at a Glance

| Metric | Baseline Model | Final Model (LightGBM + Optuna) |
|---|---|---|
| F1-Score | 64% | **86%** |
| Hyperparameter Tuning | ❌ | ✅ Optuna |
| Experiment Tracking | ❌ | ✅ MLflow |
| Model Registry | ❌ | ✅ MLflow Registry |
| Deployment | ❌ | ✅ AWS ECR + EC2 |

---

## 📌 Table of Contents

- [Project Overview](#-project-overview)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [ML Pipeline & Experimentation](#-ml-pipeline--experimentation)
- [Local Setup](#-local-setup)

---

## 🔍 Project Overview

Most people rely on gut instinct to judge the reception of a YouTube video. This project replaces that with **real-time, ML-powered sentiment analysis** — right inside the YouTube UI.

A user opens any YouTube video, and the **Chrome Extension** instantly fetches visible comments, sends them to the backend inference API, and overlays sentiment insights (positive / negative / neutral breakdown) on the page — no page reload, no manual work.

The backend is not a quick prototype. It is a **full MLOps system**:

- Reproducible **DVC pipeline** from raw data to a production model
- All experiments tracked in **MLflow** with full parameter, metric, and artifact logging
- Final LightGBM model promoted to the **MLflow Model Registry** (Production stage)
- **Flask API** containerized with Docker and deployed on **AWS EC2** via **AWS ECR**
- Automated **CI/CD** so every code push triggers testing, model validation, image build, and deployment

---
## 🏗️ System Architecture

                    ┌─────────────────────────────────┐
                    │       YouTube (Browser)          │
                    │                                  │
                    │  ┌──────────────────────────┐   │
                    │  │   Chrome Extension (JS)  │   │
                    │  │  - Reads comments        │   │
                    │  │  - Calls Flask API       │   │
                    │  │  - Renders sentiment UI  │   │
                    │  └──────────┬───────────────┘   │
                    └────────────│────────────────────┘
                                 │ HTTP POST /predict
                                 ▼
               ┌─────────────────────────────────────┐
               │         AWS EC2 Instance             │
               │  ┌──────────────────────────────┐   │
               │  │  Docker Container             │   │
               │  │  ┌────────────────────────┐  │   │
               │  │  │   Flask REST API        │  │   │
               │  │  │   - /predict endpoint   │  │   │
               │  │  │   - LightGBM model      │  │   │
               │  │  │   - MLflow Registry     │  │   │
               │  │  └────────────────────────┘  │   │
               │  └──────────────────────────────┘   │
               └─────────────────────────────────────┘
                                 ▲
               ┌─────────────────┴─────────────────┐
               │         AWS ECR                    │
               │  (Docker Image Repository)         │
               └─────────────────┬─────────────────┘
                                 ▲
               ┌─────────────────┴─────────────────┐
               │   GitHub Actions CI/CD             │
               │  Test → Build → Push → Deploy      │
               └─────────────────┬─────────────────┘
                                 ▲
               ┌─────────────────┴─────────────────┐
               │   DVC Pipeline + MLflow Tracking   │
               │   Data → EDA → Train → Evaluate    │
               │         → Register Model           │
               └───────────────────────────────────┘


---
## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.10+ |
| **ML Model** | LightGBM |
| **Hyperparameter Tuning** | Optuna |
| **Experiment Tracking** | MLflow |
| **Model Registry** | MLflow Model Registry |
| **Pipeline Orchestration** | DVC |
| **API Framework** | Flask |
| **Frontend** | Chrome Extension (JavaScript) |
| **Containerization** | Docker |
| **Container Registry** | AWS ECR |
| **Deployment** | AWS EC2 |
| **CI/CD** | GitHub Actions |
| **Version Control** | Git + GitHub |

---

## 🧪 ML Pipeline & Experimentation

### 1. Data Cleaning & EDA
- Removed noise: null values, duplicate comments, special characters, URLs
- Explored label distribution, comment length distribution, and class imbalance
- Text normalization: lowercasing, stopword removal, lemmatization

### 2. Feature Engineering
- Applied **TF-IDF vectorization** to convert text to numerical features
- Experimented with `max_features`, `n-gram range`, and sublinear TF scaling

### 3. Baseline Model
- Built an initial simple classifier to establish a performance floor
- **Baseline F1-Score: 64%**
- Logged baseline parameters and metrics to MLflow

### 4. Model Selection
- Evaluated multiple algorithms (Logistic Regression, Random Forest, XGBoost, LightGBM)
- All runs tracked in MLflow for direct, reproducible comparison

### 5. Hyperparameter Tuning with Optuna
- Used **Optuna** for efficient Bayesian hyperparameter optimization
- Tuned: `num_leaves`, `learning_rate`, `n_estimators`, `max_depth`, `min_child_samples`, `subsample`
- Each trial automatically logged to MLflow as a separate run

### 6. Final Model — LightGBM
- **Final F1-Score: 86%** (+22 percentage points over baseline)
- Selected as the production model and promoted to the **MLflow Model Registry (Production stage)**

---

## 💻 Local Setup

### Prerequisites

- Python 3.10+
- Docker
- DVC
- AWS CLI (configured)
- MLflow

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/constantaryan/yt-comment-sentiments-analysis.git
cd yt-comment-sentiments-analysis

# 2. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate        

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
export MLFLOW_TRACKING_URI=<your-mlflow-uri>
export MLFLOW_TRACKING_USERNAME=<username>
export MLFLOW_TRACKING_PASSWORD=<password>

# 5. Reproduce the DVC pipeline
dvc repro

# 6. Start the Gunicorn server
gunicorn -b 0.0.0.0:5000 app:app

```
💡 If you found this project useful, please consider giving it a ⭐ — it helps others discover it too!


