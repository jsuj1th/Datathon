# Deployment Guide

## Production Deployment

### Option 1: Docker Deployment (Recommended)

#### 1. Create Dockerfile

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p uploads test_documents

# Expose port
EXPOSE 5000

# Run with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:app"]
```

#### 2. Create docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - ./uploads:/app/uploads
      - ./hitl_feedback.json:/app/hitl_feedback.json
    restart: unless-stopped
```

#### 3. Deploy

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Option 2: Traditional Server Deployment

#### 1. Install System Dependencies

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv
sudo apt-get install -y poppler-utils tesseract-ocr nginx

# CentOS/RHEL
sudo yum install -y python3 python3-pip
sudo yum install -y poppler-utils tesseract nginx
```

#### 2. Set Up Application

```bash
# Clone repository
git clone <your-repo-url>
cd ai-document-classifier

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Configure environment
cp .env.example .env
nano .env  # Add your API keys
```

#### 3. Configure Gunicorn

Create `gunicorn_config.py`:

```python
bind = "127.0.0.1:5000"
workers = 4
worker_class = "sync"
timeout = 120
keepalive = 5
errorlog = "/var/log/gunicorn/error.log"
accesslog = "/var/log/gunicorn/access.log"
loglevel = "info"
```

#### 4. Create Systemd Service

Create `/etc/systemd/system/document-classifier.service`:

```ini
[Unit]
Description=AI Document Classification System
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/ai-document-classifier
Environment="PATH=/path/to/ai-document-classifier/venv/bin"
ExecStart=/path/to/ai-document-classifier/venv/bin/gunicorn -c gunicorn_config.py app:app

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable document-classifier
sudo systemctl start document-classifier
sudo systemctl status document-classifier
```

#### 5. Configure Nginx

Create `/etc/nginx/sites-available/document-classifier`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 50M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
    }

    location /static {
        alias /path/to/ai-document-classifier/static;
        expires 30d;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/document-classifier /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 6. Set Up SSL with Let's Encrypt

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Option 3: Cloud Platform Deployment

#### AWS Elastic Beanstalk

1. Install EB CLI:
```bash
pip install awsebcli
```

2. Initialize:
```bash
eb init -p python-3.11 document-classifier
```

3. Create environment:
```bash
eb create production-env
```

4. Set environment variables:
```bash
eb setenv OPENAI_API_KEY=your_key FLASK_ENV=production
```

5. Deploy:
```bash
eb deploy
```

#### Google Cloud Run

1. Create `Dockerfile` (see Docker section above)

2. Build and push:
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/document-classifier
```

3. Deploy:
```bash
gcloud run deploy document-classifier \
  --image gcr.io/PROJECT_ID/document-classifier \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your_key
```

#### Heroku

1. Create `Procfile`:
```
web: gunicorn app:app
```

2. Create `runtime.txt`:
```
python-3.11.0
```

3. Deploy:
```bash
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your_key
git push heroku main
```

## Security Hardening

### 1. Environment Variables
- Never commit `.env` to version control
- Use secrets management (AWS Secrets Manager, HashiCorp Vault)
- Rotate API keys regularly

### 2. File Upload Security
- Validate file types strictly
- Scan uploads for malware
- Implement rate limiting
- Set appropriate file size limits

### 3. API Security
- Implement authentication (JWT, OAuth)
- Add rate limiting (Flask-Limiter)
- Use HTTPS only
- Enable CORS selectively

### 4. Data Privacy
- Encrypt data at rest
- Implement data retention policies
- Add audit logging
- Comply with GDPR/CCPA

### 5. Network Security
- Use firewall rules
- Implement DDoS protection
- Enable WAF (Web Application Firewall)
- Regular security audits

## Monitoring and Logging

### 1. Application Monitoring

Install monitoring tools:
```bash
pip install prometheus-flask-exporter
```

Add to `app.py`:
```python
from prometheus_flask_exporter import PrometheusMetrics
metrics = PrometheusMetrics(app)
```

### 2. Log Aggregation

Configure structured logging:
```python
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('app.log', maxBytes=10000000, backupCount=5)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
```

### 3. Error Tracking

Use Sentry:
```bash
pip install sentry-sdk[flask]
```

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()]
)
```

## Performance Optimization

### 1. Caching

Add Redis caching:
```bash
pip install redis flask-caching
```

```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'redis'})
```

### 2. Database

For production, use PostgreSQL for HITL data:
```bash
pip install psycopg2-binary flask-sqlalchemy
```

### 3. CDN

Serve static files via CDN (CloudFlare, AWS CloudFront)

### 4. Load Balancing

Use multiple workers and load balancer (AWS ALB, nginx)

## Backup and Recovery

### 1. Automated Backups

```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf backup_$DATE.tar.gz uploads/ hitl_feedback.json
aws s3 cp backup_$DATE.tar.gz s3://your-backup-bucket/
```

### 2. Database Backups

```bash
# For PostgreSQL
pg_dump dbname > backup.sql
```

### 3. Disaster Recovery Plan

- Regular backup testing
- Documented recovery procedures
- Redundant deployments
- Monitoring and alerts

## Scaling Strategies

### Horizontal Scaling
- Multiple application instances
- Load balancer distribution
- Shared storage (S3, NFS)
- Distributed caching (Redis Cluster)

### Vertical Scaling
- Increase worker count
- Larger instance types
- More memory for processing
- GPU instances for vision models

### Async Processing
- Use Celery for background tasks
- Message queue (RabbitMQ, Redis)
- Separate worker processes

## Maintenance

### Regular Tasks
- Update dependencies monthly
- Review and rotate API keys
- Clean up old uploads
- Analyze HITL feedback
- Monitor error rates
- Review security logs

### Updates
```bash
# Pull latest code
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart service
sudo systemctl restart document-classifier
```

## Troubleshooting

### High Memory Usage
- Reduce worker count
- Limit concurrent uploads
- Implement file size limits
- Clear upload directory regularly

### Slow Response Times
- Enable caching
- Optimize image processing
- Use faster LLM models
- Implement request queuing

### API Rate Limits
- Implement exponential backoff
- Use multiple API keys
- Cache common results
- Batch similar requests

## Cost Optimization

### API Costs
- Use GPT-4 Turbo (cheaper)
- Cache classification results
- Implement deduplication
- Monitor usage closely

### Infrastructure Costs
- Use spot instances (AWS)
- Auto-scaling policies
- Reserved instances for base load
- Optimize storage usage
