# 🗄️ Deploy Milvus Vector Database

This section covers setting up Milvus for storing and retrieving vector embeddings to enable RAG capabilities.

## Overview

Learn how to deploy Milvus vector database on OpenShift to support Retrieval-Augmented Generation (RAG) functionality in your MCP-powered chatbot.

## Prerequisites

- OpenShift cluster with MCP server and Gradio interface deployed
- [OpenShift CLI (oc)](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html)
- [Helm](https://helm.sh/docs/intro/install/) for package management
- Cluster admin privileges or sufficient permissions to create namespaces and deploy operators

## What is Milvus?

Milvus is an open-source vector database designed for AI applications. It provides:
- **High-performance vector similarity search** - Optimized for fast similarity queries
- **Scalable architecture** - Supports both standalone and distributed deployments
- **Multiple similarity metrics** - Cosine, Euclidean, IP (Inner Product), and more
- **Real-time search capabilities** - Low-latency vector operations
- **Cloud-native design** - Built with Kubernetes in mind


## Step 1: Install Milvus Operator

### Option A: Install on Minikube

```bash
# Add the Milvus Operator Helm repository
helm repo add milvus-operator https://zilliztech.github.io/milvus-operator/
helm repo update milvus-operator

# Install Milvus Operator
helm -n milvus-operator upgrade --install --create-namespace milvus-operator milvus-operator/milvus-operator

# Verify operator installation
kubectl get pods -n milvus-operator
```

### Option B: Install on OpenShift

WIP

## Step 2: Deploy Milvus Cluster


```bash
# Apply the Milvus cluster configuration
oc apply -f milvus-cluster.yaml -n intelligent-cd
```

### Verify Cluster Deployment

```bash
# Check pods status
oc get pods -n intelligent-cd

# Check Milvus cluster status
oc get milvus -n intelligent-cd
```


## Step 3: Access Milvus Dashboard

### Option A: Port Forward (Minikube/Development)

```bash
# Forward the Milvus service port
oc port-forward svc/milvus-milvus 9091:9091 -n intelligent-cd
```

Open your browser and navigate to **http://localhost:9091/webui/** to access the Milvus dashboard.

### Option B: OpenShift Route (Production)

```bash
# Expose the service as a route
oc expose service milvus-milvus --port=9091 --name=milvus-dashboard -n intelligent-cd

# Get the route URL
oc get route milvus-dashboard -n intelligent-cd --template='https://{{ .spec.host }}'
```

**Note:** The route URL will be in the format: `https://milvus-dashboard-intelligent-cd.<cluster-domain>`


Continue to 🤖 [Deploy LLaMA Stack with MCP Integration](05-deploy-llama-stack.md) section ➡️

## Important Resources

- [Full Milvus Cluster YAML](https://github.com/milvus-io/milvus/blob/master/configs/milvus.yaml)
- [Milvus Cluster YAML example](https://github.com/zilliztech/milvus-operator/blob/main/config/samples/demo.yaml)
- [Webui Documentation](https://milvus.io/docs/milvus-webui.md)

Others:

- [Milvus Documentation](https://milvus.io/docs)
- [Milvus Operator GitHub](https://github.com/milvus-io/milvus-operator)
- [Vector Database Best Practices](https://milvus.io/docs/best_practices.md)
