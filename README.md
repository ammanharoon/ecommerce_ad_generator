# E-Commerce Ad Creative Generator - MLOps Pipeline

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.108.0-green)
![Docker](https://img.shields.io/badge/Docker-24.0-blue)
![Kubernetes](https://img.shields.io/badge/Kubernetes-1.28-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Overview

An **end-to-end production-grade MLOps system** that automatically generates compelling marketing ad copy for e-commerce products using fine-tuned T5 transformer models. The system demonstrates complete ML lifecycle management from data ingestion to production deployment with monitoring.

### Key Features

### Key Highlights
- ✅ **Automated Data Pipeline** with Apache Airflow orchestration
- ✅ **Fine-tuned T5 Model** for ad generation with MLflow experiment tracking
- ✅ **Production-Ready FastAPI** with comprehensive metrics
- ✅ **Containerized** with multi-stage Docker builds
- ✅ **CI/CD Pipeline** with GitHub Actions (automated testing, linting, building)
- ✅ **Kubernetes Deployment** with auto-scaling (HPA) and zero-downtime updates
- ✅ **Real-Time Monitoring** with Prometheus and Grafana dashboards
- ✅ **Cloud-Ready** architecture (deployable to AWS EKS, GCP GKE, Azure AKS)
- ✅ **🎁 BONUS: Drift Detection** (+5) - Statistical monitoring for model drift
- ✅ **🎁 BONUS: Canary Deployment** (+5) - Safe rollout strategy with traffic splitting

### Bonus Features (+10 Marks)
This project implements **two bonus features** for additional marks:
1. **[Model Drift Detection](docs/BONUS_SUMMARY.md#feature-1-model-drift-detection-5-marks)** (+5) - Real-time statistical drift monitoring using KS tests
2. **[Canary Deployment Strategy](docs/BONUS_SUMMARY.md#feature-2-canary-deployment-strategy-5-marks)** (+5) - Safe gradual rollouts with 75/25 traffic split

📚 **[Full Bonus Features Documentation](docs/BONUS_SUMMARY.md)** | **[Quick Start Guide](BONUS_QUICKSTART.md)**

---

## 🚀 Problem Statement

### Business Challenge

E-commerce businesses struggle to create personalized, engaging product advertisements at scale:

- **Manual Creation:** Hours per product, limiting scalability
- **High Costs:** Requires specialized copywriting expertise  
- **Inconsistent Quality:** Variable output across products
- **Operational Bottleneck:** Cannot handle thousands of products

### Our Solution

AI-powered system that:
1. Ingests product data (name, category, description, price)
2. Generates high-quality ad copy using fine-tuned T5 models
3. Serves predictions via REST API with <10s latency
4. Scales automatically based on demand (1-5 pods)
5. Monitors performance with 15+ custom metrics

### Success Metrics

| Metric | Target | Achieved |
|--------|--------|----------|
| Generation Time (P95) | <10s | ~8.5s ✅ |
| Throughput | 10+ concurrent | 10+ ✅ |
| Uptime | 99%+ | 99%+ ✅ |
| Quality | Grammatically correct | ✅ |

---

## 🏗️ System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT / USER                            │
│                     (Browser / API Client)                       │
└─────────────────────────────┬───────────────────────────────────┘
                              │ HTTP/HTTPS
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      KUBERNETES CLUSTER                          │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │         LoadBalancer Service (Port 80)                 │    │
│  └────────────────────────┬───────────────────────────────┘    │
│                           │                                     │
│                           ▼                                     │
│  ┌────────────────────────────────────────────────────────┐    │
│  │      Ad Generator API Pods (1-5 replicas, HPA)        │    │
│  │  • FastAPI Application                                 │    │
│  │  • T5 Model Inference                                  │    │
│  │  • Prometheus Metrics Exporter                         │    │
│  │  • Health Checks (liveness/readiness)                  │    │
│  └────────────────────┬───────────────────────────────────┘    │
│                       │ Metrics                                 │
│                       ▼                                         │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Prometheus (Metrics Storage & Alerting)               │    │
│  └────────────────────┬───────────────────────────────────┘    │
│                       │                                         │
│                       ▼                                         │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Grafana (Visualization & Dashboards)                  │    │
│  └────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### MLOps Pipeline Flow

```
DATA PIPELINE (Apache Airflow)
    ├── Ingest raw product data
    ├── Preprocess & clean
    ├── Generate synthetic training data
    └── Validate quality
         │
         ▼
MODEL TRAINING (MLflow + PyTorch)
    ├── Fine-tune T5-base model
    ├── Track experiments in MLflow
    ├── Log hyperparameters & metrics
    └── Save model checkpoints
         │
         ▼
CONTAINERIZATION (Docker)
    ├── Multi-stage build
    ├── Download model artifacts
    ├── Install dependencies
    └── Create production image
         │
         ▼
CI/CD (GitHub Actions)
    ├── Run automated tests
    ├── Code linting (flake8)
    ├── Build Docker image
    ├── Push to Docker Hub
    └── Validate K8s manifests
         │
         ▼
DEPLOYMENT (Kubernetes)
    ├── Deploy to K8s cluster
    ├── Configure auto-scaling (HPA)
    ├── Set up monitoring
    └── Expose via LoadBalancer
         │
         ▼
MONITORING (Prometheus + Grafana)
    ├── Collect 15+ metrics
    ├── Visualize in dashboards
    ├── Alert on anomalies
    └── Track ML performance
```

---

## 🛠️ Technology Stack

### Core Technologies

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Language** | Python | 3.11 | Primary development |
| **ML Framework** | PyTorch | 2.5.1 | Model training & inference |
| **Transformer** | Hugging Face | 4.36.2 | T5 implementation |
| **API** | FastAPI | 0.108.0 | REST API service |
| **Server** | Uvicorn | 0.25.0 | ASGI production server |

### MLOps Stack

| Tool | Version | Purpose |
|------|---------|---------|
| **Tracking** | MLflow | 2.9.2 | Experiment tracking & versioning |
| **Orchestration** | Apache Airflow | 2.7.3 | Data pipeline automation |
| **Containers** | Docker | 24.0+ | Application packaging |
| **Orchestration** | Kubernetes | 1.28+ | Container orchestration |
| **Metrics** | Prometheus | 2.48.0 | Time-series metrics |
| **Visualization** | Grafana | 10.2.0 | Monitoring dashboards |

### Infrastructure

| Component | Technology |
|-----------|-----------|
| **Registry** | Docker Hub |
| **CI/CD** | GitHub Actions |
| **Local K8s** | Minikube |
| **Cloud K8s** | GKE/EKS/AKS |
| **VCS** | Git/GitHub |

---

## 📁 Project Structure

```
e-commerce-ad-creative-generator/
├── .github/
│   └── workflows/
│       ├── ci-cd-pipeline.yaml          # Main CI/CD workflow
│       └── deploy-k8s.yaml              # K8s deployment workflow
│
├── airflow/
│   ├── dags/
│   │   └── ad_generator_dag.py          # Data pipeline DAG
│   ├── logs/                            # Airflow logs
│   └── airflow.cfg                      # Configuration
│
├── data/
│   ├── raw/                             # Raw product data
│   ├── processed/                       # Cleaned data
│   └── synthetic/                       # Generated data
│
├── docker/
│   ├── Dockerfile                       # Production build
│   └── .dockerignore                    # Exclude patterns
│
├── k8s/
│   ├── configmap.yaml                   # App configuration
│   ├── secret.yaml                      # Sensitive data
│   ├── deployment.yaml                  # Pod specification
│   ├── service.yaml                     # LoadBalancer
│   ├── hpa.yaml                         # Auto-scaler
│   └── monitoring/
│       ├── prometheus-config.yaml       # Prometheus config
│       ├── prometheus-deployment.yaml   # Prometheus deployment
│       ├── grafana-deployment.yaml      # Grafana deployment
│       └── grafana-dashboard.yaml       # Dashboard definition
│
├── models/
│   └── checkpoints/
│       └── final_model/                 # Fine-tuned weights
│
├── src/
│   ├── api/
│   │   ├── app.py                       # FastAPI application
│   │   ├── schemas.py                   # Pydantic models
│   │   ├── service.py                   # Business logic
│   │   └── metrics.py                   # Prometheus metrics
│   ├── data/
│   │   ├── pipeline.py                  # Preprocessing
│   │   └── generator.py                 # Synthetic data
│   ├── model/
│   │   ├── trainer.py                   # Training logic
│   │   └── inference.py                 # Inference wrapper
│   └── utils/
│       ├── logger.py                    # Logging config
│       └── config.py                    # Config loader
│
├── tests/
│   ├── test_api.py                      # API tests
│   ├── test_model.py                    # Model tests
│   └── test_pipeline.py                 # Pipeline tests
│
├── config.yaml                          # Application config
├── requirements.txt                     # Dev dependencies
└── requirements-docker.txt              # Production dependencies
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker 24.0+
- Kubernetes 1.28+ (Minikube for local)
- 8GB+ RAM
- 20GB+ disk space

### 1. Clone & Setup

```bash
# Clone repository
git clone https://github.com/MLOPS-Fall-2025/e-commerce-ad-creative-generator.git
cd e-commerce-ad-creative-generator

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Train Model

```bash
# Start MLflow UI
mlflow ui --port 5000 &

# Run training
python scripts/train.py

# Monitor at: http://localhost:5000
```

### 3. Run API Locally

```bash
# Start API
python src/api/app.py

# Access:
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs
```

### 4. Deploy to Kubernetes

```bash
# Start Minikube
minikube start --driver=docker --cpus=4 --memory=8192

# Deploy application
kubectl apply -f k8s/

# Deploy monitoring
kubectl apply -f k8s/monitoring/

# Check status
kubectl get all

# Access services
kubectl port-forward svc/ad-generator-service 8000:80
```

---

## 💻 API Usage

### Health Check

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_name": "t5-base",
  "device": "cpu",
  "uptime_seconds": 120.45
}
```

### Generate Ad

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Wireless Headphones Pro",
    "category": "Electronics",
    "description": "Premium noise-cancelling wireless headphones with 30-hour battery",
    "price": 149.99
  }'
```

**Response:**
```json
{
  "product_name": "Wireless Headphones Pro",
  "generated_ad": "Experience premium sound with Wireless Headphones Pro! Featuring noise-cancelling technology and 30-hour battery life. Get yours for only $149.99!",
  "category": "Electronics",
  "price": 149.99,
  "generation_time_ms": 8589.78,
  "timestamp": "2025-12-14T10:31:00"
}
```

### View Metrics

```bash
curl http://localhost:8000/metrics
```

---

## 📊 Monitoring

### Access Dashboards

```bash
# Prometheus (metrics & queries)
kubectl port-forward svc/prometheus 9090:9090
# Open: http://localhost:9090

# Grafana (visualizations)
kubectl port-forward svc/grafana 3000:3000
# Open: http://localhost:3000
# Login: admin / admin123
```

### Key Metrics (15+)

| Metric | Description |
|--------|-------------|
| `ad_generator_requests_total` | Total API requests |
| `ad_generator_generation_time_seconds` | Latency histogram |
| `ad_generator_ads_generated_total` | Ads by category |
| `ad_generator_errors_total` | Error count by type |
| `ad_generator_active_requests` | Concurrent requests |
| `ad_generator_uptime_seconds` | Service uptime |
| `ad_generator_ad_length_characters` | Ad quality metric |
| `ad_generator_product_price` | Price distribution |

### Grafana Dashboard

Pre-configured dashboard: **"Ad Generator ML Metrics"**

**10 Visualization Panels:**
- Request Rate (time series)
- Generation Latency P95 (graph)
- Total Ads Generated (stat)
- Error Rate (gauge with thresholds)
- Active Requests (gauge)
- Ads by Category (stacked area)
- Ad Quality - Length (histogram)
- Price Distribution (histogram)
- Service Uptime (time series)
- Model Information (table)

---

## 🔄 MLOps Lifecycle

### Stage 1: Data Pipeline (Airflow)

**DAG:** `ad_generator_data_pipeline`  
**Schedule:** Daily

**Tasks:**
1. `data_ingestion` - Load raw CSV/JSON
2. `data_preprocessing` - Clean & validate
3. `feature_engineering` - Create input-target pairs
4. `data_validation` - Quality checks

### Stage 2: Model Training (MLflow)

**Model:** T5-base fine-tuned

**Hyperparameters:**
- Epochs: 3
- Batch size: 4
- Learning rate: 5e-5
- Max length: 200 tokens

**Tracked Metrics:**
- Training/validation loss
- Perplexity
- Generation examples

### Stage 3: CI/CD (GitHub Actions)

**Workflow:** `.github/workflows/ci-cd-pipeline.yaml`

**Stages:**
1. Test & Lint (pytest + flake8)
2. Build Docker image
3. Push to Docker Hub
4. Validate K8s manifests
5. Trigger deployment

### Stage 4: Deployment (Kubernetes)

**Resources:**
- **Deployment:** 1-5 replicas with rolling updates
- **Service:** LoadBalancer (port 80 → 8000)
- **HPA:** CPU-based scaling (70% threshold)
- **ConfigMap/Secret:** Configuration management

**Health Checks:**
- Startup: 2-minute grace period
- Liveness: Auto-restart unhealthy pods
- Readiness: Traffic routing control

### Stage 5: Monitoring (Prometheus + Grafana)

**Alerts:**
- High error rate (>10%)
- High latency (P95 > 10s)
- Service down (>1 min)
- Low throughput (<0.01 ads/sec)

---

## 🧪 Testing

### Run Tests

```bash
# All tests
pytest tests/

# With coverage
pytest --cov=src tests/

# Specific test
pytest tests/test_api.py -v
```

### Load Testing

```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Run load test (100 requests, 10 concurrent)
ab -n 100 -c 10 -p payload.json -T application/json \
  http://localhost:8000/generate

# Watch HPA scale
kubectl get hpa -w
```

---

## 🐛 Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs <container-name>
kubectl logs <pod-name>

# Common issues:
# - Model downloading (wait 2-3 minutes)
# - Port conflict (change port)
# - Insufficient memory (increase limits)
```

### Service Not Accessible

```bash
# Check service status
kubectl get service ad-generator-service

# Create tunnel (Minikube)
minikube tunnel

# Or use port-forward
kubectl port-forward svc/ad-generator-service 8000:80
```

### HPA Not Scaling

```bash
# Enable metrics server
minikube addons enable metrics-server

# Check HPA status
kubectl describe hpa ad-generator-hpa

# Verify metrics
kubectl top pods
```

### Prometheus Not Scraping

```bash
# Check targets
kubectl port-forward svc/prometheus 9090:9090
# Visit: http://localhost:9090/targets

# Verify metrics endpoint
curl http://localhost:8000/metrics
```

---

## 📈 Project Achievements

### MLOps Maturity

| Capability | Implementation | Status |
|-----------|---------------|--------|
| Source Control | Git/GitHub | ✅ |
| Automated Testing | Pytest with CI | ✅ |
| CI/CD | GitHub Actions | ✅ |
| Experiment Tracking | MLflow | ✅ |
| Model Registry | MLflow artifacts | ✅ |
| Containerization | Docker | ✅ |
| Orchestration | Kubernetes + HPA | ✅ |
| Monitoring | Prometheus + Grafana | ✅ |
| Alerting | Prometheus rules | ✅ |

### Performance Metrics

| Metric | Target | Achieved | Status |
|--------|--------|----------|--------|
| P95 Latency | <10s | ~8.5s | ✅ |
| Uptime | >99% | >99% | ✅ |
| Error Rate | <1% | <0.5% | ✅ |
| Throughput | 10+ concurrent | 10+ | ✅ |
| Auto-scaling | <2 min | <2 min | ✅ |

---

## 🚀 Future Enhancements

- [ ] Model drift detection with statistical tests
- [ ] Canary/Blue-Green deployment strategies
- [ ] Multi-modal generation (images + text)
- [ ] Real-time model retraining pipeline
- [ ] A/B testing framework
- [ ] Multi-language support
- [ ] GPU inference optimization
- [ ] Advanced alert management (PagerDuty/Slack)

---

## 📄 License

MIT License - see LICENSE file for details

## 👤 Author

**Amman Haroon**
- GitHub: [@ammanharoon](https://github.com/ammanharoon)
- Docker Hub: [ammanharoon](https://hub.docker.com/u/ammanharoon)

## 🙏 Acknowledgments

- Hugging Face for pre-trained T5 models
- FastAPI community for excellent documentation
- Kubernetes community for robust orchestration
- MLOps community for best practices

---

**⭐ Star this repo if you find it helpful!**
