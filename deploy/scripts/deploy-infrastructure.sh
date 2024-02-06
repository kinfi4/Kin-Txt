#!/bin/bash

# Add the Bitnami Helm repository
helm repo add bitnami https://charts.bitnami.com/bitnami

# Update Helm repositories
helm repo update

echo "Helm repositories updated successfully."

# Deploy RabbitMQ
helm install rabbitmq bitnami/rabbitmq \
  --set image.tag=3-management \
  --set auth.username=kin-news-user \
  --set auth.password=kin-news-password \
  --set service.type=ClusterIP \
  || { echo "Deployment of RabbitMQ failed"; exit 1; }
echo "RabbitMQ deployed successfully."

# Deploy MongoDB
helm install mongo bitnami/mongodb \
  --set image.tag=6.0.3 \
  --set auth.rootUsername=kin-news-user \
  --set auth.rootPassword=kin-news-password \
  --set architecture=standalone \
  --set persistence.enabled=true \
  --set persistence.size=2Gi \
  --set persistence.storageClass=local-storage \
  || { echo "Deployment of MongoDB failed"; exit 1; }
echo "MongoDB deployed successfully."

# Deploy PostgreSQL
helm install postgres bitnami/postgresql \
  --set image.tag=9.6 \
  --set persistence.enabled=true \
  --set persistence.size=1Gi \
  --set postgresqlUsername=kin-news-user \
  --set postgresqlPassword=kin-news-password \
  --set postgresqlDatabase=kin-news \
  --set persistence.storageClass=local-storage \
  || { echo "Deployment of PostgreSQL failed"; exit 1; }
echo "PostgreSQL deployed successfully."

# Deploy Redis
helm install redis bitnami/redis \
  --set image.tag=6.2-alpine \
  --set architecture=standalone \
  --set master.command="redis-server --save 20 1 --loglevel warning" \
  --set persistence.enabled=true \
  --set persistence.size=1Gi \
  --set persistence.storageClass=local-storage \
  || { echo "Deployment of Redis failed"; exit 1; }
echo "Redis deployed successfully."
