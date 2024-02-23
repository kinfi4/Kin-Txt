#!/bin/bash

# Navigate to the project root directory
cd "$(dirname "$0")/../.."

# Point Docker CLI to Minikube's Docker daemon
eval $(minikube docker-env)

# List of your service directories
services=(
  "kin-api-gateway"
  "kin-builtin-models-reports-builder"
  "kin-frontend"
  "kin-generic-reports-builder"
  "kin-model-types"
  "kin-statistics"
)

# Loop through each service and build the Docker image
for service in "${services[@]}"; do
  echo "Building Docker image for $service..."
  cd "$(dirname "$0")/../../$service"

  docker build -t "$service:latest" -f "./etc/service/Dockerfile" .

  cd -

  echo "$service image built successfully."
done

echo "All Docker images have been built and are available in Minikube."
