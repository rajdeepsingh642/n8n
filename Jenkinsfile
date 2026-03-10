pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'rajdeepsingh642/n8n-demo-app'
        DOCKER_REGISTRY = 'docker.io'
        KUBECONFIG = credentials('kubeconfig')
        SLACK_WEBHOOK = credentials('slack-webhook')
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/rajdeepsingh642/n8n.git'
            }
        }
        
        stage('Notify Build Start') {
            steps {
                script {
                    sh '''
                        python3 -c "
import sys
sys.path.append('.')
from slack_notifier import SlackNotifier
notifier = SlackNotifier('${SLACK_WEBHOOK}')
notifier.notify_build_start('n8n-demo-app', '${env.BRANCH_NAME}')
"
                    '''
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    sh '''
                        docker build -t ${DOCKER_IMAGE}:${BUILD_NUMBER} .
                        docker tag ${DOCKER_IMAGE}:${BUILD_NUMBER} ${DOCKER_IMAGE}:latest
                    '''
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh '''
                            echo ${DOCKER_PASSWORD} | docker login -u ${DOCKER_USERNAME} --password-stdin ${DOCKER_REGISTRY}
                            docker push ${DOCKER_IMAGE}:${BUILD_NUMBER}
                            docker push ${DOCKER_IMAGE}:latest
                        '''
                    }
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh '''
                        python3 -c "
import sys
sys.path.append('.')
from slack_notifier import SlackNotifier
notifier = SlackNotifier('${SLACK_WEBHOOK}')
notifier.notify_deployment_start('n8n-demo-app', 'production')
"
                    '''
                    
                    withKubeConfig([credentialsId: 'kubeconfig']) {
                        sh '''
                            # Update the image tag in deployment
                            sed -i "s|image: .*|image: ${DOCKER_IMAGE}:${BUILD_NUMBER}|g" k8s/deployment.yaml
                            
                            # Apply Kubernetes manifests
                            kubectl apply -f k8s/
                            
                            # Wait for rollout
                            kubectl rollout status deployment/n8n-demo-app --timeout=300s
                        '''
                    }
                }
            }
        }
    }
    
    post {
        success {
            script {
                sh '''
                    python3 -c "
import sys
sys.path.append('.')
from slack_notifier import SlackNotifier
notifier = SlackNotifier('${SLACK_WEBHOOK}')
notifier.notify_build_success('n8n-demo-app', '${env.BRANCH_NAME}', '${DOCKER_IMAGE}:${BUILD_NUMBER}')
notifier.notify_deployment_success('n8n-demo-app', 'production', 'http://your-k8s-ip:30000')
"
                '''
            }
        }
        
        failure {
            script {
                echo "Build failed! Check logs for details."
            }
        }
        
        always {
            echo "Pipeline finished."
        }
    }
}
