# 🚀 Intelligent CD Chatbot

A fully featured Agentic application that based on the information stored in a RAG, allows you to convert your manual deployment and configuration to a fully GitOps deployment.

## ✨ Features

- **🎨 Beautiful Header**: Professional gradient header with logo and branding
- **🔍 System Status**: Monitor application health and connectivity
- **🧪 Test OCP MCP Server**: Verify MCP server connectivity
- **💬 Functional Chat Interface**: Real-time chat with AI assistant using Red Hat AI LLM
- **📝 Code Canvas**: Dynamic area for displaying results and generated content
- **🤖 LLM Integration**: Powered by Granite-3-3-8B-Instruct model
- **🐳 Containerized**: Ready for Docker deployment
- **🔧 Extensible**: Easy to add new features and integrations

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Intelligent CD Chatbot                       │
│              AI-Powered GitOps Deployment Assistant            │
│                    Powered by Red Hat AI                       │
└─────────────────────────────────────────────────────────────────┘
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Chatbot      │    │   Code Canvas    │    │   MCP Server    │
│   Interface    │    │   (60% width)    │    │   Integration   │
│   (40% width)  │    │                  │    │                 │
│   + LLM Chat   │    │   + Results      │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker (optional)
- kubectl configured with your cluster
- Access to a Kubernetes cluster
- Red Hat AI API access (for LLM functionality)

### Option 1: Run Locally (Recommended for Development)

1. **Clone and navigate to the project:**
   ```bash
   cd gradio-app
   ```

2. **Install dependencies:**
   ```bash
   make install
   # or manually:
   # pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your LLM API credentials
   ```

4. **Run the application:**
   ```bash
   make run-local
   # or manually:
   # python main.py
   ```

5. **Access the application:**
   Open your browser and go to: http://localhost:7860

### Option 2: Run with Docker

1. **Build the Docker image:**
   ```bash
   make build
   ```

2. **Create environment file:**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

3. **Run the container:**
   ```bash
   make run
   ```

4. **Access the application:**
   Open your browser and go to: http://localhost:7860

## 🛠️ Available Commands

```bash
# Build and run
make build          # Build Docker image
make run            # Run container in background
make run-interactive # Run container interactively

# Management
make stop           # Stop and remove container
make logs           # View container logs
make exec           # Execute bash in container

# Development
make run-local      # Run application locally
make install        # Install Python dependencies
make clean          # Clean up Docker images
make help           # Show all available commands
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file based on `env.example`:

```bash
# Kubernetes MCP Configuration
KUBERNETES_MCP_URL=http://localhost:8080

# RAG System Configuration
RAG_ENDPOINT=http://localhost:8000

# LLM Configuration
OLS_PROVIDER_TYPE=rhoai_vllm
OLS_PROVIDER_MODEL_NAME=granite-3-3-8b-instruct
OLS_PROVIDER_API_URL=https://granite-3-3-8b-instruct-maas-apicast-production.apps.prod.rhoai.rh-aiservices-bu.com:443/v1
OLS_PROVIDER_API_TOKEN=your_api_token_here

# Gradio Configuration
GRADIO_SERVER_NAME=0.0.0.0
GRADIO_SERVER_PORT=7860
```

### LLM Integration

The application integrates with Red Hat AI's Granite-3-3-8B-Instruct model to provide:

- **Intelligent Responses**: AI-powered assistance for Kubernetes and GitOps questions
- **Context Awareness**: The model understands deployment and configuration contexts
- **Real-time Chat**: Interactive conversation interface for deployment assistance
- **Code Generation**: Help with deployment manifests and configurations

### Kubernetes Access

The application needs access to your Kubernetes cluster. When running with Docker, it mounts your local kubeconfig:

```bash
docker run -v $(HOME)/.kube:/root/.kube:ro ...
```

## 🔧 Development

### Project Structure

```
gradio-app/
├── main.py              # Main application code with LLM integration
├── requirements.txt     # Python dependencies
├── Dockerfile          # Container configuration
├── Makefile            # Build and run commands
├── env.example         # Environment variables template
├── logo.png            # Application logo
└── README.md           # This file
```

### UI Layout

The application features a professional, modern interface:

1. **Beautiful Header**: Gradient background with logo, title, and Red Hat AI branding
2. **Top-Right Controls**: System Status and Test OCP MCP Server buttons
3. **Two-Column Layout**:
   - **Left (40%)**: Functional chat interface with AI assistant
   - **Right (60%)**: Dynamic content area for results and code generation

### Adding New Features

1. **New MCP Operations:**
   - Add methods to `KubernetesMCPClient` class
   - Update the `kubernetes_operations` function
   - Add new buttons to the top controls area

2. **New LLM Features:**
   - Extend the `LLMClient` class
   - Add new chat capabilities
   - Implement specialized deployment assistance

3. **New UI Components:**
   - Add new controls to the top-right area
   - Follow the existing pattern for consistency
   - Use the two-column layout for content

## 🧪 Testing

### Local Testing

1. **Start the application locally:**
   ```bash
   make run-local
   ```

2. **Test system status:**
   - Click the "🔍 System Status" button
   - Verify connectivity information

3. **Test MCP server:**
   - Click the "🧪 Test OCP MCP Server" button
   - Verify server connectivity

4. **Test chat functionality:**
   - Type a message in the chat input
   - Verify AI responses from the LLM
   - Test with Kubernetes and GitOps questions

### Docker Testing

1. **Build and run:**
   ```bash
   make build
   make run
   ```

2. **Check container logs:**
   ```bash
   make logs
   ```

3. **Execute commands in container:**
   ```bash
   make exec
   ```

## 🚀 Deployment

### Kubernetes Deployment

The application is ready for Kubernetes deployment. You can:

1. **Use the existing Helm chart** from your repository
2. **Create a new deployment manifest** based on the Docker image
3. **Deploy with ArgoCD** using the application manifest you created

### Production Considerations

- **Security**: Implement proper authentication and authorization
- **Monitoring**: Add Prometheus metrics and Grafana dashboards
- **Logging**: Implement structured logging with ELK stack
- **Scaling**: Use Horizontal Pod Autoscaler for load balancing
- **LLM Security**: Secure API token storage and access
- **Backup**: Implement backup strategies for chat data

## 🔮 Future Enhancements

- [ ] **Advanced Chat Features**: Streaming responses and conversation history
- [ ] **File Upload**: Support for document upload and processing
- [ ] **Authentication**: Add user authentication and role-based access
- [ ] **More MCP Operations**: Expand Kubernetes MCP capabilities
- [ ] **Monitoring**: Add Prometheus metrics and health checks
- [ ] **API Endpoints**: RESTful API for programmatic access
- [ ] **Multi-language Support**: Internationalization (i18n)
- [ ] **Custom Models**: Support for different LLM providers

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   # Check what's using port 7860
   lsof -i :7860
   # Kill the process or change the port in .env
   ```

2. **LLM API errors:**
   ```bash
   # Verify API credentials in .env
   # Check API endpoint accessibility
   # Verify API token validity
   ```

3. **Kubernetes access denied:**
   ```bash
   # Verify kubectl configuration
   kubectl cluster-info
   # Check if the container can access kubeconfig
   ```

4. **Container won't start:**
   ```bash
   # Check container logs
   make logs
   # Verify Docker daemon is running
   docker info
   ```

### Debug Mode

Run the application with debug logging:

```bash
# Local
GRADIO_DEBUG=1 python main.py

# Docker
docker run -e GRADIO_DEBUG=1 ...
```

## 📚 Resources

- [Gradio Documentation](https://gradio.app/docs/)
- [Kubernetes MCP Server](https://github.com/containers/kubernetes-mcp-server)
- [Red Hat AI Documentation](https://docs.openshift.com/ai/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Happy coding! 🎉**
