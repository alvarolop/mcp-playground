# 🔧 Deploy MCP Server on ServiceNow

This section covers deploying the ServiceNow MCP server for integration with ServiceNow instances.

## Overview

Learn how to deploy the ServiceNow MCP server to enable AI agents to interact with ServiceNow instances through the Model Context Protocol.

## Prerequisites

- Access to a ServiceNow instance
- ServiceNow admin credentials
- [OpenShift CLI (oc)](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html) or [Kubernetes CLI (kubectl)](https://kubernetes.io/docs/tasks/tools/)
- [Helm](https://helm.sh/docs/intro/install/) for package management
- [Podman](https://podman.io/getting-started/installation) for container management
- Access to a container registry (e.g., Quay.io, Docker Hub)

## Step 1: Building and pushing the Container Image

First, build the ServiceNow MCP Server image and push it to your container registry.

```bash
# Build and tag the image
./dockerfile-servicenow-mcp/build.sh latest quay.io/alopezme
```

> **Note:** The build script will prompt you to push the image to the registry.

## Step 2: Deploying the MCP Server

Deploy the ServiceNow MCP server to your Kubernetes cluster using the Helm chart.

```bash
# Configure ServiceNow credentials
SERVICENOW_INSTANCE_URL="https://your-instance.service-now.com"
SERVICENOW_USERNAME="your-username"
SERVICENOW_PASSWORD="your-password"

# Deploy the MCP server
helm template mcp-server-chart --values mcp-server-chart/values-servicenow.yaml \
  --set env[0].name=SERVICENOW_INSTANCE_URL --set env[0].value="$SERVICENOW_INSTANCE_URL" \
  --set env[1].name=SERVICENOW_USERNAME --set env[1].value="$SERVICENOW_USERNAME" \
  --set env[2].name=SERVICENOW_PASSWORD --set env[2].value="$SERVICENOW_PASSWORD" \
  | oc apply -f -
```

## Step 3: Verify Deployment

```bash
# Check the MCP server pod is running
oc get pods -n intelligent-cd

# Check the service is created
oc get svc -n intelligent-cd
```

## Next Steps

Continue to 🗄️ [Deploy Milvus Vector Database](05-deploy-milvus.md) section ➡️
