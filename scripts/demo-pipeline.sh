#!/bin/bash

# Demo script để minh họa Jenkins CI/CD workflow
# Script này mô phỏng các bước mà Jenkins sẽ thực hiện

set -e

echo "=========================================="
echo "🚀 Jenkins CI/CD Pipeline Demo"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Stage 1: Checkout
echo -e "${BLUE}Stage 1: Checkout${NC}"
echo "✓ Simulating git checkout..."
GIT_COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "abc1234")
echo "  Current commit: $GIT_COMMIT"
echo ""

# Stage 2: Build
echo -e "${BLUE}Stage 2: Build Docker Image${NC}"
BUILD_TAG="demo-$GIT_COMMIT"
echo "  Building image: ocr-khai-sinh:$BUILD_TAG"
docker build -t ocr-khai-sinh:$BUILD_TAG -t ocr-khai-sinh:latest . > /dev/null 2>&1
echo -e "${GREEN}✓ Build completed successfully${NC}"
echo ""

# Stage 3: Test
echo -e "${BLUE}Stage 3: Run Tests${NC}"
echo "  Starting test container..."

# Check if port 8128 is already in use
if docker ps | grep -q "8128->8000"; then
    echo -e "${YELLOW}  Port 8128 already in use, using existing container for tests${NC}"
    TEST_PORT=8128
else
    # Start a test container
    docker run -d --name test-container-$$ -p 9000:8000 ocr-khai-sinh:$BUILD_TAG > /dev/null
    TEST_PORT=9000
    echo "  Waiting for application to start..."
    sleep 5
fi

# Run tests
echo "  Running API tests..."
if [ $TEST_PORT -eq 8128 ]; then
    python3 tests/test_api.py > /dev/null 2>&1
else
    # Temporarily modify test to use port 9000
    sed -i.bak 's/8128/9000/g' tests/test_api.py
    python3 tests/test_api.py > /dev/null 2>&1
    mv tests/test_api.py.bak tests/test_api.py
fi

echo -e "${GREEN}✓ All tests passed${NC}"

# Cleanup test container if we created one
if [ $TEST_PORT -eq 9000 ]; then
    docker stop test-container-$$ > /dev/null 2>&1
    docker rm test-container-$$ > /dev/null 2>&1
fi
echo ""

# Stage 4: Push (simulated)
echo -e "${BLUE}Stage 4: Push to Registry${NC}"
echo -e "${YELLOW}  [SIMULATED] Would push to Docker registry:${NC}"
echo "    - ocr-khai-sinh:$BUILD_TAG"
echo "    - ocr-khai-sinh:latest"
echo ""

# Stage 5: Deploy (simulated)
echo -e "${BLUE}Stage 5: Deploy${NC}"
echo -e "${YELLOW}  [SIMULATED] Would deploy to server:${NC}"
echo "    - Pull latest image"
echo "    - Restart containers"
echo "    - Verify deployment"
echo ""

# Summary
echo "=========================================="
echo -e "${GREEN}✅ Pipeline Demo Completed Successfully!${NC}"
echo "=========================================="
echo ""
echo "📊 Summary:"
echo "  - Commit: $GIT_COMMIT"
echo "  - Image: ocr-khai-sinh:$BUILD_TAG"
echo "  - Tests: PASSED"
echo "  - Status: READY FOR DEPLOYMENT"
echo ""
echo "🔍 Next steps:"
echo "  1. Setup Jenkins server"
echo "  2. Configure credentials"
echo "  3. Create pipeline job"
echo "  4. Pipeline will run automatically on git push"
echo ""
