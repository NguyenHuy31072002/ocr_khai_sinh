#!/bin/bash

# Deploy script for OCR Khai Sinh application
# This script pulls the latest Docker image and restarts the application

set -e  # Exit on error

# Configuration
DOCKER_IMAGE="${DOCKER_IMAGE:-ocr-khai-sinh:latest}"
CONTAINER_NAME="${CONTAINER_NAME:-fastapi_app_huynk}"
COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.yml}"
APP_PORT="${APP_PORT:-8128}"

echo "=========================================="
echo "OCR Khai Sinh Deployment Script"
echo "=========================================="
echo "Docker Image: $DOCKER_IMAGE"
echo "Container Name: $CONTAINER_NAME"
echo "Compose File: $COMPOSE_FILE"
echo "=========================================="
echo

# Function to check if container is running
check_container() {
    if docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
        return 0
    else
        return 1
    fi
}

# Function to wait for application to be ready
wait_for_app() {
    echo "Waiting for application to be ready..."
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f -s "http://localhost:$APP_PORT/docs" > /dev/null 2>&1; then
            echo "✓ Application is ready!"
            return 0
        fi
        
        echo "  Attempt $attempt/$max_attempts - waiting..."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo "✗ Application did not become ready in time"
    return 1
}

# Step 1: Pull latest image (if using registry)
if [[ "$DOCKER_IMAGE" == *":"* ]] && [[ "$DOCKER_IMAGE" != *"latest"* ]]; then
    echo "Step 1: Pulling latest Docker image..."
    docker pull "$DOCKER_IMAGE" || echo "Warning: Could not pull image, using local version"
    echo
else
    echo "Step 1: Using local Docker image"
    echo
fi

# Step 2: Stop and remove old container
echo "Step 2: Stopping existing containers..."
if check_container; then
    docker-compose -f "$COMPOSE_FILE" down
    echo "✓ Containers stopped"
else
    echo "No running containers found"
fi
echo

# Step 3: Start new container
echo "Step 3: Starting new containers..."
docker-compose -f "$COMPOSE_FILE" up -d
echo "✓ Containers started"
echo

# Step 4: Verify deployment
echo "Step 4: Verifying deployment..."
sleep 5

if check_container; then
    echo "✓ Container is running"
    
    # Show container status
    echo
    echo "Container status:"
    docker-compose -f "$COMPOSE_FILE" ps
    echo
    
    # Wait for application to be ready
    if wait_for_app; then
        echo
        echo "=========================================="
        echo "✅ Deployment successful!"
        echo "=========================================="
        echo "Application URL: http://localhost:$APP_PORT/docs"
        echo
        exit 0
    else
        echo
        echo "=========================================="
        echo "⚠️  Container is running but application is not responding"
        echo "=========================================="
        echo "Check logs with: docker-compose logs -f"
        echo
        exit 1
    fi
else
    echo "✗ Container is not running"
    echo
    echo "=========================================="
    echo "❌ Deployment failed!"
    echo "=========================================="
    echo "Check logs with: docker-compose logs"
    echo
    exit 1
fi
