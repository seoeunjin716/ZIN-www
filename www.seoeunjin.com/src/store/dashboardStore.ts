import { create } from 'zustand';
import { 
  DashboardOverview, 
  mockDashboardOverview,
  RealtimeAlert,
  mockRealtimeAlerts,
  FacilityLocation,
  mockFacilityLocations,
} from '@/lib/mockData/dashboard';

interface DashboardState {
  overview: DashboardOverview;
  alerts: RealtimeAlert[];
  facilities: FacilityLocation[];
  selectedFacility: FacilityLocation | null;
  isLoading: boolean;
  
  // Actions
  updateOverview: (overview: Partial<DashboardOverview>) => void;
  addAlert: (alert: RealtimeAlert) => void;
  dismissAlert: (alertId: string) => void;
  setSelectedFacility: (facility: FacilityLocation | null) => void;
  fetchDashboardData: () => Promise<void>;
}

export const useDashboardStore = create<DashboardState>((set) => ({
  overview: mockDashboardOverview,
  alerts: mockRealtimeAlerts,
  facilities: mockFacilityLocations,
  selectedFacility: null,
  isLoading: false,

  updateOverview: (updates) =>
    set((state) => ({
      overview: { ...state.overview, ...updates },
    })),

  addAlert: (alert) =>
    set((state) => ({
      alerts: [alert, ...state.alerts].slice(0, 10), // 최근 10개만 유지
    })),

  dismissAlert: (alertId) =>
    set((state) => ({
      alerts: state.alerts.filter((a) => a.id !== alertId),
    })),

  setSelectedFacility: (facility) =>
    set({ selectedFacility: facility }),

  fetchDashboardData: async () => {
    set({ isLoading: true });
    try {
      // Mock API call
      await new Promise((resolve) => setTimeout(resolve, 500));
      // 실제로는 API 호출
      // const data = await fetchDashboardAPI();
      set({
        overview: mockDashboardOverview,
        alerts: mockRealtimeAlerts,
        facilities: mockFacilityLocations,
      });
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      set({ isLoading: false });
    }
  },
}));


