#!/bin/bash

# Build script for ArgoCD MCP Server Docker image
# Usage: ./build.sh [version] [tag]

set -e

# Default values
MCP_VERSION=${1:-main} # v0.3.0
IMAGE_TAG=${2:-latest} # v0.3.0
REGISTRY=${3:-quay.io/alopezme}

echo "Building ArgoCD MCP Server Docker image..."
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
    --build-arg MCP_SERVER_REPO=https://github.com/akuity/argocd-mcp.git \
    --build-arg NODE_VERSION=22.18.0 \
    --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
    --build-arg BUILD_REF=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown") \
    -t ${REGISTRY}/argocd-mcp:${IMAGE_TAG} \
    dockerfile-argocd-mcp

echo "Image built successfully: argocd-mcp:${IMAGE_TAG}"

echo "Image tagged for registry: ${REGISTRY}/argocd-mcp:${IMAGE_TAG}"

# Optional: push to registry
read -p "Do you want to push the image to the registry? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Pushing image to registry..."
    podman push ${REGISTRY}/argocd-mcp:${IMAGE_TAG}
    echo "Image pushed successfully!"
else
    echo "Image ready for manual push: podman push ${REGISTRY}/argocd-mcp:${IMAGE_TAG}"
fi
