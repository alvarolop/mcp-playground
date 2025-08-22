# 🗄️ Deploy Milvus Vector Database

This section covers setting up Milvus for storing and retrieving vector embeddings to enable RAG capabilities.

## Overview

Learn how to deploy Milvus vector database on OpenShift to support Retrieval-Augmented Generation (RAG) functionality in your MCP-powered chatbot.

## Prerequisites

- OpenShift cluster with MCP server and Gradio interface deployed
- [OpenShift CLI (oc)](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html)
- [Helm](https://helm.sh/docs/intro/install/) for package management

## What is Milvus?

Milvus is an open-source vector database designed for AI applications. It provides:
- High-performance vector similarity search
- Scalable architecture for large-scale deployments
- Support for various vector similarity metrics
- Real-time search capabilities

## 1.a Install Milvus Operator on Minikube

```bash
# Add the Milvus Operator Helm repository
helm repo add milvus-operator https://zilliztech.github.io/milvus-operator/
helm repo update milvus-operator

# Install Milvus Operator
helm -n milvus-operator upgrade --install --create-namespace milvus-operator milvus-operator/milvus-operator
```

## 1.b Install Milvus Operator on OpenShift

WIP


## 2. Deploy Milvus Cluster

Now, we can deploy a Milvus cluster with the following YAML file.

```bash
oc apply -f milvus-cluster.yaml -n intelligent-cd
```

Now, verify the cluster is running: 

```bash
oc get pods -n intelligent-cd
```

## 3.a Access the Milvus Dashboard on Minikube

```bash
oc port-forward svc/milvus-milvus 9091:9091 -n intelligent-cd
```

Open your browser and navigate to http://localhost:9091/webui/ to access the Milvus dashboard.

## 3.b Access the Milvus Dashboard on OpenShift

```bash
oc expose service milvus-milvus --port=9091 --name=milvus-dashboard -n intelligent-cd
```

Open your browser and navigate to the route to access the Milvus dashboard.

```bash
oc get route milvus-dashboard -n intelligent-cd
```


## Next Steps

Continue to 🤖 [Deploy LLaMA Stack with MCP Integration](05-deploy-llama-stack.md) section ➡️
