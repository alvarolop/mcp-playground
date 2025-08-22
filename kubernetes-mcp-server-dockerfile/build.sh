#!/bin/bash

# Build script for Kubernetes MCP Server Docker image
# Usage: ./build.sh [version] [tag]

set -e

# Default values
MCP_VERSION=${1:-main} # v0.0.49
IMAGE_TAG=${2:-latest} # v0.0.49
REGISTRY=${3:-quay.io/alopezme}

echo "Building Kubernetes MCP Server Docker image..."
echo "MCP Server Version: ${MCP_VERSION}"
echo "Image Tag: ${IMAGE_TAG}"
echo "Registry: ${REGISTRY}"

# Check if logged in to the registry
echo "Checking registry authentication..."
if ! podman login --get-login ${REGISTRY} >/dev/null 2>&1; then
    echo "❌ Not logged in to ${REGISTRY}"
    echo "Please login first with: podman login ${REGISTRY}"
    exit 1
fi
echo "✅ Logged in to ${REGISTRY}"

# Build the image with build arguments
podman build \
    --build-arg MCP_SERVER_VERSION=${MCP_VERSION} \
    --build-arg MCP_SERVER_REPO=https://github.com/containers/kubernetes-mcp-server.git \
    --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
    --build-arg BUILD_REF=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown") \
    -t kubernetes-mcp-server:${IMAGE_TAG} \
    kubernetes-mcp-server-dockerfile

echo "Image built successfully: kubernetes-mcp-server:${IMAGE_TAG}"

# Tag for registry
REGISTRY_IMAGE="${REGISTRY}/kubernetes-mcp-server:${IMAGE_TAG}"
podman tag kubernetes-mcp-server:${IMAGE_TAG} ${REGISTRY_IMAGE}

echo "Image tagged for registry: ${REGISTRY_IMAGE}"

# Optional: push to registry
read -p "Do you want to push the image to the registry? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Pushing image to registry..."
    podman push ${REGISTRY_IMAGE}
    echo "Image pushed successfully!"
else
    echo "Image ready for manual push: podman push ${REGISTRY_IMAGE}"
fi
