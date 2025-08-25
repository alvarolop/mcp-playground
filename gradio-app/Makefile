# Variables
IMAGE_NAME = gradio-rag-app
IMAGE_TAG = latest
CONTAINER_NAME = gradio-rag-app
PORT = 7860

# Default target
.PHONY: all
all: build

# Build the Docker image
.PHONY: build
build:
	@echo "Building Docker image..."
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .
	@echo "✅ Build completed!"

# Run the container locally
.PHONY: run
run:
	@echo "Running container..."
	docker run -d \
		--name $(CONTAINER_NAME) \
		-p $(PORT):$(PORT) \
		-v $(HOME)/.kube:/root/.kube:ro \
		--env-file .env \
		$(IMAGE_NAME):$(IMAGE_TAG)
	@echo "✅ Container started! Access at http://localhost:$(PORT)"

# Run the container in interactive mode
.PHONY: run-interactive
run-interactive:
	@echo "Running container in interactive mode..."
	docker run -it \
		--name $(CONTAINER_NAME)-interactive \
		-p $(PORT):$(PORT) \
		-v $(HOME)/.kube:/root/.kube:ro \
		--env-file .env \
		$(IMAGE_NAME):$(IMAGE_TAG)

# Stop and remove the container
.PHONY: stop
stop:
	@echo "Stopping and removing container..."
	-docker stop $(CONTAINER_NAME) $(CONTAINER_NAME)-interactive
	-docker rm $(CONTAINER_NAME) $(CONTAINER_NAME)-interactive
	@echo "✅ Container stopped and removed!"

# View container logs
.PHONY: logs
logs:
	@echo "Container logs:"
	docker logs -f $(CONTAINER_NAME)

# Execute commands in the running container
.PHONY: exec
exec:
	@echo "Executing bash in container..."
	docker exec -it $(CONTAINER_NAME) /bin/bash

# Clean up Docker images
.PHONY: clean
clean:
	@echo "Cleaning up Docker images..."
	-docker rmi $(IMAGE_NAME):$(IMAGE_TAG)
	@echo "✅ Cleanup completed!"

# Run the application locally (without Docker)
.PHONY: run-local
run-local:
	@echo "Running application locally..."
	python -m pip install -r requirements.txt
	python main.py

# Install dependencies locally
.PHONY: install
install:
	@echo "Installing Python dependencies..."
	python -m pip install -r requirements.txt
	@echo "✅ Dependencies installed!"

# Show help
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  build          - Build Docker image"
	@echo "  run            - Run container in background"
	@echo "  run-interactive- Run container interactively"
	@echo "  stop           - Stop and remove container"
	@echo "  logs           - View container logs"
	@echo "  exec           - Execute bash in container"
	@echo "  clean          - Clean up Docker images"
	@echo "  run-local      - Run application locally"
	@echo "  install        - Install Python dependencies"
	@echo "  help           - Show this help message"
