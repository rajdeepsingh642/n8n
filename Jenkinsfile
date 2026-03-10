pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'rajdeepsingh642/n8n-demo-app'
        DOCKER_REGISTRY = 'docker.io'
        // KUBECONFIG = credentials('kubeconfig')  // Temporarily disabled
        // SLACK_WEBHOOK = credentials('slack-webhook')  // Temporarily disabled
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/rajdeepsingh642/n8n.git'
            }
        }
        
        stage('Notify Build Start') {
            steps {
                echo "🚀 Build started for n8n-demo-app on branch ${env.BRANCH_NAME}"
                echo "📝 Note: Slack and K8s credentials not configured yet"
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo "🐳 Building Docker image: ${DOCKER_IMAGE}:${BUILD_NUMBER}"
                script {
                    sh '''
                        docker build -t ${DOCKER_IMAGE}:${BUILD_NUMBER} .
                        docker tag ${DOCKER_IMAGE}:${BUILD_NUMBER} ${DOCKER_IMAGE}:latest
                        echo "✅ Docker build completed successfully"
                    '''
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                echo "📤 Pushing to Docker Hub..."
                script {
                    // Skip Docker Hub push for now - need credentials
                    echo "⚠️ Docker Hub credentials not configured - skipping push"
                    echo "📦 Image built locally: ${DOCKER_IMAGE}:${BUILD_NUMBER}"
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                echo "☸️ Kubernetes deployment stage"
                script {
                    // Skip K8s deploy for now - need kubeconfig
                    echo "⚠️ Kubernetes config not configured - skipping deployment"
                    echo "🔧 To enable: Add kubeconfig credential in Jenkins"
                }
            }
        }
    }
    
    post {
        success {
            echo "✅ Pipeline completed successfully!"
            echo "📦 Docker image: ${DOCKER_IMAGE}:${BUILD_NUMBER}"
            echo "🌐 Next steps: Configure Docker Hub and K8s credentials"
        }
        
        failure {
            echo "❌ Pipeline failed! Check logs for details."
        }
        
        always {
            echo "📊 Pipeline finished."
        }
    }
}
