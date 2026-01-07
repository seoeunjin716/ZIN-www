import { create } from 'zustand';
import {
  ElectrolyzerType,
  HydrogenProduction,
  electrolyzerTypes,
  calculateHydrogenProduction,
} from '@/lib/mockData/hydrogen';

interface HydrogenState {
  electrolyzerTypes: ElectrolyzerType[];
  selectedElectrolyzer: ElectrolyzerType | null;
  surplusPower: number;
  electricityPrice: number;
  currentProduction: HydrogenProduction | null;
  isLoading: boolean;
  
  // Actions
  setSelectedElectrolyzer: (electrolyzer: ElectrolyzerType | null) => void;
  setSurplusPower: (power: number) => void;
  setElectricityPrice: (price: number) => void;
  calculateProduction: () => void;
  fetchHydrogenData: () => Promise<void>;
}

export const useHydrogenStore = create<HydrogenState>((set, get) => ({
  electrolyzerTypes,
  selectedElectrolyzer: electrolyzerTypes[0], // 기본값: PEM
  surplusPower: 0,
  electricityPrice: 80,
  currentProduction: null,
  isLoading: false,

  setSelectedElectrolyzer: (electrolyzer) =>
    set({ selectedElectrolyzer: electrolyzer }),

  setSurplusPower: (power) =>
    set({ surplusPower: power }),

  setElectricityPrice: (price) =>
    set({ electricityPrice: price }),

  calculateProduction: () => {
    const { selectedElectrolyzer, surplusPower, electricityPrice } = get();
    if (!selectedElectrolyzer || surplusPower <= 0) {
      return;
    }
    
    const production = calculateHydrogenProduction(
      selectedElectrolyzer.id,
      surplusPower,
      electricityPrice
    );
    
    set({ currentProduction: production });
  },

  fetchHydrogenData: async () => {
    set({ isLoading: true });
    try {
      await new Promise((resolve) => setTimeout(resolve, 500));
      // 실제로는 API 호출
    } catch (error) {
      console.error('Failed to fetch hydrogen data:', error);
    } finally {
      set({ isLoading: false });
    }
  },
}));


