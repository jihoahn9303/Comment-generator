#!/usr/bin/env bash

GCP_DOCKER_REGISTRY_URL=$(curl --silent http://metadata.google.internal/computeMetadata/v1/instance/attributes/gcp_docker_registry_url -H "Metadata-Flavor: Google")
HF_TOKEN=$(curl --silent http://metadata.google.internal/computeMetadata/v1/instance/attributes/hf_token -H "Metadata-Flavor: Google")
HF_NAMESPACE=$(curl --silent http://metadata.google.internal/computeMetadata/v1/instance/attributes/hf_namespace -H "Metadata-Flavor: Google")
NTQAI_ENDPOINT_NAME=$(curl --silent http://metadata.google.internal/computeMetadata/v1/instance/attributes/ntqai_endpoint_name -H "Metadata-Flavor: Google")

curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

echo '=========== Downloading Docker Image ============'
gcloud auth configure-docker --quiet asia-northeast3-docker.pkg.dev
echo "GCP_DOCKER_REGISTERY_URL = ${GCP_DOCKER_REGISTRY_URL}"
time sudo docker pull "${GCP_DOCKER_REGISTRY_URL}"

sudo docker run --init \
  --network host \
  --ipc host \
  --user root \
  --hostname "$(hostname)" --privileged \
  --log-driver=gcplogs \
  -e HF_TOKEN="${HF_TOKEN}" \
  -e HF_NAMESPACE="${HF_NAMESPACE}" \
  -e NTQAI_ENDPOINT_NAME="${NTQAI_ENDPOINT_NAME}" \
  ${GCP_DOCKER_REGISTRY_URL}
