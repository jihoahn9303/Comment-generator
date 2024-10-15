# Make all targets .PHONY
.PHONY: $(shell sed -n -e '/^$$/ { n ; /^[^ .\#][^ ]*:/ { s/:.*$$// ; p ; } ; }' $(MAKEFILE_LIST))

include envs/huggingface.env
include envs/gcp.env
include envs/fastapi.env
export

SHELL := /usr/bin/env bash
HOSTNAME := $(shell hostname)

ifeq (, $(shell which docker-compose))
	DOCKER_COMPOSE_COMMAND = docker compose
else
	DOCKER_COMPOSE_COMMAND = docker-compose
endif

## Returns true if the stem is a non-empty environment variable, or else raises an error.
guard-%:
	@#$(or ${$*}, $(error $* is not set))

## Create GCP VM Instance 
generate-vm-instance: push
	./scripts/create-server.sh

## Build docker container with docker-compose
build:
	$(DOCKER_COMPOSE_COMMAND) build

## Push docker image to GCP Artifact Registry. Requires IMAGE_TAG to be specified.
push: guard-IMAGE_TAG build
	@gcloud auth configure-docker asia-northeast3-docker.pkg.dev --quiet
	@docker tag "${DOCKER_IMAGE_NAME}:latest" "$${GCP_DOCKER_REGISTRY_URL}:$${IMAGE_TAG}"
	@docker push "$${GCP_DOCKER_REGISTRY_URL}:$${IMAGE_TAG}"
