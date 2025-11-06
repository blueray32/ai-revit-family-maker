# LiveKit Agents Deployment Patterns

## Deployment Options Overview

LiveKit Agents can be deployed in multiple environments:

1. **LiveKit Cloud** - Fully managed, automatic scaling
2. **Kubernetes** - Self-managed, flexible orchestration
3. **Docker Swarm** - Simple container orchestration
4. **AWS ECS/Fargate** - Serverless containers
5. **Google Cloud Run** - Serverless with auto-scaling
6. **Custom VMs** - Direct deployment on virtual machines

## LiveKit Cloud Deployment

### Prerequisites

```bash
# Install LiveKit CLI
brew install livekit-cli  # macOS
# or
curl -sSL https://get.livekit.io/cli | bash  # Linux
```

### Basic Deployment

```bash
# 1. Authenticate with LiveKit Cloud
lk cloud login

# 2. Deploy your agent
lk agent deploy

# 3. Monitor deployment
lk agent logs --follow
```

### Configuration Files

**livekit.toml:**
```toml
[agent]
job_type = "room"        # or "publisher" for specific participant
worker_type = "agent"    # identifies this as an agent worker

[agent.prewarm]
count = 2                # Keep 2 warm instances ready

[agent.scaling]
min_workers = 1
max_workers = 20
target_utilization = 0.7

[agent.resources]
cpu = "500m"            # 0.5 CPU cores
memory = "512Mi"        # 512MB RAM
```

**Dockerfile for LiveKit Cloud:**
```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install UV
RUN pip install uv

# Copy and install dependencies
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen

# Copy application
COPY . .

# Pre-download models (optional but recommended)
RUN python -c "from livekit.plugins import silero; silero.VAD.load()"

# Set environment
ENV PYTHONUNBUFFERED=1

# Run agent
CMD ["uv", "run", "python", "agent.py"]
```

### Rolling Deployments

LiveKit Cloud uses rolling deployments automatically:

```mermaid
Old Version (v1) → Running Sessions
     ↓
Deploy v2 → New Sessions go to v2
     ↓
v1 drains (up to 1 hour)
     ↓
v1 terminated → Only v2 running
```

## Kubernetes Deployment

### Deployment Manifest

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: livekit-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: livekit-agent
  template:
    metadata:
      labels:
        app: livekit-agent
    spec:
      containers:
      - name: agent
        image: your-registry/livekit-agent:latest
        env:
        - name: LIVEKIT_URL
          valueFrom:
            secretKeyRef:
              name: livekit-secrets
              key: url
        - name: LIVEKIT_API_KEY
          valueFrom:
            secretKeyRef:
              name: livekit-secrets
              key: api-key
        - name: LIVEKIT_API_SECRET
          valueFrom:
            secretKeyRef:
              name: livekit-secrets
              key: api-secret
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
```

### Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: livekit-agent-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: livekit-agent
  minReplicas: 2
  maxReplicas: 50
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300  # Wait 5 minutes before scaling down
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 30
      policies:
      - type: Percent
        value: 100
        periodSeconds: 30
```

## AWS ECS Deployment

### Task Definition

```json
{
  "family": "livekit-agent",
  "taskRoleArn": "arn:aws:iam::account:role/ecsTaskRole",
  "executionRoleArn": "arn:aws:iam::account:role/ecsExecutionRole",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "agent",
      "image": "your-ecr-repo/livekit-agent:latest",
      "essential": true,
      "environment": [
        {"name": "WORKER_TYPE", "value": "agent"}
      ],
      "secrets": [
        {
          "name": "LIVEKIT_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:livekit-api-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/livekit-agent",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "agent"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "python -c 'import sys; sys.exit(0)'"],
        "interval": 30,
        "timeout": 5,
        "retries": 3
      }
    }
  ]
}
```

### Auto-Scaling Configuration

```python
# AWS CDK example
from aws_cdk import (
    aws_ecs as ecs,
    aws_applicationautoscaling as autoscaling,
)

# Create service
service = ecs.FargateService(
    self, "LiveKitAgentService",
    cluster=cluster,
    task_definition=task_definition,
    desired_count=2,
)

# Configure auto-scaling
scaling = service.auto_scale_task_count(
    min_capacity=2,
    max_capacity=50
)

# CPU-based scaling
scaling.scale_on_cpu_utilization(
    "CpuScaling",
    target_utilization_percent=70,
    scale_in_cooldown=Duration.minutes(5),
    scale_out_cooldown=Duration.seconds(30),
)

# Custom metric scaling (active sessions)
scaling.scale_on_metric(
    "SessionScaling",
    metric=custom_metric,
    scaling_steps=[
        {"upper": 10, "change": -1},
        {"lower": 50, "change": +1},
        {"lower": 100, "change": +5},
    ],
)
```

## Google Cloud Run Deployment

### Deployment Configuration

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: livekit-agent
  annotations:
    run.googleapis.com/launch-stage: GA
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "2"
        autoscaling.knative.dev/maxScale: "100"
        run.googleapis.com/cpu-throttling: "false"
    spec:
      containerConcurrency: 1  # One agent per container
      timeoutSeconds: 3600     # 1 hour max session
      containers:
      - image: gcr.io/project/livekit-agent
        resources:
          limits:
            cpu: "1"
            memory: "1Gi"
        env:
        - name: LIVEKIT_URL
          valueFrom:
            secretKeyRef:
              name: livekit-url
              key: latest
        startupProbe:
          httpGet:
            path: /startup
          initialDelaySeconds: 0
          periodSeconds: 1
          timeoutSeconds: 1
          failureThreshold: 30
```

### Deployment Script

```bash
#!/bin/bash

# Build and push image
gcloud builds submit --tag gcr.io/PROJECT/livekit-agent

# Deploy to Cloud Run
gcloud run deploy livekit-agent \
  --image gcr.io/PROJECT/livekit-agent \
  --platform managed \
  --region us-central1 \
  --min-instances 2 \
  --max-instances 100 \
  --memory 1Gi \
  --cpu 1 \
  --timeout 3600 \
  --set-env-vars WORKER_TYPE=agent \
  --set-secrets LIVEKIT_API_KEY=livekit-key:latest
```

## Docker Compose (Development)

```yaml
version: '3.8'

services:
  agent:
    build: .
    environment:
      - LIVEKIT_URL=${LIVEKIT_URL}
      - LIVEKIT_API_KEY=${LIVEKIT_API_KEY}
      - LIVEKIT_API_SECRET=${LIVEKIT_API_SECRET}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DEEPGRAM_API_KEY=${DEEPGRAM_API_KEY}
    volumes:
      - .:/app
    command: uv run python agent.py dev
    restart: unless-stopped
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

## Monitoring and Observability

### Health Check Endpoint

```python
from aiohttp import web

async def health_check(request):
    """Health check endpoint for load balancers."""
    return web.json_response({
        "status": "healthy",
        "worker_id": os.environ.get("WORKER_ID"),
        "version": "1.0.0",
        "uptime": time.time() - START_TIME
    })

async def readiness_check(request):
    """Readiness check for Kubernetes."""
    # Check if worker is ready to accept jobs
    if worker.is_ready():
        return web.json_response({"ready": True})
    else:
        return web.json_response({"ready": False}, status=503)

# Add to your agent
app = web.Application()
app.router.add_get('/health', health_check)
app.router.add_get('/ready', readiness_check)
web.run_app(app, port=8080)
```

### Metrics Collection

```python
import prometheus_client as prom

# Define metrics
session_counter = prom.Counter('agent_sessions_total', 'Total sessions')
session_duration = prom.Histogram('agent_session_duration_seconds', 'Session duration')
active_sessions = prom.Gauge('agent_active_sessions', 'Currently active sessions')
tool_calls = prom.Counter('agent_tool_calls_total', 'Tool calls', ['tool_name'])

# Instrument your agent
class MonitoredAgent(Agent):
    async def on_enter(self):
        session_counter.inc()
        active_sessions.inc()
        self.start_time = time.time()
    
    async def on_exit(self):
        active_sessions.dec()
        duration = time.time() - self.start_time
        session_duration.observe(duration)
    
    @function_tool
    async def monitored_tool(self, context, **kwargs):
        tool_calls.labels(tool_name='monitored_tool').inc()
        # Tool implementation
```

## Security Best Practices

### Environment Variables

```python
# Use secrets management
import boto3
from google.cloud import secretmanager

def get_secret(secret_name):
    """Get secret from cloud provider."""
    if os.environ.get('AWS_REGION'):
        # AWS Secrets Manager
        client = boto3.client('secretsmanager')
        response = client.get_secret_value(SecretId=secret_name)
        return response['SecretString']
    elif os.environ.get('GOOGLE_CLOUD_PROJECT'):
        # Google Secret Manager
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{project}/secrets/{secret_name}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    else:
        # Local development
        return os.environ.get(secret_name)
```

### Network Security

```yaml
# Kubernetes NetworkPolicy
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: livekit-agent-netpol
spec:
  podSelector:
    matchLabels:
      app: livekit-agent
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: load-balancer
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: livekit-server
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 443  # HTTPS for API calls
```

## Deployment Checklist

### Pre-Deployment
- [ ] Environment variables configured
- [ ] Secrets stored securely
- [ ] Docker image built and tested
- [ ] Health checks implemented
- [ ] Logging configured
- [ ] Metrics instrumented

### Deployment
- [ ] Deploy to staging first
- [ ] Run smoke tests
- [ ] Monitor initial performance
- [ ] Check error rates
- [ ] Verify auto-scaling

### Post-Deployment
- [ ] Monitor dashboards
- [ ] Check logs for errors
- [ ] Verify session handling
- [ ] Test rollback procedure
- [ ] Document any issues

This comprehensive deployment guide covers all major platforms and patterns for deploying LiveKit Agents in production.