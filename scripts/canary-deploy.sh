#!/bin/bash
# Automated Canary Deployment Script

set -e

STABLE_IMAGE="ammanharoon/ad-generator-api:stable"
CANARY_IMAGE="ammanharoon/ad-generator-api:canary"
NAMESPACE="${NAMESPACE:-default}"
CANARY_DURATION="${CANARY_DURATION:-1800}"  # 30 minutes

echo "🚀 Starting Canary Deployment"
echo "================================"

# Step 1: Verify stable deployment is healthy
echo "📊 Step 1: Checking stable deployment health..."
kubectl rollout status deployment/ad-generator-stable -n $NAMESPACE --timeout=60s
STABLE_READY=$(kubectl get deployment ad-generator-stable -n $NAMESPACE -o jsonpath='{.status.readyReplicas}')
echo "✅ Stable deployment ready: $STABLE_READY pods"

# Step 2: Build and push canary image
echo ""
echo "🏗️  Step 2: Building canary image..."
docker build -t $CANARY_IMAGE -f docker/Dockerfile .
docker push $CANARY_IMAGE
echo "✅ Canary image pushed"

# Step 3: Deploy canary
echo ""
echo "🐤 Step 3: Deploying canary (25% traffic)..."
kubectl apply -f k8s/canary/deployment-canary.yaml -n $NAMESPACE
kubectl wait --for=condition=ready pod -l version=canary -n $NAMESPACE --timeout=300s
echo "✅ Canary deployed and ready"

# Step 4: Monitor canary
echo ""
echo "👀 Step 4: Monitoring canary for $CANARY_DURATION seconds..."
echo "   Checking error rate, latency, and drift..."

START_TIME=$(date +%s)
ERRORS=0
MAX_ERRORS=5

while [ $(($(date +%s) - START_TIME)) -lt $CANARY_DURATION ]; do
    ELAPSED=$(($(date +%s) - START_TIME))
    REMAINING=$((CANARY_DURATION - ELAPSED))
    
    echo ""
    echo "⏱️  Time elapsed: ${ELAPSED}s / ${CANARY_DURATION}s (${REMAINING}s remaining)"
    
    # Check pod status
    CANARY_STATUS=$(kubectl get pods -l version=canary -n $NAMESPACE -o jsonpath='{.items[0].status.phase}')
    if [ "$CANARY_STATUS" != "Running" ]; then
        echo "❌ Canary pod not running! Status: $CANARY_STATUS"
        ERRORS=$((ERRORS + 1))
    else
        echo "✅ Canary status: $CANARY_STATUS"
    fi
    
    # Check restart count
    RESTARTS=$(kubectl get pods -l version=canary -n $NAMESPACE -o jsonpath='{.items[0].status.containerStatuses[0].restartCount}')
    if [ "$RESTARTS" -gt 0 ]; then
        echo "⚠️  Canary restarted $RESTARTS times"
        ERRORS=$((ERRORS + 1))
    fi
    
    # Check drift detection (via port-forward in background)
    DRIFT_CHECK=$(kubectl exec -n $NAMESPACE deployment/ad-generator-canary -- curl -s http://localhost:8000/drift/report 2>/dev/null || echo '{"status":"error"}')
    DRIFT_DETECTED=$(echo $DRIFT_CHECK | grep -o '"drift_detected":[^,}]*' | cut -d: -f2 | tr -d ' ')
    
    if [ "$DRIFT_DETECTED" = "true" ]; then
        echo "⚠️  Data drift detected in canary!"
        ERRORS=$((ERRORS + 1))
    else
        echo "✅ No drift detected"
    fi
    
    # Check error threshold
    if [ $ERRORS -ge $MAX_ERRORS ]; then
        echo ""
        echo "❌ CANARY FAILED: Too many errors ($ERRORS/$MAX_ERRORS)"
        echo "🔄 Rolling back canary..."
        kubectl delete -f k8s/canary/deployment-canary.yaml -n $NAMESPACE
        echo "✅ Rollback complete - 100% traffic on stable"
        exit 1
    fi
    
    sleep 60
done

# Step 5: Promote canary
echo ""
echo "🎉 Step 5: Canary validation passed!"
echo "📈 Promoting canary to stable..."

# Tag canary as new stable
docker tag $CANARY_IMAGE $STABLE_IMAGE
docker push $STABLE_IMAGE

# Update stable deployment
kubectl set image deployment/ad-generator-stable ad-generator-api=$STABLE_IMAGE -n $NAMESPACE
kubectl rollout status deployment/ad-generator-stable -n $NAMESPACE --timeout=300s

# Remove canary
kubectl delete -f k8s/canary/deployment-canary.yaml -n $NAMESPACE

echo ""
echo "✅ CANARY PROMOTION COMPLETE"
echo "================================"
echo "All traffic now on new stable version"
kubectl get pods -l app=ad-generator -n $NAMESPACE
