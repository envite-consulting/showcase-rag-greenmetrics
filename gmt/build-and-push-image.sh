#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

IMAGE_REPO="${IMAGE_REPO:-enviteconsulting/showcase-rag-greenmetrics}"
IMAGE_TAG="${1:-${IMAGE_TAG:-demo}}"
DOCKER_PLATFORM="${DOCKER_PLATFORM:-linux/amd64}"
IMAGE_REF="${IMAGE_REPO}:${IMAGE_TAG}"

echo "Building ${IMAGE_REF} for ${DOCKER_PLATFORM}..."
docker build \
  --platform "${DOCKER_PLATFORM}" \
  --file "${REPO_ROOT}/docker/Dockerfile" \
  --tag "${IMAGE_REF}" \
  "${REPO_ROOT}"

echo "Pushing ${IMAGE_REF}..."
docker push "${IMAGE_REF}"

echo "Done: ${IMAGE_REF}"
