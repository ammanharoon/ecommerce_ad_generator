# Canary Deployment Strategy

## Overview
Implements canary deployment with 75% stable / 25% canary traffic split for safe rollouts.

## Architecture
```
Traffic (100%)
    ↓
Service (LoadBalancer)
    ├─→ Stable Pods (3 replicas) → 75% traffic
    └─→ Canary Pod  (1 replica)  → 25% traffic
```

## Traffic Distribution
- **Stable**: 3 replicas = 75% of traffic
- **Canary**: 1 replica = 25% of traffic
- Service uses `app: ad-generator` label to route to both versions

## Deployment Steps

### 1. Initial Deployment (Stable Only)
```bash
# Apply stable version first
kubectl apply -f k8s/canary/deployment-stable.yaml
kubectl apply -f k8s/canary/service.yaml
kubectl apply -f k8s/canary/hpa.yaml

# Wait for stable to be ready
kubectl wait --for=condition=ready pod -l version=stable --timeout=300s

# Verify stable running
kubectl get pods -l app=ad-generator
```

### 2. Deploy Canary Version
```bash
# Tag new image as canary
docker tag ammanharoon/ad-generator-api:latest ammanharoon/ad-generator-api:canary
docker push ammanharoon/ad-generator-api:canary

# Deploy canary (1 pod = 25% traffic)
kubectl apply -f k8s/canary/deployment-canary.yaml

# Wait for canary to be ready
kubectl wait --for=condition=ready pod -l version=canary --timeout=300s
```

### 3. Monitor Canary Performance
```bash
# Watch pod status
kubectl get pods -l app=ad-generator -w

# Check canary logs
kubectl logs -l version=canary --tail=50 -f

# Check stable logs for comparison
kubectl logs -l version=stable --tail=50 -f

# Monitor metrics from both versions
kubectl port-forward svc/ad-generator-service 8080:80

# Access drift detection report
curl http://localhost:8080/drift/report

# Check Prometheus metrics (compare stable vs canary)
curl http://localhost:8080/metrics | grep -E "version|error|duration"
```

### 4. Validate Canary (Success Criteria)
Monitor for 15-30 minutes and check:
- ✅ Error rate < 1% (similar to stable)
- ✅ Response time within 10% of stable
- ✅ No drift alerts (check `/drift/report`)
- ✅ CPU/Memory usage normal
- ✅ No crash loops

```bash
# Get error metrics
kubectl top pods -l app=ad-generator

# Check health endpoints
for pod in $(kubectl get pods -l version=canary -o name); do
  kubectl exec $pod -- curl -s http://localhost:8000/health
done
```

### 5a. Promote Canary (If Validation Passes)
```bash
# Tag canary as new stable
docker tag ammanharoon/ad-generator-api:canary ammanharoon/ad-generator-api:stable
docker push ammanharoon/ad-generator-api:stable

# Update stable deployment to use new image
kubectl set image deployment/ad-generator-stable ad-generator-api=ammanharoon/ad-generator-api:stable

# Wait for rollout
kubectl rollout status deployment/ad-generator-stable

# Delete canary deployment
kubectl delete -f k8s/canary/deployment-canary.yaml

# Verify all traffic on new stable
kubectl get pods -l app=ad-generator
```

### 5b. Rollback Canary (If Validation Fails)
```bash
# Simply delete canary deployment
kubectl delete -f k8s/canary/deployment-canary.yaml

# Traffic automatically returns 100% to stable
kubectl get pods -l app=ad-generator
```

## Traffic Split Adjustments

### 50/50 Split (Testing)
```bash
kubectl scale deployment ad-generator-stable --replicas=2
kubectl scale deployment ad-generator-canary --replicas=2
```

### 90/10 Split (Conservative)
```bash
kubectl scale deployment ad-generator-stable --replicas=9
kubectl scale deployment ad-generator-canary --replicas=1
```

### 10/90 Split (Pre-promotion)
```bash
kubectl scale deployment ad-generator-stable --replicas=1
kubectl scale deployment ad-generator-canary --replicas=9
```

## Monitoring Dashboard Queries

### Prometheus Queries
```promql
# Request rate by version
rate(http_requests_total{app="ad-generator"}[5m])

# Error rate by version
rate(http_requests_total{app="ad-generator",status=~"5.."}[5m])

# P95 latency by version
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{app="ad-generator"}[5m]))

# Active pods by version
count(kube_pod_info{pod=~"ad-generator.*"}) by (pod)
```

### Grafana Dashboard Panels
1. **Traffic Distribution**: Pie chart showing request count by version
2. **Error Rate Comparison**: Line graph comparing stable vs canary errors
3. **Latency Comparison**: P50/P95/P99 latency for both versions
4. **Resource Usage**: CPU/Memory by version
5. **Drift Alerts**: Counter of drift detections

## Automated Canary Analysis (Optional)

For advanced setups, use Flagger for automated canary analysis:
```bash
# Install Flagger
kubectl apply -k github.com/fluxcd/flagger//kustomize/kubernetes

# Create Canary resource
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: ad-generator
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ad-generator-stable
  service:
    port: 80
  analysis:
    interval: 1m
    threshold: 10
    maxWeight: 50
    stepWeight: 10
    metrics:
    - name: request-success-rate
      thresholdRange:
        min: 99
    - name: request-duration
      thresholdRange:
        max: 500
```

## Best Practices
1. **Always deploy stable first** before adding canary
2. **Monitor drift detection** endpoint during canary rollout
3. **Start with small canary** (1 pod) and increase gradually
4. **Set clear success criteria** before deploying canary
5. **Keep stable running** until canary fully validated
6. **Automate rollback** if error rate spikes
7. **Test canary** with synthetic load before real traffic

## Cleanup
```bash
# Remove canary deployment
kubectl delete -f k8s/canary/

# Or keep stable running
kubectl delete deployment ad-generator-canary
```
