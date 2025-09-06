# MCP Playground 🚀

Welcome to the Model Context Protocol (MCP) Playground! This repository provides a complete, production-ready solution for deploying AI agents that can safely interact with Kubernetes clusters through the [kubernetes-mcp-server](https://github.com/containers/kubernetes-mcp-server).

## 🎯 What is MCP?

The Model Context Protocol (MCP) is a standardized way for AI agents to interact with external systems and data sources. In our case, we're using it to enable AI agents to safely interact with Kubernetes clusters, making it easier to build intelligent chatbots, automation tools, and AI-powered Kubernetes management solutions.

## 🏗️ Architecture Overview

Our playground demonstrates a complete, production-ready MCP-based solution using:

- **MCP Server**: The bridge between AI agents and Kubernetes clusters
- **Gradio Interface**: A user-friendly chatbot frontend for human-AI interaction
- **OpenShift**: Enterprise Kubernetes platform for production deployments
- **Milvus**: Vector database for RAG (Retrieval-Augmented Generation) capabilities
- **LLaMA Stack**: Large Language Model deployment and management for intelligent responses

## 📚 Getting Started

This playground is organized into progressive sections that build upon each other, taking you from local development to a fully integrated AI-powered Kubernetes management system:

### 1. 🚀 [Local Development with Cursor](docs/01-local-development.md)
Start here to set up MCP locally with Cursor and test the integration with a local minikube cluster.

### 2. ☸️ [Deploy MCP Server on Kubernetes](docs/02-deploy-mcp-openshift.md)
Learn how to deploy the MCP server on Kubernetes/OpenShift for production use with proper RBAC and security.

### 3. 🔄 [Deploy MCP Server on ArgoCD](docs/03-deploy-mcp-argocd.md)
Set up the Akuity's ArgoCD MCP server for GitOps-based MCP deployments.

### 4. 🔧 [Deploy MCP Server on ServiceNow](docs/04-deploy-mcp-servicenow.md)
Set up the ServiceNow MCP server for integration with ServiceNow instances.

### 5. 🗄️ [Deploy Milvus Vector Database](docs/05-deploy-milvus.md)
Set up Milvus for storing and retrieving vector embeddings to enable RAG capabilities.

### 6. 🤖 [Deploy LLaMA Stack with MCP Integration](docs/06-deploy-llama-stack.md)
Integrate everything together using the LLaMA Stack Operator to deploy and manage LLMs.

### 7. 🌐 [Deploy Gradio Interface on OpenShift](docs/07-deploy-gradio-openshift.md)
Deploy your Gradio chatbot interface to OpenShift to make it accessible to your team.

## 🛠️ Prerequisites

- [minikube](https://minikube.sigs.k8s.io/docs/start/) for local development
- [kubectl](https://kubernetes.io/docs/tasks/tools/) for cluster management
- [OpenShift CLI (oc)](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html) for OpenShift operations
- [Helm](https://helm.sh/docs/intro/install/) for package management
- [Cursor Editor](https://www.cursor.com/) for MCP integration testing
- [Node.js](https://nodejs.org/) for MCP server installation
- [Podman](https://podman.io/) for container operations


## 📖 Additional Resources

### Core Technologies
- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [Kubernetes MCP Server](https://github.com/containers/kubernetes-mcp-server)
- [OpenShift Documentation](https://docs.openshift.com/)

### Components
- [Gradio Documentation](https://gradio.app/docs/) - Chatbot interface
- [Milvus Documentation](https://milvus.io/docs) - Vector database
- [LLaMA Stack Documentation](https://docs.llamaindex.ai/) - LLM management

### Community & Support
- [MCP GitHub Discussions](https://github.com/modelcontextprotocol/spec/discussions)
- [OpenShift Community](https://www.redhat.com/en/technologies/cloud-computing/openshift/community)

## 🤝 Contributing

Feel free to contribute improvements, bug fixes, or additional examples to this playground!

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



