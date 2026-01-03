pipeline {
    agent any
    
    environment {
        // Docker registry configuration
        DOCKER_REGISTRY = credentials('docker-registry-url') // Configure in Jenkins credentials
        DOCKER_IMAGE_NAME = 'ocr-khai-sinh'
        DOCKER_CREDENTIALS_ID = 'docker-hub-credentials' // Configure in Jenkins credentials
        
        // Build information
        GIT_COMMIT_SHORT = sh(returnStdout: true, script: "git rev-parse --short HEAD").trim()
        BUILD_TAG = "${env.BUILD_NUMBER}-${GIT_COMMIT_SHORT}"
        
        // Deployment configuration
        DEPLOY_HOST = credentials('deploy-host') // Configure in Jenkins credentials
        DEPLOY_USER = credentials('deploy-user') // Configure in Jenkins credentials
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
                sh 'git rev-parse HEAD'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo "Building Docker image: ${DOCKER_IMAGE_NAME}:${BUILD_TAG}"
                script {
                    docker.build("${DOCKER_IMAGE_NAME}:${BUILD_TAG}")
                    docker.build("${DOCKER_IMAGE_NAME}:latest")
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                script {
                    // Start container for testing
                    sh """
                        docker run -d --name test-container-${BUILD_NUMBER} \
                            -p 8000:8000 \
                            ${DOCKER_IMAGE_NAME}:${BUILD_TAG}
                    """
                    
                    // Wait for container to be ready
                    sleep(time: 10, unit: 'SECONDS')
                    
                    // Run health check
                    sh """
                        curl -f http://localhost:8000/docs || exit 1
                    """
                    
                    // Run tests if test file exists
                    sh """
                        if [ -f tests/test_api.py ]; then
                            python3 tests/test_api.py
                        else
                            echo "No test file found, skipping tests"
                        fi
                    """
                }
            }
            post {
                always {
                    // Clean up test container
                    sh """
                        docker stop test-container-${BUILD_NUMBER} || true
                        docker rm test-container-${BUILD_NUMBER} || true
                    """
                }
            }
        }
        
        stage('Push to Registry') {
            when {
                branch 'main'
            }
            steps {
                echo 'Pushing Docker image to registry...'
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", "${DOCKER_CREDENTIALS_ID}") {
                        docker.image("${DOCKER_IMAGE_NAME}:${BUILD_TAG}").push()
                        docker.image("${DOCKER_IMAGE_NAME}:latest").push()
                    }
                }
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                echo 'Deploying to server...'
                script {
                    // Deploy using SSH
                    sshagent(credentials: ['ssh-deploy-key']) {
                        sh """
                            ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} '
                                cd /opt/ocr-khai-sinh &&
                                docker-compose pull &&
                                docker-compose up -d &&
                                docker-compose ps
                            '
                        """
                    }
                    
                    // Verify deployment
                    sh """
                        sleep 15
                        curl -f http://${DEPLOY_HOST}:8128/docs || exit 1
                    """
                }
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline completed successfully!'
            // You can add notifications here (Slack, Email, etc.)
        }
        failure {
            echo 'Pipeline failed!'
            // You can add failure notifications here
        }
        always {
            // Clean up Docker images to save space
            sh """
                docker image prune -f
            """
        }
    }
}
