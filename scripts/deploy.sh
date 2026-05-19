#!/bin/bash

echo "Loading image into Minikube..."
minikube image load safety-net-backend:v3

echo "Deploying to Kubernetes..."
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml

echo "Checking Pods..."
kubectl get pods