# 🚀 Complete CI/CD Pipeline: GitHub → n8n → Jenkins → Docker → Kubernetes

## 📋 Overview

यह एक complete CI/CD pipeline है जो GitHub push events को trigger करके automated Docker builds और Kubernetes deployments करता है।

### 🔄 Pipeline Flow

```
GitHub Push → n8n Webhook → n8n IF → n8n HTTP Request → Jenkins Build → Docker Build → Docker Push → Kubernetes Deploy → Slack Notifications
```

## 🏗️ Architecture

### Components Used
- **GitHub**: Source code repository
- **n8n**: Workflow automation (self-hosted on Docker)
- **Jenkins**: CI/CD orchestration
- **Docker Hub**: Container registry
- **Kubernetes**: Container orchestration
- **Slack**: Notifications (optional)

### 🖥️ Server Details
- **Jenkins IP**: `http://192.168.33.141:8080`
- **n8n IP**: `http://192.168.33.141:5678`
- **GitHub Repo**: `https://github.com/rajdeepsingh642/n8n.git`
- **Docker Image**: `rajdeepsingh642/n8n-demo-app`

---

## 📁 Project Structure

```
n8n/
├── app.py                 # Flask application
├── Dockerfile            # Docker build configuration
├── requirements.txt      # Python dependencies
├── Jenkinsfile          # Jenkins pipeline definition
├── slack_notifier.py    # Slack notification utility
├── k8s/                 # Kubernetes manifests
│   ├── deployment.yaml  # K8s deployment config
│   └── service.yaml     # K8s service config
└── README.md           # This documentation
```

---

## 🛠️ Setup Instructions

### 1. GitHub Repository Setup

```bash
# Clone repository
git clone https://github.com/rajdeepsingh642/n8n.git
cd n8n

# Push initial code
git add .
git commit -m "Initial CI/CD setup"
git push origin master
```

### 2. n8n Setup (Docker)

```bash
# Run n8n on Docker
docker run -d --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  n8nio/n8n:latest

# Access n8n at: http://192.168.33.141:5678
```

### 3. n8n Workflow Configuration

#### Webhook Node
- **Path**: `/webhook/github-trigger`
- **HTTP Method**: POST
- **Response Code**: 200

#### IF Node (Branch Filter)
- **Condition**: `{{ $json.ref }} contains refs/heads/master`
- **Purpose**: Only trigger on master branch pushes

#### HTTP Request Node (Jenkins Trigger)
- **Method**: POST
- **URL**: `http://192.168.33.141:8080/job/n8n-demo-app/build`
- **Authentication**: Basic Auth
  - **Username**: आपका Jenkins username
  - **Password**: Jenkins API Token

### 4. Jenkins Setup

#### Create Jenkins Job
1. **New Item** → Pipeline
2. **Job name**: `n8n-demo-app`
3. **Pipeline script from SCM**: Git
4. **Repository URL**: `https://github.com/rajdeepsingh642/n8n.git`
5. **Branch**: `*/master`
6. **Script Path**: `Jenkinsfile`

#### Jenkins Credentials
Add these credentials in **Manage Jenkins** → **Credentials**:

1. **Docker Hub Credentials**
   - **Kind**: Username with password
   - **ID**: `dockerhub-credentials`
   - **Username**: आपका Docker Hub username
   - **Password**: Docker Hub access token

2. **Jenkins API Token** (for n8n trigger)
   - Generate from **Configure** → **API Token** → **Add new Token**
   - Use in n8n HTTP Request Basic Auth

3. **Slack Webhook** (optional)
   - **Kind**: Secret text
   - **ID**: `slack-webhook`
   - **Secret**: Slack webhook URL

4. **Kubeconfig** (optional)
   - **Kind**: Secret file
   - **ID**: `kubeconfig`
   - **File**: Upload `~/.kube/config`

---

## 📦 Application Details

### Flask App (`app.py`)
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from n8n CI/CD Pipeline! 🚀"

@app.route('/health')
def health():
    return {"status": "healthy"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Docker Configuration
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

---

## 🔄 Jenkins Pipeline Stages

### ✅ Working Stages
1. **Checkout**: Pull code from GitHub
2. **Notify Build Start**: Console notification
3. **Build Docker Image**: Build container image
4. **Push to Docker Hub**: Upload to registry (requires credentials)
5. **Deploy to Kubernetes**: Deploy to cluster (requires kubeconfig)

### 📊 Pipeline Status
- **Docker Build**: ✅ Working
- **Docker Push**: ⏳ Needs Docker Hub credentials
- **K8s Deploy**: ⏳ Needs kubeconfig
- **Slack Notifications**: ⏳ Needs Slack webhook

---

## 🧪 Testing the Pipeline

### 1. Manual Jenkins Build
```bash
# In Jenkins UI: n8n-demo-app → Build Now
```

### 2. n8n Workflow Test
```bash
# Test webhook directly
curl -X POST "http://192.168.33.141:5678/webhook/github-trigger" \
  -H "Content-Type: application/json" \
  -d '{"ref":"refs/heads/master"}'
```

### 3. End-to-End Test
```bash
# Push code to trigger full pipeline
git commit --allow-empty -m "🚀 Test complete CI/CD pipeline"
git push origin master
```

---

## 🔧 Configuration Files

### Jenkinsfile
```groovy
pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'rajdeepsingh642/n8n-demo-app'
        DOCKER_REGISTRY = 'docker.io'
        // KUBECONFIG = credentials('kubeconfig')  // Enable when ready
        // SLACK_WEBHOOK = credentials('slack-webhook')  // Enable when ready
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/rajdeepsingh642/n8n.git'
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
                    // Enable when Docker Hub credentials are ready
                    echo "⚠️ Docker Hub credentials not configured - skipping push"
                    echo "📦 Image built locally: ${DOCKER_IMAGE}:${BUILD_NUMBER}"
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                echo "☸️ Kubernetes deployment stage"
                script {
                    // Enable when kubeconfig is ready
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
```

---

## 🚀 Next Steps

### To Enable Full Pipeline:

1. **Docker Hub Setup**
   ```bash
   # Add dockerhub-credentials in Jenkins
   # Uncomment Docker Hub push stage in Jenkinsfile
   ```

2. **Kubernetes Setup**
   ```bash
   # Add kubeconfig credential in Jenkins
   # Uncomment K8s deployment stage in Jenkinsfile
   ```

3. **Slack Notifications**
   ```bash
   # Add slack-webhook credential in Jenkins
   # Uncomment Slack notification stages
   ```

---

## 📱 Monitoring

### Jenkins Dashboard
- **URL**: http://192.168.33.141:8080
- **Job**: n8n-demo-app
- **Build History**: Track all builds

### n8n Dashboard
- **URL**: http://192.168.33.141:5678
- **Executions Tab**: Monitor workflow runs
- **Editor Tab**: Modify workflow

### GitHub Webhooks
- **URL**: https://github.com/rajdeepsingh642/n8n/settings/hooks
- **Webhook**: http://192.168.33.141:5678/webhook/github-trigger

---

## 🆘 Troubleshooting

### Common Issues

1. **n8n Webhook Not Triggering**
   - Check workflow is Published
   - Verify GitHub webhook URL
   - Check webhook deliveries in GitHub

2. **Jenkins 403 Forbidden**
   - Use Jenkins API Token + Basic Auth
   - Enable "Trigger builds remotely" with token

3. **Docker Build Failures**
   - Check Dockerfile syntax
   - Verify all files are in repository

4. **Branch Filter Issues**
   - Verify IF node condition: `{{ $json.ref }} contains refs/heads/master`
   - Check GitHub webhook payload format

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👥 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

## 📞 Support

For issues and questions:
- 📧 Email: support@example.com
- 💬 Slack: #ci-cd-support
- 🐛 Issues: [GitHub Issues](https://github.com/rajdeepsingh642/n8n/issues)

---

**🎉 Congratulations! Your CI/CD pipeline is now running!**

*Last Updated: March 2026*
