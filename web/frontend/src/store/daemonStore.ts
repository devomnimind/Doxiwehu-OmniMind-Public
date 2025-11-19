import { create } from 'zustand';
import type { DaemonStatus, DaemonTask } from '../types/daemon';

interface DaemonState {
  status: DaemonStatus | null;
  tasks: DaemonTask[];
  loading: boolean;
  error: string | null;
  setStatus: (status: DaemonStatus) => void;
  setTasks: (tasks: DaemonTask[]) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useDaemonStore = create<DaemonState>((set) => ({
  status: null,
  tasks: [],
  loading: false,
  error: null,
  setStatus: (status) => set({ status }),
  setTasks: (tasks) => set({ tasks }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
}));
