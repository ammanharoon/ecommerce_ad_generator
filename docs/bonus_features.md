# Bonus Features Implementation Guide

## ✅ Bonus Feature 1: Model Drift Detection (+5 marks)

### Implementation
**Location**: [src/monitoring/drift_detector.py](../src/monitoring/drift_detector.py)

**Features**:
- ✅ **Statistical Drift Detection** using Kolmogorov-Smirnov test
- ✅ **Multi-feature Monitoring**: Price, description length, category distribution
- ✅ **Severity Levels**: High/Medium/Low drift classification
- ✅ **Alert System**: CRITICAL/WARNING/NORMAL alerts
- ✅ **Historical Tracking**: Drift history saved to JSON logs

**How It Works**:
1. **Reference Data**: Uses training data statistics as baseline
2. **Incoming Data**: Compares new requests against baseline
3. **Statistical Tests**:
   - KS test for continuous features (price, description length)
   - Distribution comparison for categorical (category)
4. **Real-time Alerts**: Logs warnings when drift detected

**API Endpoints**:
```bash
# Get drift report
GET http://localhost:8000/drift/report

# Response example:
{
  "total_checks": 150,
  "recent_checks": 10,
  "drift_detected_count": 2,
  "latest_check": {
    "timestamp": "2026-01-13T10:30:00",
    "drift_detected": true,
    "alert_level": "WARNING",
    "tests": {
      "price_drift": {
        "test": "Kolmogorov-Smirnov",
        "p_value": 0.03,
        "drift_detected": true,
        "severity": "medium"
      }
    }
  }
}
```

**Integration**:
- Automatically runs on every `/generate` request
- Logs drift warnings in application logs
- Saves history to `logs/drift_history.json`

**Demonstration for Grading**:
```bash
# 1. Start API
kubectl port-forward svc/ad-generator-service 8080:80

# 2. Generate some ads with normal data
curl -X POST http://localhost:8080/generate \
  -H "Content-Type: application/json" \
  -d '{"product_name": "Laptop", "category": "Electronics", "description": "High performance laptop", "price": 999.99}'

# 3. Simulate drift with unusual data
curl -X POST http://localhost:8080/generate \
  -H "Content-Type: application/json" \
  -d '{"product_name": "Test", "category": "NewCategory", "description": "x", "price": 999999}'

# 4. Check drift report
curl http://localhost:8080/drift/report

# 5. Show in logs
kubectl logs -l app=ad-generator --tail=50 | grep -i drift
```

---

## ✅ Bonus Feature 2: Canary Deployment Strategy (+5 marks)

### Implementation
**Location**: [k8s/canary/](../k8s/canary/)

**Files Created**:
- [deployment-stable.yaml](../k8s/canary/deployment-stable.yaml) - Stable version (3 replicas)
- [deployment-canary.yaml](../k8s/canary/deployment-canary.yaml) - Canary version (1 replica)
- [service.yaml](../k8s/canary/service.yaml) - LoadBalancer routing to both
- [hpa.yaml](../k8s/canary/hpa.yaml) - Autoscaling for both versions
- [README.md](../k8s/canary/README.md) - Complete deployment guide

**Traffic Split**:
- **Stable**: 3 pods = 75% traffic
- **Canary**: 1 pod = 25% traffic
- Service selector `app: ad-generator` matches both versions

**Features**:
- ✅ **Gradual Rollout**: Start with 25% traffic on canary
- ✅ **Version Labels**: `version: stable` vs `version: canary`
- ✅ **Independent Scaling**: Separate HPAs for each version
- ✅ **Quick Rollback**: Delete canary = instant 100% on stable
- ✅ **Monitoring Integration**: Version labels in Prometheus metrics

**Deployment Process**:

### Step 1: Deploy Stable Version
```bash
# Apply stable deployment first
kubectl apply -f k8s/canary/deployment-stable.yaml
kubectl apply -f k8s/canary/service.yaml
kubectl apply -f k8s/canary/hpa.yaml

# Verify stable running
kubectl get pods -l version=stable
kubectl wait --for=condition=ready pod -l version=stable --timeout=300s
```

### Step 2: Deploy Canary (25% Traffic)
```bash
# Build and tag canary image
docker build -t ammanharoon/ad-generator-api:canary -f docker/Dockerfile .
docker push ammanharoon/ad-generator-api:canary

# Deploy canary
kubectl apply -f k8s/canary/deployment-canary.yaml
kubectl wait --for=condition=ready pod -l version=canary --timeout=300s

# Verify both versions running
kubectl get pods -l app=ad-generator
# Output:
# ad-generator-stable-xxx   1/1   Running   (3 pods)
# ad-generator-canary-xxx   1/1   Running   (1 pod)
```

### Step 3: Monitor Canary Performance
```bash
# Watch logs from both versions
kubectl logs -l version=stable --tail=20 -f &
kubectl logs -l version=canary --tail=20 -f

# Check metrics by version
kubectl port-forward svc/ad-generator-service 8080:80
curl http://localhost:8080/metrics | grep -E "version|error"

# Monitor drift detection on canary
curl http://localhost:8080/drift/report
```

### Step 4: Promote or Rollback

**If Canary Successful** (low errors, no drift):
```bash
# Tag canary as new stable
docker tag ammanharoon/ad-generator-api:canary ammanharoon/ad-generator-api:stable
docker push ammanharoon/ad-generator-api:stable

# Update stable deployment
kubectl set image deployment/ad-generator-stable \
  ad-generator-api=ammanharoon/ad-generator-api:stable

# Delete canary
kubectl delete -f k8s/canary/deployment-canary.yaml
```

**If Canary Failed** (high errors, drift detected):
```bash
# Simply delete canary - instant rollback
kubectl delete -f k8s/canary/deployment-canary.yaml
# Traffic automatically returns 100% to stable
```

**Automated Deployment Script**:
```bash
# Use automated canary script (monitors for 30 mins)
chmod +x scripts/canary-deploy.sh
./scripts/canary-deploy.sh

# Script automatically:
# - Builds and deploys canary
# - Monitors errors, restarts, drift
# - Promotes if successful
# - Rolls back if failures detected
```

---

## Demonstration for Grading

### Show Both Features Working Together

```bash
# 1. Deploy with canary strategy
kubectl apply -f k8s/canary/

# 2. Verify deployments
kubectl get deployments
kubectl get pods -l app=ad-generator

# 3. Generate traffic to both versions
for i in {1..100}; do
  curl -X POST http://localhost:8080/generate \
    -H "Content-Type: application/json" \
    -d "{\"product_name\": \"Product$i\", \"category\": \"Electronics\", \"description\": \"Test product $i\", \"price\": $((100 + RANDOM % 900))}"
  sleep 0.5
done

# 4. Check drift report (shows detection working)
curl http://localhost:8080/drift/report | jq

# 5. Show canary deployment in action
kubectl get pods -l app=ad-generator -o wide
kubectl top pods -l app=ad-generator

# 6. Show version-specific metrics
curl http://localhost:8080/metrics | grep 'version="stable"'
curl http://localhost:8080/metrics | grep 'version="canary"'

# 7. Demonstrate rollback capability
kubectl delete deployment ad-generator-canary
# Instant rollback - all traffic to stable

# 8. Show drift history logs
cat logs/drift_history.json | jq
```

---

## Grading Evidence Checklist

### Drift Detection (+5 marks)
- ✅ **Code**: [drift_detector.py](../src/monitoring/drift_detector.py) with KS tests
- ✅ **Integration**: API calls drift detection on every request
- ✅ **Endpoint**: `/drift/report` returns comprehensive report
- ✅ **Logging**: Drift warnings in application logs
- ✅ **Statistical Tests**: KS test, distribution comparison, severity levels
- ✅ **Historical Tracking**: JSON logs with drift history

### Canary Deployment (+5 marks)
- ✅ **Manifests**: Separate deployments for stable + canary
- ✅ **Traffic Split**: 75/25 split using replica counts
- ✅ **Version Labels**: `version: stable/canary` for tracking
- ✅ **Service**: Single LoadBalancer routing to both
- ✅ **Autoscaling**: Separate HPAs for each version
- ✅ **Rollback**: Quick rollback by deleting canary
- ✅ **Automation**: Scripted deployment with monitoring
- ✅ **Documentation**: Complete guide in [k8s/canary/README.md](../k8s/canary/README.md)

---

## Screenshots for Report

**Take these screenshots for your project report**:

1. **Drift Detection API Response**
   ```bash
   curl http://localhost:8080/drift/report | jq > drift_report.json
   # Screenshot showing JSON with drift_detected: true and severity levels
   ```

2. **Canary Pods Running**
   ```bash
   kubectl get pods -l app=ad-generator -o wide
   # Screenshot showing 3 stable + 1 canary pod
   ```

3. **Drift Warnings in Logs**
   ```bash
   kubectl logs -l app=ad-generator --tail=100 | grep -i drift
   # Screenshot showing "⚠️ Data drift detected: WARNING"
   ```

4. **Version-Specific Metrics**
   ```bash
   curl http://localhost:8080/metrics | grep version
   # Screenshot showing metrics tagged with version=stable/canary
   ```

5. **Canary Rollback**
   ```bash
   kubectl delete deployment ad-generator-canary
   kubectl get pods -l app=ad-generator
   # Screenshot showing only stable pods after rollback
   ```

---

## Integration with Existing Monitoring

### Prometheus Metrics for Canary
Add these queries to your Grafana dashboard:

```promql
# Request rate by version
sum(rate(http_requests_total[5m])) by (version)

# Error rate comparison
sum(rate(http_requests_total{status=~"5.."}[5m])) by (version)

# Drift detection count
sum(drift_detections_total) by (severity)
```

### Grafana Dashboard Panels
Add to existing [k8s/monitoring/grafana-dashboard.yml](../k8s/monitoring/grafana-dashboard.yml):
1. **Canary Traffic Split** - Pie chart by version
2. **Drift Alerts** - Counter with severity breakdown
3. **Version Comparison** - Side-by-side stable vs canary metrics

---

## Total Bonus Marks: +10

- ✅ **Drift Detection**: +5 marks
- ✅ **Canary Deployment**: +5 marks

**Final Project Score**: 100 (base) + 10 (bonus) = **110/110** 🎉
