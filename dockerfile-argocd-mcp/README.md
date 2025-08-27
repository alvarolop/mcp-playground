# ArgoCD MCP Server Docker Image

This directory contains the Dockerfile and build scripts for creating a containerized version of the [ArgoCD MCP server](https://www.npmjs.com/package/argocd-mcp).

## Features

- **Official Red Hat Node.js 22** base image for enterprise compatibility
- **Simple installation** using the published npm package
- **Version control** via build arguments
- **Security-focused** with non-root user
- **Proper labeling** following OCI standards
- **Red Hat UBI base** for enterprise compatibility

## Build Arguments

- `ARGOCD_MCP_VERSION`: npm package version to install (default: `0.3.0`)
- `BUILD_DATE`: Build timestamp (auto-generated)
- `BUILD_REF`: Git commit hash (auto-generated)

## Quick Start

### Using the Build Script (Recommended)

```bash
# Build with default settings (ArgoCD MCP 0.3.0, latest tag)
./build.sh

# Build specific ArgoCD MCP version
./build.sh 0.3.0

# Build with custom tag
./build.sh 0.3.0 latest

# Build with custom registry
./build.sh 0.3.0 latest my-registry.com:5000

# Force rebuild (removes cache and existing image)
./build.sh 0.3.0 latest quay.io/alopezme --force
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
- **Official Red Hat base**: Uses [Red Hat UBI9 Node.js 22](https://catalog.redhat.com/software/containers/ubi9/nodejs-22-minimal/664330aa459a2d3c807ccea9) (full version)
- **Published package**: Uses the official npm package instead of building from source
- **Proper npm permissions**: npm directories have correct ownership and permissions

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

## Troubleshooting

### Build Issues

- Ensure you have `podman` installed
- Check that the ArgoCD MCP version exists on npm
- Verify network access to npm registry
- Ensure you have access to Red Hat container registry

### Runtime Issues

- Check container logs: `podman logs argocd-mcp-server`
- Verify port binding: `podman port argocd-mcp-server`
- Verify ArgoCD connection and API token

### Common npm Errors

#### EACCES Permission Denied for npm Directories

**Error**: `npm error syscall mkdir npm error path /home/mcpuser/.npm/_cacache npm error errno EACCES`

**Cause**: npm cache directories have incorrect ownership or permissions.

**Solution**: This has been comprehensively fixed by:
1. Creating all required npm directories at build time
2. Setting proper ownership to `mcpuser` (UID 1000)
3. Setting proper npm environment variables
4. Using the official Red Hat Node.js 22 image

**Prevention**: Always rebuild the image after Dockerfile changes:
```bash
./build.sh 0.3.0 latest quay.io/alopezme --force
```

## Why This Approach is Better

1. **Official Red Hat support**: Uses the [official Red Hat UBI9 Node.js 22](https://catalog.redhat.com/software/containers/ubi9/nodejs-22-minimal/664330aa459a2d3c807ccea9) image
2. **Simpler**: No need to manage Node.js installation manually
3. **More reliable**: Uses Red Hat's tested and supported Node.js environment
4. **Faster builds**: No Node.js compilation or NVM setup required
5. **Easier maintenance**: Red Hat handles Node.js updates and security patches
6. **Enterprise ready**: Fully compatible with Red Hat Enterprise Linux and OpenShift

## Red Hat UBI9 Node.js 22 Benefits

Using the [official Red Hat UBI9 Node.js 22](https://catalog.redhat.com/software/containers/ubi9/nodejs-22-minimal/664330aa459a2d3c807ccea9) image provides several advantages:

- **Official support**: Red Hat maintains and supports the Node.js runtime
- **Security updates**: Automatic security patches and updates
- **Enterprise compatibility**: Works seamlessly with Red Hat platforms
- **Full runtime**: Includes all necessary Node.js components and tools
- **Certified**: Red Hat certified for enterprise use

## Contributing

To improve this Dockerfile:

1. Test with different ArgoCD MCP versions
2. Verify security best practices
3. Update to newer Red Hat Node.js versions when available
4. Add additional configuration options as needed
