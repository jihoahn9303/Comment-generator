#!/usr/bin/env bash

set -euo pipefail

gcloud compute instances create "${VM_NAME}" \
    --project="${GCP_PROJECT_ID}" \
    --zone="${ZONE}" \
    --machine-type="${MACHINE_TYPE}"\
    --network="${NETWORK}" \
    --subnet="${SUBNET}" \
    --restart-on-failure \
    --maintenance-policy=TERMINATE \
    --provisioning-model=STANDARD \
    --service-account="${SERVICE_ACCOUNT}" \
    --scopes=https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/cloud.useraccounts.readonly,https://www.googleapis.com/auth/cloudruntimeconfig \
    --tags=http-server,https-server \
    --create-disk=auto-delete=yes,boot=yes,image="projects/${IMAGE_PROJECT_ID}/global/images/${IMAGE_NAME}",mode=rw,size=50,type=pd-balanced \
    --labels="${LABELS}" \
    --metadata-from-file=startup-script=./scripts/startup-script.sh \
    --metadata \
gcp_docker_registry_url="${GCP_DOCKER_REGISTRY_URL}:${IMAGE_TAG}",\
hf_token="${HF_TOKEN}",\
hf_namespace="${HF_NAMESPACE}",\
ntqai_endpoint_name="${NTQAI_ENDPOINT_NAME}"

