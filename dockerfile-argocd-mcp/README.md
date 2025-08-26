# ArgoCD MCP Server Docker Image

This directory contains the Dockerfile and build scripts for creating a containerized version of the [ArgoCD MCP server](https://github.com/akuity/argocd-mcp).

## Features

- **Multi-stage build** for optimized image size
- **Version control** via build arguments
- **Security-focused** with non-root user
- **Health checks** for container monitoring
- **Proper labeling** following OCI standards
- **Red Hat UBI base** for enterprise compatibility
- **Node.js runtime** optimized for ArgoCD MCP operations

## Build Arguments

- `MCP_SERVER_VERSION`: Git tag/branch to build from (default: `main`)
- `MCP_SERVER_REPO`: Repository URL (default: official ArgoCD MCP repo)
- `NODE_VERSION`: Node.js version to use (default: `18`)
- `BUILD_DATE`: Build timestamp (auto-generated)
- `BUILD_REF`: Git commit hash (auto-generated)

## Quick Start

### Using the Build Script (Recommended)

```bash
# Build with default settings (main branch, latest tag)
./build.sh

# Build specific version
./build.sh v0.3.0

# Build with custom tag
./build.sh v0.3.0 stable

# Build with custom registry
./build.sh v0.3.0 stable my-registry.com:5000
```

## Image Labels

The built image includes comprehensive metadata:

- `org.opencontainers.image.title`: Image title
- `org.opencontainers.image.description`: Description
- `org.opencontainers.image.vendor`: Vendor information
- `org.opencontainers.image.source`: Source repository
- `org.opencontainers.image.version`: MCP server version
- `org.opencontainers.image.created`: Build timestamp
- `org.opencontainers.image.revision`: Git commit hash
- `org.opencontainers.image.licenses`: License information

## Security Features

- **Non-root user**: Container runs as `mcpuser` (UID 1000)
- **Minimal base image**: Uses `ubi-minimal` for runtime
- **Health checks**: Built-in health monitoring
- **Multi-stage build**: Build dependencies not included in final image
- **Production-only npm install**: Only production dependencies included

## Usage

```bash
# Run the container
podman run -d \
    --name argocd-mcp-server \
    -p 8080:8080 \
    -e ARGOCD_BASE_URL="https://your-argocd-instance.com" \
    -e ARGOCD_API_TOKEN="your-api-token" \
    argocd-mcp-server:latest

# Run with custom configuration
podman run -d \
    --name argocd-mcp-server \
    -p 8080:8080 \
    -e ARGOCD_BASE_URL="https://your-argocd-instance.com" \
    -e ARGOCD_API_TOKEN="your-api-token" \
    -e MCP_READ_ONLY="true" \
    argocd-mcp-server:latest
```

## Environment Variables

The ArgoCD MCP server requires the following environment variables:

- `ARGOCD_BASE_URL`: URL of your ArgoCD instance
- `ARGOCD_API_TOKEN`: API token for ArgoCD authentication
- `MCP_READ_ONLY`: Set to "true" to disable write operations (optional)
- `NODE_TLS_REJECT_UNAUTHORIZED`: Set to "0" for self-signed certificates (optional)

## Health Check

The container includes a health check that runs every 30 seconds:

```bash
# Check container health
podman healthcheck run argocd-mcp-server

# View health status
podman inspect argocd-mcp-server | jq '.[0].State.Health'
```

## Troubleshooting

### Build Issues

- Ensure you have `podman` installed
- Check that the MCP server version exists in the repository
- Verify network access to GitHub
- Ensure Node.js version is compatible

### Runtime Issues

- Check container logs: `podman logs argocd-mcp-server`
- Verify port binding: `podman port argocd-mcp-server`
- Check health status: `podman healthcheck run argocd-mcp-server`
- Verify ArgoCD connection and API token

## Contributing

To improve this Dockerfile:

1. Test with different MCP server versions
2. Verify security best practices
3. Update base images when new versions are available
4. Add additional configuration options as needed
5. Test with different Node.js versions
