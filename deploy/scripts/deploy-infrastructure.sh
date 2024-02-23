#!/bin/bash


install_storage_class() {
    # Check if the 'local-disk' StorageClass already exists
    if kubectl get sc local-disk > /dev/null 2>&1; then
        echo "StorageClass 'local-disk' already exists. Skipping installation."
    else
        echo "Installing StorageClass 'local-disk' from kin-infrastructure chart..."
        helm install kin-infra ../charts/kin-infrastructure
        cd - || exit 1;
        echo "StorageClass 'local-disk' installed."
    fi
}

install_storage_class

# Add the Bitnami Helm repository
helm repo add bitnami https://charts.bitnami.com/bitnami

# Update Helm repositories
helm repo update

echo "Helm repositories updated successfully."

# Deploy RabbitMQ
helm install rabbitmq bitnami/rabbitmq \
  --set auth.username=kin-txt-user \
  --set auth.password=kin-txt-password \
  --set service.type=ClusterIP \
  --set fullnameOverride=rabbitmq \
  || { echo "Deployment of RabbitMQ failed"; exit 1; }
echo "RabbitMQ deployed successfully."

# Deploy MongoDB
helm install mongo bitnami/mongodb \
  --set auth.rootPassword=kin-txt-password \
  --set architecture=standalone \
  --set persistence.enabled=true \
  --set persistence.size=2Gi \
  --set fullnameOverride=mongo \
  || { echo "Deployment of MongoDB failed"; exit 1; }
echo "MongoDB deployed successfully."

# Deploy PostgreSQL
helm upgrade --install postgres bitnami/postgresql \
  --set image.tag=9.6 \
  --set persistence.enabled=true \
  --set persistence.size=1Gi \
  --set fullnameOverride=postgres \
  || { echo "Deployment of PostgreSQL failed"; exit 1; }
echo "PostgreSQL deployed successfully."

# Deploy Redis
helm install redis bitnami/redis \
  --set architecture=standalone \
  --set command[0]="redis-server",command[1]="--save",command[2]="20 1",command[3]="--loglevel",command[4]="warning" \
  --set persistence.enabled=true \
  --set persistence.size=1Gi \
  --set fullnameOverride=redis \
  || { echo "Deployment of Redis failed"; exit 1; }
echo "Redis deployed successfully."
