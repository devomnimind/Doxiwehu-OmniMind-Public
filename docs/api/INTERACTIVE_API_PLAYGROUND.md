# Interactive API Playground Guide

## Overview

OmniMind provides an interactive API playground for exploring and testing API endpoints without writing code. This guide covers how to use the Swagger UI interface and Postman collections.

## Accessing the API Playground

### Swagger UI (Built-in)

The interactive API documentation is available at:

```
http://localhost:8000/docs
```

When the backend server is running, navigate to this URL to access the full interactive API playground.

### Alternative: ReDoc

For a different documentation style, access ReDoc at:

```
http://localhost:8000/redoc
```

## Using Swagger UI

### 1. Authentication

Most endpoints require Basic Authentication:

1. Click the **"Authorize"** button at the top right
2. Enter your credentials:
   - Username: Your dashboard username
   - Password: Your dashboard password
3. Click **"Authorize"**
4. Click **"Close"**

### 2. Exploring Endpoints

Endpoints are organized by tags:

- **Health**: System health checks and trends
- **Daemon**: Daemon status, tasks, and control
- **Messages**: Message polling and posting
- **WebSocket**: Real-time metrics broadcasting

### 3. Testing Endpoints

To test an endpoint:

1. Click on the endpoint to expand it
2. Click **"Try it out"**
3. Fill in required parameters
4. Click **"Execute"**
5. View the response below

### 4. Example Requests

Each endpoint includes example requests and responses. Click on "Example Value" to see sample data.

## Postman Collections

### Importing the Collection

1. Generate the Postman collection:
   ```bash
   python -c "from src.security.api_documentation import APIDocumentationGenerator; gen = APIDocumentationGenerator(); gen.generate_postman_collection()"
   ```

2. Import into Postman:
   - Open Postman
   - Click **"Import"**
   - Select `docs/api/OmniMind_API.postman_collection.json`
   - Click **"Import"**

### Setting Up Environment Variables

Create a Postman environment with these variables:

```json
{
  "name": "OmniMind Local",
  "values": [
    {
      "key": "base_url",
      "value": "http://localhost:8000",
      "enabled": true
    },
    {
      "key": "username",
      "value": "your_username",
      "enabled": true
    },
    {
      "key": "password",
      "value": "your_password",
      "enabled": true,
      "type": "secret"
    }
  ]
}
```

### Using the Collection

1. Select the "OmniMind Local" environment
2. Navigate to the desired request folder
3. Click on a request
4. Click **"Send"**
5. View the response

## Common API Workflows

### 1. Health Check

```bash
GET /api/v1/health/
```

No authentication required. Returns system health status.

### 2. Get Daemon Status

```bash
GET /daemon/status
Authorization: Basic <credentials>
```

Returns comprehensive daemon status with consciousness metrics.

### 3. List Tasks

```bash
GET /daemon/tasks
Authorization: Basic <credentials>
```

Returns list of active tasks from Tribunal.

### 4. Add Task

```bash
POST /daemon/tasks/add
Authorization: Basic <credentials>

{
  "task_id": "example_task",
  "description": "Example task description",
  "priority": "NORMAL"
}
```

### 5. Get Messages

```bash
GET /api/omnimind/messages
Authorization: Basic <credentials>
```

Returns pending messages for polling clients.

## API Rate Limits

Currently, there are no hard rate limits, but consider:

- Maximum 100 concurrent requests
- Websocket connections: 50 simultaneous connections
- Task orchestration: 10 concurrent tasks

## Response Formats

All responses are in JSON format:

### Success Response
```json
{
  "status": "success",
  "data": { ... }
}
```

### Error Response
```json
{
  "error": "Error description",
  "detail": "Detailed error message",
  "code": "ERROR_CODE"
}
```

## Advanced Features

### WebSocket Testing

For real-time metrics updates, use the WebSocket endpoint:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onopen = () => {
  console.log('Connected to OmniMind WebSocket');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);

  // Handle different message types
  if (data.type === 'metrics_update') {
    console.log('Metrics update:', data.data);
  } else if (data.type === 'metrics') {
    console.log('Sinthome metrics:', data.data);
  }
};

// Send ping to keep connection alive
setInterval(() => {
  ws.send(JSON.stringify({ type: 'ping', id: Date.now() }));
}, 30000);
```

## Troubleshooting

### Authentication Errors

**Error:** 401 Unauthorized

**Solution:**
1. Verify credentials in `config/dashboard_auth.json`
2. Check environment variables:
   ```bash
   echo $OMNIMIND_DASHBOARD_USER
   echo $OMNIMIND_DASHBOARD_PASS
   ```

### Connection Refused

**Error:** Connection refused to localhost:8000

**Solution:**
1. Start the backend server:
   ```bash
   source scripts/start_dashboard.sh
   ```
2. Verify server is running:
   ```bash
   curl http://localhost:8000/api/v1/health/
   ```

### CORS Errors

**Error:** CORS policy blocked

**Solution:**
The server allows all origins by default. If you're having issues:
1. Check that you're accessing from the correct origin
2. Verify the server configuration in `web/backend/main.py`

## SDK Code Examples

### Python

```python
from omnimind_sdk import OmniMindClient

client = OmniMindClient(
    base_url="http://localhost:8000",
    username="your_username",
    password="your_password"
)

# Submit task
task = client.submit_task(
    description="Analyze security vulnerabilities",
    priority="high"
)

# Get task status
status = client.get_task(task['task_id'])
print(f"Task status: {status['status']}")

# List all tasks
tasks = client.list_tasks(status="running")
```

### JavaScript

```javascript
import { OmniMindClient } from './omnimind-sdk';

const client = new OmniMindClient({
  baseUrl: 'http://localhost:8000',
  username: 'your_username',
  password: 'your_password'
});

// Submit task
const task = await client.submitTask({
  description: 'Analyze security vulnerabilities',
  priority: 'high'
});

// Get task status
const status = await client.getTask(task.task_id);
console.log(`Task status: ${status.status}`);

// List all tasks
const tasks = await client.listTasks({ status: 'running' });
```

## Additional Resources

- [API Reference](./API_DOCUMENTATION.md)
- [Authentication Guide](./AUTHENTICATION.md)
- [WebSocket Guide](./WEBSOCKET_GUIDE.md)
- [Performance Tuning](./PERFORMANCE_TUNING.md)
- [Troubleshooting](./TROUBLESHOOTING.md)
