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

### Namespace Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `namespace.create` | Whether to create a new namespace | `true` |
| `namespace.name` | Name of the namespace to create or use | `intelligent-cd` |

### MCP Server Settings

| Parameter | Description | Default |
|-----------|-------------|---------|
| `mcpServer.port` | Port for the MCP server to listen on | `8080` |
| `mcpServer.disableDestructive` | Disable destructive operations | `true` |
| `mcpServer.logLevel` | Log level (0-9) | `5` |
| `mcpServer.args` | Arguments to pass to the command | `["--sse-port", "8080", "--disable-destructive", "--log-level", "5"]` |
| `mcpServer.serviceAccount.create` | Whether to create a new service account | `true` |
| `mcpServer.serviceAccount.name` | Service account name (only used if create=true) | `ocp-mcp-server` |

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

### Environment Variables

| Parameter | Description | Default |
|-----------|-------------|---------|
| `env` | List of environment variables to add to the container | `[]` |

Example environment variables configuration:
```yaml
env:
  - name: DEBUG
    value: "true"
  - name: API_KEY
    valueFrom:
      secretKeyRef:
        name: my-secret
        key: api-key
```

## Customizing Arguments

Different MCP servers may require different command-line arguments. You can customize the arguments in the values:

```yaml
mcpServer:
  # Custom arguments for your MCP server
  args:
    - "--config"
    - "/etc/mcp/config.yaml"
    - "--port"
    - "9090"
    - "--log-level"
    - "7"
```

**Note**: The command is fixed to `./kubernetes-mcp-server`. If you need to use a different MCP server binary, you'll need to modify the container image accordingly.

## Service Account Configuration

The chart provides flexible service account configuration:

1. **Default behavior** (`create: true`, no name specified): Creates a service account with the default name "ocp-mcp-server"
2. **Custom existing service account** (`create: false`, name specified): Uses an existing service account with the specified name
3. **Custom new service account** (`create: true`, name specified): Creates a new service account with the specified name

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
