import type { DaemonStatus, DaemonTask, AddTaskRequest } from '../types/daemon';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ApiService {
  private username: string = '';
  private password: string = '';

  setCredentials(username: string, password: string) {
    this.username = username;
    this.password = password;
  }

  private getAuthHeader(): string {
    const credentials = btoa(`${this.username}:${this.password}`);
    return `Basic ${credentials}`;
  }

  getHeaders(): HeadersInit {
    return {
      'Authorization': this.getAuthHeader(),
      'Content-Type': 'application/json',
    };
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const headers = {
      'Authorization': this.getAuthHeader(),
      'Content-Type': 'application/json',
      ...options.headers,
    };

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async getDaemonStatus(): Promise<DaemonStatus> {
    return this.request<DaemonStatus>('/daemon/status');
  }

  async getDaemonTasks(): Promise<DaemonTask[]> {
    return this.request<DaemonTask[]>('/daemon/tasks');
  }

  async addTask(task: AddTaskRequest): Promise<{ message: string; task_id: string }> {
    return this.request('/daemon/tasks/add', {
      method: 'POST',
      body: JSON.stringify(task),
    });
  }

  async startDaemon(): Promise<{ message: string }> {
    return this.request('/daemon/start', { method: 'POST' });
  }

  async stopDaemon(): Promise<{ message: string }> {
    return this.request('/daemon/stop', { method: 'POST' });
  }
}

export const apiService = new ApiService();
