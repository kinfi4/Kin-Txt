#!/bin/bash

# Define the tag based on the latest Git commit hash
tag=$(git rev-parse --short HEAD)

# But currently we don't use tags for local k8s runs
tag=""

function build_and_push() {
  service_dir=$1
  service_name=$2
  docker_username="kinfi4"

  # Navigate to the service directory
  cd "$service_dir" || exit

  # Build the Docker image
  docker build -f ./etc/Dockerfile -t $docker_username/"$service_name":"$tag" .

  # Push the Docker image to Docker Hub
  docker push $docker_username/"$service_name":"$tag"

  # Navigate back to the original directory
  cd - || exit
}

build_and_push "kin-api-gateway" "kin-api-gateway"
build_and_push "kin-builtin-models-reports-builder" "kin-builtin-models-reports-builder"
build_and_push "kin-frontend" "kin-frontend"
build_and_push "kin-generic-reports-builder" "kin-generic-reports-builder"
build_and_push "kin-model-types" "kin-model-types"
build_and_push "kin-statistics" "kin-statistics"
