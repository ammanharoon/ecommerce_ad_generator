#!/bin/bash
echo "Setting up MLflow..."
mkdir -p mlruns
mkdir -p mlartifacts
export MLFLOW_TRACKING_URI=http://localhost:5000
echo "MLflow directories created"
echo "Starting MLflow UI on port 5000..."
echo "Access UI at: http://localhost:5000"
mlflow ui --host 0.0.0.0 --port 5000