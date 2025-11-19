# Kubernetes Deployment

This directory contains Kubernetes manifests for deploying OmniMind in production.

## Directory Structure

```
k8s/
├── base/               # Base deployment manifests
│   └── deployment.yaml # Main deployment configuration
├── staging/            # Staging environment overlays
└── production/         # Production environment overlays
```

## Quick Start

### Prerequisites

- Kubernetes cluster (1.28+)
- kubectl CLI configured
- NGINX Ingress Controller
- cert-manager (for TLS)

### Deploy to Kubernetes

1. **Create namespace and deploy:**
```bash
kubectl apply -f k8s/base/deployment.yaml
```

2. **Verify deployment:**
```bash
kubectl get pods -n omnimind
kubectl get services -n omnimind
kubectl get ingress -n omnimind
```

3. **Check logs:**
```bash
kubectl logs -n omnimind -l app=omnimind,component=backend -f
```

## Components

### Backend Deployment
- **Replicas:** 3 (with HPA 3-10)
- **Resources:** 
  - Requests: 250m CPU, 512Mi memory
  - Limits: 1000m CPU, 2Gi memory
- **Probes:** Liveness and readiness checks
- **Auto-scaling:** Based on CPU (70%) and Memory (80%)

### Frontend Deployment
- **Replicas:** 2 (with HPA 2-5)
- **Resources:**
  - Requests: 100m CPU, 128Mi memory
  - Limits: 200m CPU, 256Mi memory
- **Probes:** Liveness and readiness checks
- **Auto-scaling:** Based on CPU (70%)

### Ingress
- **TLS:** Let's Encrypt via cert-manager
- **Paths:**
  - `/api` → Backend service
  - `/ws` → WebSocket (Backend)
  - `/` → Frontend service

## Configuration

### Update Secrets

```bash
kubectl create secret generic omnimind-secrets \
  --from-literal=OMNIMIND_DASHBOARD_USER=admin \
  --from-literal=OMNIMIND_DASHBOARD_PASS=<your-password> \
  -n omnimind --dry-run=client -o yaml | kubectl apply -f -
```

### Update Ingress Hostname

Edit `k8s/base/deployment.yaml` and replace `omnimind.example.com` with your domain.

### Storage Configuration

The deployment uses a PersistentVolumeClaim for data storage:
- **Size:** 10Gi
- **Storage Class:** standard (adjust as needed)

To use a different storage class:
```bash
kubectl patch pvc omnimind-data -n omnimind -p '{"spec":{"storageClassName":"fast-ssd"}}'
```

## Monitoring

### View Autoscaling Status

```bash
kubectl get hpa -n omnimind
kubectl describe hpa omnimind-backend-hpa -n omnimind
```

### View Resource Usage

```bash
kubectl top pods -n omnimind
kubectl top nodes
```

### View Logs

```bash
# Backend logs
kubectl logs -n omnimind -l component=backend --tail=100 -f

# Frontend logs
kubectl logs -n omnimind -l component=frontend --tail=100 -f
```

## Scaling

### Manual Scaling

```bash
# Scale backend
kubectl scale deployment omnimind-backend -n omnimind --replicas=5

# Scale frontend
kubectl scale deployment omnimind-frontend -n omnimind --replicas=3
```

### Update HPA Limits

```bash
# Increase backend max replicas
kubectl patch hpa omnimind-backend-hpa -n omnimind \
  -p '{"spec":{"maxReplicas":15}}'
```

## Troubleshooting

### Pods Not Starting

```bash
kubectl describe pod <pod-name> -n omnimind
kubectl logs <pod-name> -n omnimind --previous
```

### Service Not Accessible

```bash
# Check service
kubectl get svc -n omnimind
kubectl describe svc omnimind-backend -n omnimind

# Check ingress
kubectl get ingress -n omnimind
kubectl describe ingress omnimind-ingress -n omnimind
```

### SSL/TLS Issues

```bash
# Check certificate
kubectl get certificate -n omnimind
kubectl describe certificate omnimind-tls -n omnimind

# Check cert-manager logs
kubectl logs -n cert-manager -l app=cert-manager
```

## Cleanup

```bash
kubectl delete -f k8s/base/deployment.yaml
```

Or delete just the namespace:
```bash
kubectl delete namespace omnimind
```

## Advanced Configuration

### Custom Resource Limits

Edit the deployment and adjust resource requests/limits:

```yaml
resources:
  requests:
    memory: "1Gi"
    cpu: "500m"
  limits:
    memory: "4Gi"
    cpu: "2000m"
```

### Multiple Environments

Use Kustomize for environment-specific configurations:

```bash
# Base + Staging overlay
kubectl apply -k k8s/staging/

# Base + Production overlay
kubectl apply -k k8s/production/
```

## Security

### Network Policies

Apply network policies to restrict traffic:

```bash
kubectl apply -f k8s/security/network-policies.yaml
```

### Pod Security Standards

The deployment follows Pod Security Standards:
- No privileged containers
- Non-root user execution
- Read-only root filesystem where possible

## Support

For detailed deployment guide, see [ENTERPRISE_DEPLOYMENT.md](../docs/ENTERPRISE_DEPLOYMENT.md)
