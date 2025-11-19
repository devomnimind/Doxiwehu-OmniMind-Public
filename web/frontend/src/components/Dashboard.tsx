import { useEffect, useCallback } from 'react';
import { useAuthStore } from '../store/authStore';
import { useDaemonStore } from '../store/daemonStore';
import { apiService } from '../services/api';
import { DaemonStatus } from './DaemonStatus';
import { SystemMetrics } from './SystemMetrics';
import { TaskList } from './TaskList';
import { DaemonControls } from './DaemonControls';

export function Dashboard() {
  const logout = useAuthStore((state) => state.logout);
  const username = useAuthStore((state) => state.username);
  const { setStatus, setTasks, setLoading, setError } = useDaemonStore();

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [status, tasks] = await Promise.all([
        apiService.getDaemonStatus(),
        apiService.getDaemonTasks(),
      ]);
      setStatus(status);
      setTasks(tasks);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch data');
      console.error('Fetch error:', err);
    } finally {
      setLoading(false);
    }
  }, [setStatus, setTasks, setLoading, setError]);

  useEffect(() => {
    fetchData();
    // Refresh every 5 seconds
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, [fetchData]);

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <h1 className="text-3xl font-bold text-white">🧠 OmniMind Dashboard</h1>
              <button
                onClick={fetchData}
                className="px-3 py-1 bg-gray-700 hover:bg-gray-600 text-white rounded-lg text-sm transition-colors"
              >
                🔄 Refresh
              </button>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-gray-400">Welcome, <span className="text-white font-semibold">{username}</span></span>
              <button
                onClick={logout}
                className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg font-semibold transition-colors"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Status and Controls */}
          <div className="lg:col-span-2 space-y-6">
            <DaemonStatus />
            <TaskList />
          </div>

          {/* Right Column - Metrics and Controls */}
          <div className="space-y-6">
            <SystemMetrics />
            <DaemonControls />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 border-t border-gray-700 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-gray-400 text-sm">
            <p>OmniMind Autonomous Agent System</p>
            <p className="mt-1">24/7 Background Task Execution</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
