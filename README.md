# n8n Demo App - CI/CD Pipeline

Simple Python Flask application with complete CI/CD pipeline using Jenkins, Docker Hub, Kubernetes, and Slack notifications.

## 🏗️ Architecture

```
GitHub → Jenkins → Docker Hub → Kubernetes → Slack
```

## 📁 Project Structure

```
n8n-demo-app/
├── app.py                 # Flask web application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker image configuration
├── Jenkinsfile           # CI/CD pipeline definition
├── slack_notifier.py     # Slack notification utility
├── k8s/                  # Kubernetes manifests
│   ├── deployment.yaml   # Kubernetes deployment
│   └── service.yaml      # Kubernetes service
└── README.md            # This file
```

## 🚀 Setup Instructions

### 1. Prerequisites

- Docker installed
- Kubernetes cluster running
- Jenkins server with Docker and kubectl plugins
- Docker Hub account
- Slack workspace with incoming webhook

### 2. Jenkins Setup

1. Install required plugins:
   - Docker Pipeline
   - Kubernetes CLI
   - Git

2. Add credentials in Jenkins:
   - `dockerhub-credentials`: Username/Password for Docker Hub
   - `kubeconfig`: Kubernetes configuration file
   - `slack-webhook`: Slack webhook URL

3. Create pipeline job using the `Jenkinsfile`

### 3. Kubernetes Setup

```bash
# Apply manifests
kubectl apply -f k8s/

# Check deployment
kubectl get pods -l app=n8n-demo-app
kubectl get services
```

### 4. Environment Variables

Update the following in `Jenkinsfile`:
- `DOCKER_IMAGE`: Your Docker Hub image name
- GitHub repository URL
- Kubernetes service URL in Slack notifications

## 🔄 Pipeline Stages

1. **Checkout**: Pull code from GitHub
2. **Notify Build Start**: Send Slack notification
3. **Build Docker Image**: Build container image
4. **Push to Docker Hub**: Upload to registry
5. **Deploy to Kubernetes**: Update deployment
6. **Notifications**: Send success/failure alerts

## 🧪 Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py

# Test Slack notifications
python slack_notifier.py

# Build Docker image
docker build -t n8n-demo-app .
docker run -p 5000:5000 n8n-demo-app
```

## 📱 Endpoints

- **Application**: http://localhost:5000
- **Health Check**: http://localhost:5000/health
- **Kubernetes Service**: http://your-k8s-ip:30000

## 🔧 Configuration

### Slack Webhook Setup

1. Go to Slack App Directory
2. Create "Incoming Webhooks" app
3. Add to workspace
4. Copy webhook URL
5. Add as Jenkins credential

### Docker Hub Integration

1. Create Docker Hub repository
2. Update `DOCKER_IMAGE` in Jenkinsfile
3. Add Docker Hub credentials to Jenkins

### Kubernetes Deployment

The deployment includes:
- 2 replicas for high availability
- Resource limits (128Mi-256Mi memory, 100m-200m CPU)
- Health checks and readiness probes
- NodePort service for external access

## 🎯 Features

- ✅ Automated builds on code changes
- ✅ Docker image versioning with build numbers
- ✅ Rolling deployments to Kubernetes
- ✅ Real-time Slack notifications
- ✅ Health checks and monitoring
- ✅ Resource optimization
- ✅ Zero-downtime deployments

## 🛠️ Customization

- Modify `app.py` for your application logic
- Update `requirements.txt` for dependencies
- Adjust `k8s/deployment.yaml` for scaling needs
- Customize Slack messages in `slack_notifier.py`

## 📞 Support

For issues or questions, check:
- Jenkins logs for pipeline failures
- Kubernetes logs: `kubectl logs -l app=n8n-demo-app`
- Docker build logs in Jenkins console output
