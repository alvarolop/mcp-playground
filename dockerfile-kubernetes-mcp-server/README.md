# Kubernetes MCP Server Docker Image

This directory contains the Dockerfile and build scripts for creating a containerized version of the [kubernetes-mcp-server](https://github.com/containers/kubernetes-mcp-server).

## Features

- **Multi-stage build** for optimized image size
- **Version control** via build arguments
- **Security-focused** with non-root user
- **Health checks** for container monitoring
- **Proper labeling** following OCI standards
- **Red Hat UBI base** for enterprise compatibility

## Build Arguments

- `MCP_SERVER_VERSION`: Git tag/branch to build from (default: `main`)
- `MCP_SERVER_REPO`: Repository URL (default: official repo)
- `BUILD_DATE`: Build timestamp (auto-generated)
- `BUILD_REF`: Git commit hash (auto-generated)

## Quick Start

### Using the Build Script (Recommended)

```bash
# Build with default settings (main branch, latest tag)
./build.sh

# Build specific version
./build.sh v0.1.0

# Build with custom tag
./build.sh v0.1.0 stable

# Build with custom registry
./build.sh v0.1.0 stable my-registry.com:5000
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

## Usage

```bash
# Run the container
podman run -d \
    --name mcp-server \
    -p 8080:8080 \
    kubernetes-mcp-server:latest

# Run with custom configuration
podman run -d \
    --name mcp-server \
    -p 8080:8080 \
    kubernetes-mcp-server:latest \
    --sse-port 8080 \
    --log-level 9 \
    --disable-destructive
```

## Health Check

The container includes a health check that runs every 30 seconds:

```bash
# Check container health
podman healthcheck run mcp-server

# View health status
podman inspect mcp-server | jq '.[0].State.Health'
```

## Troubleshooting

### Build Issues

- Ensure you have `podman` installed
- Check that the MCP server version exists in the repository
- Verify network access to GitHub

### Runtime Issues

- Check container logs: `podman logs mcp-server`
- Verify port binding: `podman port mcp-server`
- Check health status: `podman healthcheck run mcp-server`

## Contributing

To improve this Dockerfile:

1. Test with different MCP server versions
2. Verify security best practices
3. Update base images when new versions are available
4. Add additional configuration options as needed
