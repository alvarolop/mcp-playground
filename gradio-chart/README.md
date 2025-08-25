# Gradio Helm Chart

A simplified Helm chart for deploying Gradio applications in OpenShift/Kubernetes.

## Features

- **Namespace Management**: Automatic namespace creation with configurable name and labels
- **Gradio Application Deployment**: Deploy Gradio apps with essential configuration
- **Flexible Exposure**: Choose between no exposure, Ingress, or OpenShift Route
- **OpenShift Compatibility**: Full support for OpenShift 4.18+ with automatic security contexts
- **Security**: OpenShift-compatible security policies (automatically configured)

## Prerequisites

- Kubernetes 1.19+ or OpenShift 4.6+
- Helm 3.0+
- Ingress controller (e.g., nginx-ingress) for Ingress exposure

## Installation

### Basic Installation

```bash
# Install the chart (creates namespace automatically)
helm install my-gradio gradio-chart/gradio-chart \
  --namespace intelligent-cd \
  --create-namespace
```

### Installation with Custom Values

```bash
helm install my-gradio gradio-chart/gradio-chart \
  --namespace intelligent-cd \
  --create-namespace \
  --values custom-values.yaml
```

### Installation with Route Exposure

```bash
# For OpenShift with Route exposure
helm install my-gradio gradio-chart/gradio-chart \
  --namespace intelligent-cd \
  --create-namespace \
  --set exposure.type=route \
  --set exposure.host="gradio.apps.your-cluster.com"
```

## Configuration

### Namespace Configuration

```yaml
namespace:
  # Create namespace automatically
  create: true
  # Namespace name (default: intelligent-cd)
  name: "intelligent-cd"
```

### Gradio Configuration

```yaml
gradio:
  appFile: "app.py"
  appFunction: "demo"
  title: "My Gradio App"
  description: "A simple Gradio application"
```

### Exposure Configuration

```yaml
exposure:
  # Type of exposure: none, ingress, or route
  type: "route"
  # Hostname for ingress or route (optional)
  host: "gradio.apps.example.com"
```

**Exposure Types:**
- **`none`**: No external exposure (use port-forward for access)
- **`ingress`**: Use Kubernetes Ingress (requires nginx-ingress controller)
- **`route`**: Use OpenShift Route (automatically configured with edge TLS)

## Example Values Files

### Basic Gradio App (No External Exposure)

```yaml
# basic-gradio.yaml
namespace:
  create: true
  name: "intelligent-cd"

gradio:
  appFile: "app.py"
  appFunction: "demo"
  title: "Hello World"
  description: "A simple Gradio app"

exposure:
  type: "none"
```

### Ingress Exposure

```yaml
# ingress-gradio.yaml
namespace:
  create: true
  name: "intelligent-cd"

gradio:
  appFile: "app.py"
  appFunction: "demo"
  title: "Hello World"
  description: "A simple Gradio app"

exposure:
  type: "ingress"
  host: "gradio.local"
```

### OpenShift Route Exposure

```yaml
# route-gradio.yaml
namespace:
  create: true
  name: "intelligent-cd"

gradio:
  appFile: "app.py"
  appFunction: "demo"
  title: "My Gradio App"
  description: "A simple Gradio application"

exposure:
  type: "route"
  host: "gradio.apps.your-cluster.com"
```

## Usage Examples

### 1. Deploy with No External Exposure

```bash
# Create a simple values file
cat > simple-values.yaml << EOF
namespace:
  create: true
  name: "intelligent-cd"

gradio:
  appFile: "app.py"
  appFunction: "demo"
  title: "Hello World"
  description: "A simple Gradio app"

exposure:
  type: "none"
EOF

# Install the chart
helm install hello-gradio gradio-chart/gradio-chart \
  --values simple-values.yaml \
  --namespace intelligent-cd \
  --create-namespace
```

### 2. Deploy with OpenShift Route

```bash
# Create values file for OpenShift Route
cat > route-values.yaml << EOF
namespace:
  create: true
  name: "intelligent-cd"

gradio:
  appFile: "app.py"
  appFunction: "demo"
  title: "My Gradio App"
  description: "A simple Gradio application"

exposure:
  type: "route"
  host: "gradio.apps.your-cluster.com"
EOF

# Install on OpenShift
helm install route-gradio gradio-chart/gradio-chart \
  --values route-values.yaml \
  --namespace intelligent-cd \
  --create-namespace
```

## What You Get

1. **Namespace**: Automatically created with configurable name
2. **Gradio Application**: Your Python app running in a container
3. **Service**: Internal ClusterIP service for the Gradio app
4. **Exposure**: Configurable external access (none/ingress/route)
5. **Health Checks**: Liveness and readiness probes
6. **Security**: Automatically configured OpenShift-compatible security contexts

## Security Features

- **Automatically configured** for OpenShift 4.18+ compatibility
- **Non-root execution** for all containers
- **Dropped capabilities** for enhanced security
- **Works on both Kubernetes and OpenShift** clusters

## Troubleshooting

### Common Issues

1. **Pod not starting**: Check resource limits and security contexts
2. **Ingress/Route not working**: Verify ingress controller or OpenShift router
3. **Security context issues**: Security contexts are automatically configured

### Debug Commands

```bash
# Check namespace
kubectl get namespace intelligent-cd

# Check pod status
kubectl get pods -n your-namespace

# View logs
kubectl logs -f deployment/gradio-app -n your-namespace

# Check exposure resources
kubectl get ingress -n your-namespace
# or for OpenShift
oc get route -n your-namespace

# Test connectivity
kubectl exec -it deployment/gradio-app -n your-namespace -- curl localhost:7860

# Check security contexts
kubectl describe pod -l app.kubernetes.io/name=gradio-chart -n your-namespace
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the Apache License 2.0.

## Support

For support and questions:

- Create an issue in the repository
- Check the documentation
- Review the troubleshooting section

## Changelog

### Version 0.5.0
- **Simplified exposure configuration** - Single `exposure.type` selector (none/ingress/route)
- **Removed OpenShift toggle** - Always OpenShift-compatible
- **Hardcoded service type** - Always ClusterIP
- **Removed pod customization** - No more podLabels or podAnnotations
- **Simplified TLS** - Route TLS always edge termination
- **Cleaner configuration** - Streamlined values file

### Version 0.4.0
- **Simplified chart structure** - Removed MCP server components
- **Removed Kubernetes API access** - Now focused on pure Gradio deployment
- **Removed RBAC and service account complexity** - Uses default service account
- **Streamlined configuration** - Cleaner, simpler values file
- **Maintained OpenShift compatibility** - Security contexts and routes still work

### Version 0.3.0
- Added automatic namespace creation
- Added OpenShift 4.18+ compatibility
- Added OpenShift Route support
- **Automatically configured security contexts** for both Kubernetes and OpenShift
- **Simplified service account configuration** (main app uses default)
- Enhanced security for OpenShift environments

### Version 0.2.0
- Simplified to MVP configuration
- Focused on Gradio + Kubernetes API access
- Removed complex LLM/RAG features
- Streamlined templates and configuration

### Version 0.1.0
- Initial release with basic Gradio deployment
