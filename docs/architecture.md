Copilot said: ## 📚 **STAGE-BY-STAGE DOCUMENTATION** I'll provide each document
📚 STAGE-BY-STAGE DOCUMENTATION
I'll provide each document separately so you can copy easily.

DOCUMENT 1: PROJECT_OVERVIEW. md
Markdown
# E-Commerce Ad Creative Generator - Project Overview

## Problem Statement

### Business Challenge
E-commerce businesses struggle with creating engaging, personalized product advertisements at scale. Manual ad creation is: 
- **Time-consuming:** Hours per product
- **Expensive:** Requires copywriting expertise
- **Inconsistent:** Quality varies across products
- **Unscalable:** Cannot handle thousands of products

### Solution
An end-to-end MLOps system that automatically generates high-quality ad copy for e-commerce products using fine-tuned language models, with complete production infrastructure including monitoring, scaling, and continuous deployment.

## System Requirements

### Functional Requirements

#### 1. Data Pipeline
- **FR-1.1:** Ingest e-commerce product data (name, category, description, price)
- **FR-1.2:** Preprocess and clean product information
- **FR-1.3:** Generate synthetic training data for model fine-tuning
- **FR-1.4:** Automate data pipeline orchestration with scheduling

#### 2. Machine Learning Model
- **FR-2.1:** Fine-tune T5 transformer model for ad generation
- **FR-2.2:** Accept product metadata as input
- **FR-2.3:** Generate compelling ad copy (50-200 characters)
- **FR-2.4:** Support multiple product categories
- **FR-2.5:** Inference time < 10 seconds per product

#### 3. API Service
- **FR-3.1:** RESTful API for ad generation
- **FR-3.2:** Single product generation endpoint
- **FR-3.3:** Batch product generation endpoint
- **FR-3.4:** Health check and monitoring endpoints
- **FR-3.5:** Interactive API documentation (Swagger)

#### 4. MLOps Infrastructure
- **FR-4.1:** Track experiments with MLflow
- **FR-4.2:** Version control for models
- **FR-4.3:** Containerize application with Docker
- **FR-4.4:** Automated CI/CD pipeline
- **FR-4.5:** Deploy to Kubernetes with auto-scaling
- **FR-4.6:** Real-time monitoring with Prometheus
- **FR-4.7:** Visualization with Grafana dashboards

### Non-Functional Requirements

#### Performance
- **NFR-1.1:** API response time < 10s for single generation
- **NFR-1.2:** Support 10+ concurrent requests
- **NFR-1.3:** System uptime > 99%
- **NFR-1.4:** Auto-scale from 1-5 pods based on CPU (70% threshold)

#### Scalability
- **NFR-2.1:** Horizontal scaling via Kubernetes HPA
- **NFR-2.2:** Handle 100+ products in batch mode
- **NFR-2.3:** Stateless architecture for easy scaling

#### Reliability
- **NFR-3.1:** Health checks (liveness, readiness, startup probes)
- **NFR-3.2:** Graceful failure handling
- **NFR-3.3:** Automatic pod restart on failure
- **NFR-3.4:** Alert on high error rate (>10%)

#### Observability
- **NFR-4.1:** Track 15+ custom Prometheus metrics
- **NFR-4.2:** Real-time Grafana dashboards
- **NFR-4.3:** Alert rules for performance degradation
- **NFR-4.4:** Comprehensive logging

#### Security
- **NFR-5.1:** Kubernetes Secrets for sensitive data
- **NFR-5.2:** ConfigMaps for configuration
- **NFR-5.3:** CORS middleware for API
- **NFR-5.4:** Resource limits to prevent DoS

#### Maintainability
- **NFR-6.1:** Modular code structure
- **NFR-6.2:** Type hints and documentation
- **NFR-6.3:** Automated testing in CI/CD
- **NFR-6.4:** Code linting (flake8)

## System Constraints

### Technical Constraints
- **TC-1:** Python 3.11 runtime environment
- **TC-2:** T5-base model (220M parameters)
- **TC-3:** CPU-only inference (cost optimization)
- **TC-4:** Docker image size < 3GB
- **TC-5:** Kubernetes 1.28+

### Resource Constraints
- **RC-1:** Memory: 1Gi request, 4Gi limit per pod
- **RC-2:** CPU: 500m request, 2000m limit per pod
- **RC-3:** Storage: ephemeral (no persistent volumes)

### Business Constraints
- **BC-1:** Free tier infrastructure (Minikube for demo)
- **BC-2:** Cloud-ready for production (AWS EKS/GCP GKE/Azure AKS)
- **BC-3:** Open-source technologies only

## Success Metrics

### Model Performance
- **M-1:** Generated ads are grammatically correct (>95%)
- **M-2:** Ads include product name and price
- **M-3:** Ads are contextually relevant to category

### System Performance
- **M-4:** P95 latency < 10 seconds
- **M-5:** Error rate < 1%
- **M-6:** Auto-scaling response time < 2 minutes

### MLOps Maturity
- **M-7:** Automated CI/CD pipeline (100% coverage)
- **M-8:** Comprehensive monitoring (15+ metrics)
- **M-9:** Zero-downtime deployments
- **M-10:** Experiment tracking for all training runs

## Target Users

### Primary Users
- **E-commerce Product Managers:** Bulk ad generation
- **Marketing Teams:** Campaign ad copy creation
- **Developers:** API integration

### Secondary Users
- **Data Scientists:** Model experimentation
- **DevOps Engineers:** Infrastructure management
- **Business Analysts:** Performance monitoring

## Out of Scope

- Real-time model retraining
- Multi-language support
- Image generation (text-only)
- A/B testing framework
- User authentication/authorization
- Production database integration
DOCUMENT 2: ARCHITECTURE. md
Markdown
# System Architecture

## High-Level Architecture

┌─────────────────────────────────────────────────────────────────┐ │ USER / CLIENT │ │ (Browser / API Client) │ └────────────────────────────┬────────────────────────────────────┘ │ │ HTTPS Request ▼ ┌─────────────────────────────────────────────────────────────────┐ │ KUBERNETES CLUSTER │ │ │ │ ┌────────────────────────────────────────────────────────┐ │ │ │ LoadBalancer Service │ │ │ │ (External Access: Port 80) │ │ │ └──────────────────────┬─────────────────────────────────┘ │ │ │ │ │ ▼ │ │ ┌────────────────────────────────────────────────────────┐ │ │ │ Ad Generator Deployment (1-5 pods) │ │ │ │ ┌──────────┐ ┌──────────┐ ┌──────────┐ │ │ │ │ │ Pod 1 │ │ Pod 2 │ │ Pod N │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ FastAPI │ │ FastAPI │ │ FastAPI │ │ │ │ │ │ T5 Model │ │ T5 Model │ │ T5 Model │ │ │ │ │ │ /metrics │ │ /metrics │ │ /metrics │ │ │ │ │ └──────────┘ └──────────┘ └──────────┘ │ │ │ └────────────────────┬───────────────────────────────────┘ │ │ │ │ │ │ Metrics Scraping │ │ ▼ │ │ ┌────────────────────────────────────────────────────────┐ │ │ │ Prometheus (Monitoring) │ │ │ │ - Scrapes metrics every 15s │ │ │ │ - Stores time-series data │ │ │ │ - Evaluates alert rules │ │ │ └────────────────────┬───────────────────────────────────┘ │ │ │ │ │ │ Data Source │ │ ▼ │ │ ┌────────────────────────────────────────────────────────┐ │ │ │ Grafana (Visualization) │ │ │ │ - Custom ML dashboards │ │ │ │ - Real-time metrics visualization │ │ │ │ - Alert management │ │ │ └────────────────────────────────────────────────────────┘ │ │ │ │ ┌────────────────────────────────────────────────────────┐ │ │ │ Horizontal Pod Autoscaler (HPA) │ │ │ │ - Monitors CPU/Memory │ │ │ │ - Scales pods 1-5 based on 70% CPU threshold │ │ │ └────────────────────────────────────────────────────────┘ │ │ │ │ ┌────────────────────────────────────────────────────────┐ │ │ │ ConfigMap & Secrets │ │ │ │ - Environment variables │ │ │ │ - Model configuration │ │ │ │ - API keys (Secrets) │ │ │ └────────────────────────────────────────────────────────┘ │ └──────────────────────────────────────────────────────────────────┘

Code

## Data Flow Diagram

┌──────────────┐ │ Raw Product │ │ Data │ │ (CSV/JSON) │ └──────┬───────┘ │ │ 1. Ingestion ▼ ┌──────────────────────────────────────────┐ │ Apache Airflow DAG │ │ ┌────────────────────────────────────┐ │ │ │ Task 1: data_ingestion │ │ │ │ - Load product data │ │ │ │ - Validate schema │ │ │ └────────────┬───────────────────────┘ │ │ │ │ │ ▼ │ │ ┌────────────────────────────────────┐ │ │ │ Task 2: data_preprocessing │ │ │ │ - Clean text │ │ │ │ - Handle missing values │ │ │ │ - Standardize formats │ │ │ └────────────┬───────────────────────┘ │ │ │ │ │ ▼ │ │ ┌────────────────────────────────────┐ │ │ │ Task 3: feature_engineering │ │ │ │ - Create input prompts │ │ │ │ - Generate target ads │ │ │ └────────────┬───────────────────────┘ │ │ │ │ │ ▼ │ │ ┌────────────────────────────────────┐ │ │ │ Task 4: data_validation │ │ │ │ - Quality checks │ │ │ │ - Statistics logging │ │ │ └────────────┬───────────────────────┘ │ └───────────────┼──────────────────────────┘ │ │ 2. Processed Data ▼ ┌────────────────┐ │ Training Data │ │ (processed/) │ └────────┬───────┘ │ │ 3. Model Training ▼ ┌────────────────────────────────────────────┐ │ Model Training Pipeline │ │ ┌──────────────────────────────────────┐ │ │ │ 1. Load T5-base model │ │ │ │ (google/flan-t5-base) │ │ │ └──────────────┬───────────────────────┘ │ │ │ │ │ ▼ │ │ ┌──────────────────────────────────────┐ │ │ │ 2. Fine-tune on product data │ │ │ │ - 3 epochs │ │ │ │ - Batch size: 4 │ │ │ │ - Learning rate: 5e-5 │ │ │ └──────────────┬───────────────────────┘ │ │ │ │ │ ▼ │ │ ┌──────────────────────────────────────┐ │ │ │ 3. Log to MLflow │ │ │ │ - Hyperparameters │ │ │ │ - Metrics (loss, perplexity) │ │ │ │ - Model artifacts │ │ │ └──────────────┬───────────────────────┘ │ └─────────────────┼────────────────────────────┘ │ │ 4. Model Artifact ▼ ┌──────────────────┐ │ Trained Model │ │ (checkpoints/) │ └────────┬──────────┘ │ │ 5. Containerization ▼ ┌──────────────────────────────────────────────┐ │ Docker Image Build │ │ ┌────────────────────────────────────────┐ │ │ │ 1. Base: python:3.11-slim │ │ │ │ 2. Install dependencies │ │ │ │ 3. Copy source code │ │ │ │ 4. Download T5 model │ │ │ │ 5. Expose port 8000 │ │ │ └────────────┬───────────────────────────┘ │ └───────────────┼──────────────────────────────┘ │ │ 6. Push to Registry ▼ ┌──────────────────┐ │ Docker Hub │ │ ammanharoon/ │ │ ad-generator-api │ └────────┬─────────┘ │ │ 7. Deploy ▼ ┌──────────────────────────────────────────────┐ │ Kubernetes Deployment │ │ ┌────────────────────────────────────────┐ │ │ │ Pull image from Docker Hub │ │ │ │ Create pods (1-5 replicas) │ │ │ │ Expose via LoadBalancer │ │ │ │ Configure HPA │ │ │ │ Mount ConfigMaps/Secrets │ │ │ └────────────┬───────────────────────────┘ │ └───────────────┼──────────────────────────────┘ │ │ 8. API Request ▼ ┌──────────────────┐ │ API Endpoint │ │ POST /generate │ └────────┬──────────┘ │ │ 9. Inference ▼ ┌────────────────────────────────────────────┐ │ Ad Generation Process │ │ ┌──────────────────────────────────────┐ │ │ │ 1. Receive product data │ │ │ │ {name, category, desc, price} │ │ │ └──────────────┬───────────────────────┘ │ │ │ │ │ ▼ │ │ ┌──────────────────────────────────────┐ │ │ │ 2. Format prompt │ │ │ │ "Generate ad for [product]..." │ │ │ └──────────────┬───────────────────────┘ │ │ │ │ │ ▼ │ │ ┌──────────────────────────────────────┐ │ │ │ 3. Tokenize input │ │ │ │ (T5Tokenizer) │ │ │ └──────────────┬───────────────────────┘ │ │ │ │ │ ▼ │ │ ┌──────────────────────────────────────┐ │ │ │ 4. Model inference │ │ │ │ (T5ForConditionalGeneration) │ │ │ └──────────────┬───────────────────────┘ │ │ │ │ │ ▼ │ │ ┌──────────────────────────────────────┐ │ │ │ 5. Decode output │ │ │ │ "Amazing product! Get 20% off..."│ │ │ └──────────────┬───────────────────────┘ │ │ │ │ │ ▼ │ │ ┌──────────────────────────────────────┐ │ │ │ 6. Track metrics │ │ │ │ - Latency, throughput │ │ │ │ - Quality (length, word count) │ │ │ └──────────────┬───────────────────────┘ │ └─────────────────┼────────────────────────────┘ │ │ 10. Response ▼ ┌──────────────────┐ │ Generated Ad │ │ + Metadata │ │ (JSON Response) │ └───────────────────┘

Code

## MLOps Pipeline

┌──────────────────────────────────────────────────────────────────┐ │ CONTINUOUS INTEGRATION │ └──────────────────────────────────────────────────────────────────┘ │ │ git push ▼ ┌─────────────────┐ │ GitHub Repo │ └────────┬────────┘ │ │ Webhook trigger ▼ ┌─────────────────────────────────────────────────────────────────┐ │ GitHub Actions Workflow │ │ │ │ ┌────────────────────────────────────────────────────────┐ │ │ │ Stage 1: Test & Lint │ │ │ │ ✓ Run pytest (unit tests) │ │ │ │ ✓ Flake8 linting │ │ │ │ ✓ Code quality checks │ │ │ └────────────────────┬───────────────────────────────────┘ │ │ │ Pass │ │ ▼ │ │ ┌────────────────────────────────────────────────────────┐ │ │ │ Stage 2: Build Docker Image │ │ │ │ ✓ Multi-stage build │ │ │ │ ✓ Download model │ │ │ │ ✓ Tag with commit SHA │ │ │ └────────────────────┬───────────────────────────────────┘ │ │ │ Success │ │ ▼ │ │ ┌────────────────────────────────────────────────────────┐ │ │ │ Stage 3: Push to Docker Hub │ │ │ │ ✓ docker push ammanharoon/ad-generator-api:latest │ │ │ │ ✓ docker push ammanharoon/ad-generator-api: <sha> │ │ │ └────────────────────┬───────────────────────────────────┘ │ │ │ Complete │ │ ▼ │ │ ┌────────────────────────────────────────────────────────┐ │ │ │ Stage 4: Validate K8s Manifests │ │ │ │ ✓ kubectl apply --dry-run=client │ │ │ │ ✓ Syntax validation │ │ │ └────────────────────┬───────────────────────────────────┘ │ └───────────────────────┼──────────────────────────────────────────┘ │ │ Trigger deployment ▼ ┌─────────────────────────────────────────────────────────────────┐ │ CONTINUOUS DEPLOYMENT │ │ │ │ ┌────────────────────────────────────────────────────────┐ │ │ │ Kubernetes Cluster │ │ │ │ │ │ │ │ 1. Pull new image from Docker Hub │ │ │ │ 2. Rolling update strategy: │ │ │ │ - Create new pod with new image │ │ │ │ - Wait for health checks to pass │ │ │ │ - Route traffic to new pod │ │ │ │ - Terminate old pod │ │ │ │ - Repeat for all replicas │ │ │ │ │ │ │ │ ✓ Zero downtime deployment │ │ │ │ ✓ Automatic rollback on failure │ │ │ └─────────────────────────────────────────────────────────┘ │ └─────────────────────────────────────────────────────────────────┘ │ ▼ ┌─────────────────────────────────────────────────────────────────┐ │ CONTINUOUS MONITORING │ │ │ │ Prometheus: Collect metrics every 15s │ │ ├─ Request rate, latency, errors │ │ ├─ Model performance (generation time) │ │ ├─ System metrics (CPU, memory, uptime) │ │ └─ Business metrics (ads generated, categories) │ │ │ │ Grafana: Visualize & Alert │ │ ├─ Real-time dashboards │ │ ├─ Alert on high error rate (>10%) │ │ ├─ Alert on high latency (>10s) │ │ └─ Alert on service down │ │ │ │ MLflow: Track experiments │ │ ├─ Model versions │ │ ├─ Hyperparameters │ │ ├─ Training metrics │ │ └─ Model artifacts │ └─────────────────────────────────────────────────────────────────┘

Code

## Component Diagram

┌────────────────────────────────────────────────────────────────┐ │ APPLICATION LAYER │ ├────────────────────────────────────────────────────────────────┤ │ │ │ ┌──────────────────┐ ┌──────────────────┐ │ │ │ FastAPI App │◄─────┤ API Schemas │ │ │ │ (app.py) │ │ (Pydantic) │ │ │ └────────┬─────────┘ └──────────────────┘ │ │ │ │ │ │ uses │ │ ▼ │ │ ┌─────────────────────────────────────────┐ │ │ │ Ad Generation Service │ │ │ │ (service.py) │ │ │ │ - generate_ad() │ │ │ │ - generate_batch() │ │ │ │ - get_health() │ │ │ └────────┬────────────────────────────────┘ │ │ │ uses │ │ ▼ │ │ ┌─────────────────────────────────────────┐ │ │ │ Model Inference │ │ │ │ (inference.py) │ │ │ │ - AdCreativeGenerator │ │ │ │ - load_model() │ │ │ │ - generate() │ │ │ └────────┬────────────────────────────────┘ │ │ │ uses │ │ ▼ │ │ ┌─────────────────────────────────────────┐ │ │ │ T5 Model (Transformers) │ │ │ │ - T5ForConditionalGeneration │ │ │ │ - T5Tokenizer │ │ │ └─────────────────────────────────────────┘ │ │ │ └─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐ │ MONITORING LAYER │ ├─────────────────────────────────────────────────────────────────┤ │ │ │ ┌──────────────────┐ ┌──────────────────┐ │ │ │ Prometheus Client│◄─────┤ Custom Metrics │ │ │ │ │ │ (metrics.py) │ │ │ │ - Counters │ │ - track_request()│ │ │ │ - Histograms │ │ - track_gen() │ │ │ │ - Gauges │ │ - track_error() │ │ │ └──────────────────┘ └──────────────────┘ │ │ │ └─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐ │ DATA LAYER │ ├─────────────────────────────────────────────────────────────────┤ │ │ │ ┌──────────────────┐ ┌──────────────────┐ │ │ │ Data Pipeline │◄─────┤ Airflow DAG │ │ │ │ (pipeline.py) │ │ (ad_generator_dag)│ │ │ │ │ │ │ │ │ │ - ingest() │ │ Tasks: │ │ │ │ - preprocess() │ │ 1. ingestion │ │ │ │ - validate() │ │ 2. preprocessing │ │ │ └──────────────────┘ │ 3. feature_eng │ │ │ │ 4. validation │ │ │ └──────────────────┘ │ │ │ └─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐ │ INFRASTRUCTURE LAYER │ ├─────────────────────────────────────────────────────────────────┤ │ │ │ Docker Kubernetes Monitoring │ │ ┌────────┐ ┌────────────┐ ┌─────────┐ │ │ │Dockerfile│──builds──►│ Deployment │◄─scrapes─│Prometheus│ │ │ └────────┘ │ Service │ └────┬────┘ │ │ │ HPA │ │ │ │ │ ConfigMap │ ┌────▼────┐ │ │ │ Secret │ │ Grafana │ │ │ └────────────┘ └─────────┘ │ │ │ └─────────────────────────────────────────────────────────────────┘

Code

## Technology Stack

### Core Technologies
| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Language** | Python | 3.11 | Primary language |
| **ML Framework** | PyTorch | 2.5.1 | Model training |
| **Transformer** | Hugging Face Transformers | 4.36.2 | T5 model |
| **API Framework** | FastAPI | 0.108.0 | REST API |
| **ASGI Server** | Uvicorn | 0.25.0 | Production server |

### MLOps Tools
| Tool | Version | Purpose |
|------|---------|---------|
| **MLflow** | 2.9.2 | Experiment tracking |
| **Apache Airflow** | 2.7.3 | Pipeline orchestration |
| **Docker** | 24.0+ | Containerization |
| **Kubernetes** | 1.28+ | Orchestration |
| **Prometheus** | 2.48.0 | Metrics collection |
| **Grafana** | 10.2.0 | Visualization |

### Infrastructure
| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Container Registry** | Docker Hub | Image storage |
| **CI/CD** | GitHub Actions | Automation |
| **Local K8s** | Minikube | Development |
| **Cloud K8s** | GKE/EKS/AKS | Production (optional) |

## Deployment Architecture

### Development Environment
Local Machine ├── Python 3.11 venv ├── Airflow (localhost: 8080) ├── MLflow (localhost:5000) └── FastAPI (localhost:8000)

Code

### Production Environment
Kubernetes Cluster ├── Namespace: default ├── Deployments │ ├── ad-generator (1-5 replicas) │ ├── prometheus (1 replica) │ └── grafana (1 replica) ├── Services │ ├── ad-generator-service (LoadBalancer) │ ├── prometheus (NodePort: 30090) │ └── grafana (NodePort:30030) ├── ConfigMaps │ ├── ad-generator-config │ ├── prometheus-config │ └── grafana-datasources ├── Secrets │ └── ad-generator-secret └── HPA └── ad-generator-hpa (1-5 pods, 70% CPU)

Code

## Security Architecture

### Network Security
- CORS middleware on API
- LoadBalancer for external access
- Internal cluster networking for services
- NodePort for monitoring tools (development only)

### Data Security
- Kubernetes Secrets for sensitive data
- ConfigMaps for non-sensitive configuration
- No persistent storage (stateless design)
- Environment variable injection

### Resource Security
- Resource limits prevent DoS
- Namespace isolation
- RBAC for Prometheus service account
- Health checks prevent unhealthy pods from receiving traffic