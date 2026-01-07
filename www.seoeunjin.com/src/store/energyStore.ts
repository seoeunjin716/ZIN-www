import { create } from 'zustand';
import {
  EnergyGeneration,
  EnergyForecast,
  CurtailmentData,
  mockRealtimeEnergy,
  mockEnergyForecast,
  mockCurtailmentData,
} from '@/lib/mockData/energy';

interface EnergyState {
  currentGeneration: EnergyGeneration;
  forecast: EnergyForecast[];
  curtailment: CurtailmentData;
  surplusEnergy: number;
  isLoading: boolean;
  
  // Actions
  updateGeneration: (generation: EnergyGeneration) => void;
  updateForecast: (forecast: EnergyForecast[]) => void;
  calculateSurplus: (demand: number) => void;
  fetchEnergyData: () => Promise<void>;
}

export const useEnergyStore = create<EnergyState>((set, get) => ({
  currentGeneration: mockRealtimeEnergy,
  forecast: mockEnergyForecast,
  curtailment: mockCurtailmentData,
  surplusEnergy: 0,
  isLoading: false,

  updateGeneration: (generation) =>
    set({ currentGeneration: generation }),

  updateForecast: (forecast) =>
    set({ forecast }),

  calculateSurplus: (demand) => {
    const { currentGeneration } = get();
    const surplus = Math.max(0, currentGeneration.total - demand);
    set({ surplusEnergy: surplus });
  },

  fetchEnergyData: async () => {
    set({ isLoading: true });
    try {
      await new Promise((resolve) => setTimeout(resolve, 500));
      set({
        currentGeneration: mockRealtimeEnergy,
        forecast: mockEnergyForecast,
        curtailment: mockCurtailmentData,
      });
    } catch (error) {
      console.error('Failed to fetch energy data:', error);
    } finally {
      set({ isLoading: false });
    }
  },
}));


