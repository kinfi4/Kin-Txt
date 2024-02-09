#!/bin/bash


charts=(
#    "../charts/kin-statistics"
#    "../charts/kin-builtin-models"
#    "../charts/kin-generic-models"
#    "../charts/kin-model-types"
    "../charts/kin-api-gateway"
#    "../charts/kin-frontend"
)


for chartPath in "${charts[@]}"; do
    echo "Deploying $chartPath ..."

    # Navigate to the chart directory
    cd "$chartPath" || { echo "Failed to navigate to $chartPath"; exit 1; }

    # Install or upgrade the Helm chart
    # Note: This assumes Helm 3, adjust if using Helm 2
    serviceName=$(basename "$chartPath")
    helm upgrade --install "$serviceName" . || { echo "Deployment of $serviceName failed"; exit 1; }

    # Navigate back to the original directory
    cd - || { echo "Failed to navigate back to the original directory"; exit 1; }

    echo "$serviceName deployed successfully."
    echo ""
    echo ""
done

echo "All charts have been deployed."
