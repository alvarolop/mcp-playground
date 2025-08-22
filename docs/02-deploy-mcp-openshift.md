# ☸️ Deploy MCP Server on Kubernetes

This section covers deploying the MCP server on Kubernetes for production use.

> **Note:** This guide is based on the [OpenDataHub LLaMA Stack Demos - OpenShift MCP](https://github.com/opendatahub-io/llama-stack-demos/blob/main/kubernetes/mcp-servers/openshift-mcp/README.md) GitHub article, which provides comprehensive examples of deploying MCP servers on OpenShift.

## Overview

Learn how to deploy the [kubernetes-mcp-server](https://github.com/containers/kubernetes-mcp-server) on Kubernetes, configure it properly, and ensure it's accessible for your AI agents. This deployment will enable AI tools to interact with your Kubernetes cluster through the Model Context Protocol.

## Prerequisites

- Access to a Kubernetes cluster
- [OpenShift CLI (oc)](https://docs.redhat.com/en/documentation/openshift_container_platform/latest/html/cli_tools/openshift-cli-oc#cli-getting-started) or [Kubernetes CLI (kubectl)](https://kubernetes.io/docs/tasks/tools/)
- [Helm](https://helm.sh/docs/intro/install/) for package management
- [Podman](https://podman.io/getting-started/installation) for container management
- Access to a container registry (e.g., Quay.io, Docker Hub)


## Step 1: Building and pushing the Container Image

First, build the MCP Server image and push it to your container registry. This step creates a containerized version of the kubernetes-mcp-server that can be deployed to Kubernetes.

```bash
# Build and tag the image with version v0.0.49
./kubernetes-mcp-server-dockerfile/build.sh v0.0.49 v0.0.49
```

> **Note:** The build script will prompt you to push the image to the registry.

## Step 2: Deploying the MCP Server

Deploy the MCP server to your Kubernetes cluster using the Helm chart. This will create all necessary resources including the deployment, service, and RBAC configuration.

```bash
helm template ocp-mcp ./mcp-server-chart | oc apply -f -
```

After a few seconds, you should see the MCP server running:

```bash
# Verify the MCP server pod is running
oc get pods -n intelligent-cd

# Verify the service is created
oc get svc -n intelligent-cd
```






## 🛠️ Troubleshooting: Testing the MCP Server

To verify the MCP server is running and test its functionality, follow these steps. This will help you confirm the deployment was successful and the server can respond to requests.


### Step 1: Port Forwarding

Forward the port 8080 of the MCP server to your local machine. This allows you to test the MCP server from your local environment without exposing it externally.

```bash
oc port-forward svc/ocp-mcp 8080:8080 -n intelligent-cd
```

### Step 2: Listing the available tools

```bash
curl -sX POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json,text/event-stream" \
  -H "Mcp-Session-Id: test-session-$(date +%s)" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list",
    "params": {}
  }' | jq '.result.tools[].name'
```

### Step 3: Test the MCP Server Tools

Based on the [kubernetes-mcp-server documentation](https://github.com/containers/kubernetes-mcp-server/tree/v0.0.49), use the `pods_list` tool to list all pods in the cluster:

```bash
curl -sX POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json,text/event-stream" \
  -H "Mcp-Session-Id: test-session-$(date +%s)" \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
      "name": "pods_list",
      "arguments": {}
    }
  }' | jq -r '.result.content[0].text'
```



## Next Steps

Continue to 🌐 [Deploy Gradio Interface on OpenShift](03-deploy-gradio-openshift.md) section ➡️
