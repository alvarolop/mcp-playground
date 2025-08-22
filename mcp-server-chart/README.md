# Kubernetes MCP Server Chart

This Helm chart deploys the [kubernetes-mcp-server](https://github.com/containers/kubernetes-mcp-server) on Kubernetes/OpenShift clusters.

## What is the Kubernetes MCP Server?

The Kubernetes MCP Server is a Model Context Protocol (MCP) server that allows AI agents to interact with Kubernetes clusters. It provides a standardized interface for AI tools to query and manage Kubernetes resources.

## Prerequisites

- Kubernetes 1.19+ or OpenShift 4.6+
- Helm 3.0+
- Access to the container image registry

## Quick Start

```bash
helm template mcp-server ./kubernetes-mcp-server-chart | oc apply -f -
```

## Configuration

### MCP Server Settings

| Parameter | Description | Default |
|-----------|-------------|---------|
| `mcpServer.port` | Port for the MCP server to listen on | `8080` |
| `mcpServer.disableDestructive` | Disable destructive operations | `true` |
| `mcpServer.logLevel` | Log level (0-9) | `5` |
| `mcpServer.serviceAccountName` | Service account name | `ocp-mcp` |

### Security Settings

| Parameter | Description | Default |
|-----------|-------------|---------|
| `rbac.clusterRole` | Cluster role to bind | `edit` |
| `namespace` | Deployment namespace | `intelligent-cd` |

### Basic Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of replicas | `1` |
| `image.repository` | Container image repository | `quay.io/alopezme/kubernetes-mcp-server` |
| `image.tag` | Container image tag | `latest` |
| `image.pullPolicy` | Image pull policy | `IfNotPresent` |


## Security Considerations

- **RBAC**: The default configuration uses `edit` role. Consider creating a custom role with minimal required permissions for production use.
- **Network Policies**: Consider implementing network policies to restrict traffic to/from the MCP server.
- **Pod Security**: The chart runs containers as non-root users by default.
- **Image Security**: Use signed images and implement image scanning in your CI/CD pipeline.

## Contributing

To improve this chart:

1. Test with different Kubernetes versions
2. Add additional configuration options
3. Improve security defaults
4. Add more comprehensive health checks
5. Implement proper monitoring and alerting
