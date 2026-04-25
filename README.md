# 🎬 IMDB Sentiment Analysis — End-to-End MLOps Pipeline

![Python](https://img.shields.io/badge/Python-3.10-blue)
![MLflow](https://img.shields.io/badge/MLflow-2.15-orange)
![DVC](https://img.shields.io/badge/DVC-3.53-purple)
![Docker](https://img.shields.io/badge/Docker-✓-blue)
![Kubernetes](https://img.shields.io/badge/Kubernetes-1.32-blue)
![AWS](https://img.shields.io/badge/AWS-EKS%20|%20ECR%20|%20S3-orange)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-green)

A production-grade, fully automated MLOps pipeline for sentiment analysis on 50,000 IMDB movie reviews — from data ingestion to model deployment on AWS EKS with real-time monitoring.

---

## 🏗️ Project Architecture

```
Developer (git push)
        │
        ▼
GitHub Actions (CI/CD)
        │
        ├── DVC Pipeline (Train → Evaluate → Register)
        ├── MLflow (Experiment Tracking + Model Registry)
        ├── Docker Build → AWS ECR (Image Registry)
        └── kubectl apply → AWS EKS (Deployment)
                │
                ▼
        AWS ELB (Load Balancer)
                │
        ┌───────┴───────┐
        │               │
    Pod 1 (Flask)   Pod 2 (Flask)
        │
        ▼
AWS EC2 (Prometheus) → AWS EC2 (Grafana)
```

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| **ML & NLP** | Scikit-learn, NLTK, Logistic Regression, BoW |
| **Experiment Tracking** | MLflow, DagsHub |
| **Data Versioning** | DVC, AWS S3 |
| **Web App** | Flask, Python |
| **Containerization** | Docker, AWS ECR |
| **Orchestration** | Kubernetes, AWS EKS |
| **CI/CD** | GitHub Actions |
| **Monitoring** | Prometheus, Grafana, AWS EC2 |
| **Cloud** | AWS (EKS, ECR, S3, EC2, IAM, ELB, VPC) |

---

## 📊 ML Experimentation Results

Tested 10 algorithm-vectorizer combinations tracked via MLflow:

| Algorithm | Vectorizer | Accuracy | F1 Score |
|---|---|---|---|
| **Logistic Regression** | **BoW** | **85%** | **0.83** ✅ |
| Gradient Boosting | TF-IDF | 82% | 0.83 |
| Multinomial NB | BoW | 82% | 0.81 |
| Random Forest | BoW | 74% | 0.72 |
| XGBoost | TF-IDF | 72% | 0.73 |

**Best Hyperparameters:** `C=10, penalty=l2, solver=liblinear`

---

## 📁 Project Structure

```
mlops-project/
├── .github/
│   └── workflows/
│       └── ci.yaml              # GitHub Actions CI/CD
├── data/
│   ├── raw/                     # Original data
│   ├── interim/                 # Preprocessed data
│   └── processed/               # Feature engineered data
├── flask_app/
│   ├── app.py                   # Flask application
│   └── templates/               # HTML templates
├── models/
│   ├── model.pkl                # Trained model
│   └── vectorizer.pkl           # Text vectorizer
├── notebooks/
│   ├── exp1_baseline.py         # Baseline experiments
│   ├── exp2_bow_vs_tfidf.py     # BoW vs TF-IDF comparison
│   └── exp3_lor_bow_hp.py       # Hyperparameter tuning
├── reports/
│   ├── metrics.json             # Model metrics
│   └── experiment_info.json     # MLflow run info
├── scripts/
│   └── promote_model.py         # Staging → Production
├── src/
│   ├── data/
│   │   ├── data_ingestion.py    # Kaggle data download
│   │   └── data_preprocessing.py # Text cleaning
│   ├── features/
│   │   └── feature_engineering.py # BoW vectorization
│   └── model/
│       ├── model_building.py    # Model training
│       ├── model_evaluation.py  # Metrics + MLflow logging
│       └── register_model.py    # MLflow Model Registry
├── tests/
│   ├── test_model.py            # Model unit tests
│   └── test_flask_app.py        # Flask app tests
├── deployment.yaml              # Kubernetes deployment
├── Dockerfile                   # Docker image
├── dvc.yaml                     # DVC pipeline stages
├── params.yaml                  # Pipeline parameters
└── requirements.txt             # Dependencies
```

---

## 🔄 DVC Pipeline Stages

```yaml
data_ingestion      # Kaggle → 50K IMDB reviews
      ↓
data_preprocessing  # NLTK text cleaning
      ↓
feature_engineering # BoW vectorization (5000 features)
      ↓
model_building      # Logistic Regression training
      ↓
model_evaluation    # Metrics + MLflow logging
      ↓
model_registration  # MLflow Model Registry
```

---

## 🚀 CI/CD Pipeline

Every `git push` triggers:

```
1. Install dependencies
2. dvc repro        → Full ML pipeline
3. dvc push         → Save artifacts to S3
4. Run model tests  → Performance validation
5. Promote model    → Staging → Production
6. Run Flask tests  → API validation
7. Docker build     → Create image
8. ECR push         → Store image
9. EKS deploy       → Update production
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10
- AWS CLI configured
- Docker Desktop
- kubectl + eksctl

### Local Setup

```bash
# 1. Clone repo
git clone https://github.com/altamashhhh/mlops-project
cd mlops-project

# 2. Create virtual environment
conda create -n imbd python=3.10
conda activate imbd

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
export CAPSTONE_TEST=your_dagshub_token
export KAGGLE_API_TOKEN=your_kaggle_token

# 5. Run DVC pipeline
dvc repro

# 6. Run Flask app locally
cd flask_app
python app.py
```

---

## 🌐 Deployment

### AWS EKS Deployment

```bash
# Create EKS cluster
eksctl create cluster \
  --name flask-app-cluster \
  --region us-east-1 \
  --nodegroup-name flask-app-nodes \
  --node-type t3.small \
  --nodes 1 --managed \
  --version 1.32

# Deploy application
kubectl apply -f deployment.yaml

# Get public URL
kubectl get svc flask-app-service
```

### Access the App
```
http://<EXTERNAL-IP>
```

---

## 📈 Monitoring

### Prometheus
- Deployed on AWS EC2 (Ubuntu, t3.medium)
- Scrape interval: 15 seconds
- Metrics: Request count, latency, prediction distribution

### Grafana
- Deployed on AWS EC2 (Ubuntu, t3.medium)
- Port: 3000
- Data source: Prometheus

### Custom Metrics Tracked
```python
REQUEST_COUNT      # Total requests per endpoint
REQUEST_LATENCY    # Response time in seconds
PREDICTION_COUNT   # Positive vs Negative predictions
```

---

## 🔐 GitHub Secrets Required

| Secret | Description |
|---|---|
| `CAPSTONE_TEST` | DagsHub API token |
| `KAGGLE_API_TOKEN` | Kaggle API token |
| `AWS_ACCESS_KEY_ID` | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key |
| `AWS_REGION` | AWS region (us-east-1) |
| `AWS_ACCOUNT_ID` | AWS account ID |
| `ECR_REPOSITORY` | ECR repo name (flask-app) |

---

## 📦 Model Registry

Models tracked in MLflow Model Registry with aliases:

```
my_model
├── Version 1  
├── Version 2  
├── ...
└── Latest → @Staging or @Production
```

---

## 🧪 Running Tests

```bash
# Model tests
python -m unittest tests/test_model.py

# Flask app tests
python -m unittest tests/test_flask_app.py
```

---

## 🗑️ AWS Cleanup

```bash
# Delete Kubernetes resources
kubectl delete deployment flask-app
kubectl delete service flask-app-service
kubectl delete secret capstone-secret

# Delete EKS cluster
eksctl delete cluster --name flask-app-cluster --region us-east-1

# Verify deletion
eksctl get cluster --region us-east-1
```

---

## 👨‍💻 Author

**Altamash Ansari**
- GitHub: [@altamashhhh](https://github.com/altamashhhh)
- DagsHub: [@altamashdsa99](https://dagshub.com/altamashdsa99)

---

## 📄 License

This project is licensed under the MIT License.
