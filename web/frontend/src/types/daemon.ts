export interface SystemMetrics {
  cpu_percent: number;
  memory_percent: number;
  disk_percent: number;
  is_user_active: boolean;
  idle_seconds: number;
  is_sleep_hours: boolean;
}

export interface TaskStats {
  total_executions: number;
  successful_executions: number;
  failed_executions: number;
  last_execution?: string;
  last_success?: string;
  last_failure?: string;
}

export interface DaemonTask {
  task_id: string;
  name: string;
  description: string;
  priority: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  repeat_interval_seconds: number | null;
  timeout_seconds: number;
  last_run?: string;
  next_run?: string;
  stats: TaskStats;
}

export interface DaemonStatus {
  running: boolean;
  uptime_seconds: number;
  system_metrics: SystemMetrics;
  task_count: number;
  completed_tasks: number;
  failed_tasks: number;
  cloud_connected: boolean;
}

export interface AddTaskRequest {
  task_id: string;
  name: string;
  description: string;
  code: string;
  priority: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  repeat_interval_seconds?: number;
  timeout_seconds?: number;
}
