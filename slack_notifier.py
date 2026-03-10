import requests
import json
import os

class SlackNotifier:
    def __init__(self, webhook_url=None):
        self.webhook_url = webhook_url or os.getenv("SLACK_WEBHOOK_URL")
        
    def send_message(self, message, channel=None, username="CI/CD Bot"):
        if not self.webhook_url:
            print("Slack webhook URL not configured")
            return False
            
        payload = {
            "text": message,
            "username": username
        }
        
        if channel:
            payload["channel"] = channel
            
        try:
            response = requests.post(
                self.webhook_url,
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json'}
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Failed to send Slack notification: {e}")
            return False
    
    def notify_build_start(self, app_name, branch):
        message = f"🚀 Build started for {app_name} on branch {branch}"
        return self.send_message(message)
    
    def notify_build_success(self, app_name, branch, image_tag):
        message = f"✅ Build successful for {app_name} on branch {branch}\n📦 Image: {image_tag}"
        return self.send_message(message)
    
    def notify_build_failure(self, app_name, branch, error):
        message = f"❌ Build failed for {app_name} on branch {branch}\n🔥 Error: {error}"
        return self.send_message(message)
    
    def notify_deployment_start(self, app_name, environment):
        message = f"🔄 Deployment started for {app_name} to {environment}"
        return self.send_message(message)
    
    def notify_deployment_success(self, app_name, environment, url=None):
        message = f"✅ Deployment successful for {app_name} to {environment}"
        if url:
            message += f"\n🌐 URL: {url}"
        return self.send_message(message)
    
    def notify_deployment_failure(self, app_name, environment, error):
        message = f"❌ Deployment failed for {app_name} to {environment}\n🔥 Error: {error}"
        return self.send_message(message)

if __name__ == "__main__":
    # Test the notifier
    notifier = SlackNotifier()
    notifier.send_message("🧪 Slack notification test from CI/CD pipeline")
