#!/bin/bash

# Build script for ArgoCD MCP Server Docker image
# Usage: ./build.sh [argocd_version] [tag] [registry] [--force]

set -e

# Default values
ARGOCD_MCP_VERSION=${1:-0.3.0} # 0.3.0
IMAGE_TAG=${2:-latest} # latest
REGISTRY=${3:-quay.io/alopezme}
FORCE_REBUILD=${4:-}

echo "Building ArgoCD MCP Server Docker image..."
echo "ArgoCD MCP Version: ${ARGOCD_MCP_VERSION}"
echo "Node.js Version: 22 (from Red Hat UBI9 nodejs-22)"
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

# Build arguments
BUILD_ARGS=(
    --build-arg ARGOCD_MCP_VERSION=${ARGOCD_MCP_VERSION}
    --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
    --build-arg BUILD_REF=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
)

# Add force rebuild if requested
if [[ "${FORCE_REBUILD}" == "--force" ]]; then
    echo "🔄 Force rebuild requested - removing existing image..."
    podman rmi ${REGISTRY}/argocd-mcp:${IMAGE_TAG} 2>/dev/null || true
    BUILD_ARGS+=(--no-cache)
fi

# Build the image with build arguments
echo "🔨 Building image..."
podman build \
    "${BUILD_ARGS[@]}" \
    -t ${REGISTRY}/argocd-mcp:${IMAGE_TAG} \
    dockerfile-argocd-mcp

echo "✅ Image built successfully: argocd-mcp:${IMAGE_TAG}"
echo "Image tagged for registry: ${REGISTRY}/argocd-mcp:${IMAGE_TAG}"

# Optional: push to registry
read -p "Do you want to push the image to the registry? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📤 Pushing image to registry..."
    podman push ${REGISTRY}/argocd-mcp:${IMAGE_TAG}
    echo "✅ Image pushed successfully!"
else
    echo "📋 Image ready for manual push: podman push ${REGISTRY}/argocd-mcp:${IMAGE_TAG}"
fi
