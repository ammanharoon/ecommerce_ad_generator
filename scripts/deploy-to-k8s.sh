#!/bin/bash
set -e

echo "🚀 Deploying E-Commerce Ad Generator to Kubernetes"
echo "=================================================="
echo ""

# Get the latest image
IMAGE_TAG=${1:-latest}
IMAGE_NAME="ammanharoon/ad-generator-api: ${IMAGE_TAG}"

echo "📦 Using image: ${IMAGE_NAME}"
echo ""

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl not found. Please install kubectl first."
    exit 1
fi

# Check if cluster is accessible
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Cannot connect to Kubernetes cluster."
    echo "   For Minikube: run 'minikube start'"
    echo "   For cloud:  configure kubectl with cluster credentials"
    exit 1
fi

echo "✅ Connected to Kubernetes cluster"
echo ""

# Apply manifests
echo "📝 Applying Kubernetes manifests..."
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml

echo ""
echo "🔄 Updating deployment image to ${IMAGE_NAME}..."
kubectl set image deployment/ad-generator-deployment \
  ad-generator-api=${IMAGE_NAME} \
  -n default

echo ""
echo "⏳ Waiting for rollout to complete..."
kubectl rollout status deployment/ad-generator-deployment -n default

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📊 Current status:"
kubectl get pods -n default -l app=ad-generator
echo ""
kubectl get service ad-generator-service -n default
echo ""
kubectl get hpa ad-generator-hpa -n default

echo ""
echo "🎯 To access the service:"
echo "   minikube service ad-generator-service --url"
echo ""
echo "   Or create tunnel:"
echo "   minikube tunnel"