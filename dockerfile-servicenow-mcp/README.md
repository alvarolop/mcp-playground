# ServiceNow MCP Server Docker Image

This directory contains the Dockerfile and build scripts for creating a containerized version of the [servicenow-mcp](https://github.com/echelon-ai-labs/servicenow-mcp).

## Features

- **Multi-stage build** for optimized image size
- **Version control** via build arguments
- **Security-focused** with non-root user
- **Python-based** MCP server implementation
- **Proper labeling** following OCI standards
- **Red Hat UBI base** for enterprise compatibility

## Build Arguments

- `MCP_SERVER_VERSION`: Git tag/branch to build from (default: `main`)
- `MCP_SERVER_REPO`: Repository URL (default: `https://github.com/echelon-ai-labs/servicenow-mcp.git`)
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

- `org.opencontainers.image.title`: ServiceNow MCP Server
- `org.opencontainers.image.description`: Model Context Protocol server for ServiceNow
- `org.opencontainers.image.vendor`: MCP Playground
- `org.opencontainers.image.source`: Source repository
- `org.opencontainers.image.version`: MCP server version
- `org.opencontainers.image.created`: Build timestamp
- `org.opencontainers.image.revision`: Git commit hash
- `org.opencontainers.image.licenses`: License information

## Security Features

- **Non-root user**: Container runs as `mcpuser` (UID 1000)
- **Minimal base image**: Uses `ubi-minimal` for runtime
- **Multi-stage build**: Build dependencies not included in final image
- **Python security**: Uses Red Hat UBI Python packages

## Usage

```bash
# Run the container
podman run -d \
    --name servicenow-mcp-server \
    -p 8080:8080 \
    servicenow-mcp-server:latest

# Run with custom configuration
podman run -d \
    --name servicenow-mcp-server \
    -p 8080:8080 \
    servicenow-mcp-server:latest \
    --host=0.0.0.0 \
    --port=8080
```

## Health Check

The container can be monitored using standard container health checks:

```bash
# Check container health
podman healthcheck run servicenow-mcp-server

# View health status
podman inspect servicenow-mcp-server | jq '.[0].State.Health'
```

## Troubleshooting

### Build Issues

- Ensure you have `podman` installed
- Check that the MCP server version exists in the repository
- Verify network access to GitHub
- Ensure Python 3.11 is available in UBI9

### Runtime Issues

- Check container logs: `podman logs servicenow-mcp-server`
- Verify port binding: `podman port servicenow-mcp-server`
- Check health status: `podman healthcheck run servicenow-mcp-server`
- Verify Python dependencies: `podman exec servicenow-mcp-server pip list`

## Contributing

To improve this Dockerfile:

1. Test with different ServiceNow MCP server versions
2. Verify security best practices
3. Update base images when new versions are available
4. Add additional configuration options as needed
5. Test Python dependency compatibility with UBI9
