import { create } from 'zustand';
import {
  BiocharMaterial,
  BiocharProduction,
  BiocharFacility,
  biocharMaterials,
  mockBiocharFacilities,
  calculateBiocharProduction,
} from '@/lib/mockData/biochar';

interface BiocharState {
  materials: BiocharMaterial[];
  facilities: BiocharFacility[];
  currentProduction: BiocharProduction | null;
  selectedMaterial: BiocharMaterial | null;
  inputAmount: number;
  temperature: number;
  isLoading: boolean;
  
  // Actions
  setSelectedMaterial: (material: BiocharMaterial | null) => void;
  setInputAmount: (amount: number) => void;
  setTemperature: (temp: number) => void;
  calculateProduction: () => void;
  fetchBiocharData: () => Promise<void>;
}

export const useBiocharStore = create<BiocharState>((set, get) => ({
  materials: biocharMaterials,
  facilities: mockBiocharFacilities,
  currentProduction: null,
  selectedMaterial: null,
  inputAmount: 0,
  temperature: 500,
  isLoading: false,

  setSelectedMaterial: (material) =>
    set({ selectedMaterial: material }),

  setInputAmount: (amount) =>
    set({ inputAmount: amount }),

  setTemperature: (temp) =>
    set({ temperature: temp }),

  calculateProduction: () => {
    const { selectedMaterial, inputAmount, temperature } = get();
    if (!selectedMaterial || inputAmount <= 0) {
      return;
    }
    
    const production = calculateBiocharProduction(
      selectedMaterial.id,
      inputAmount,
      temperature
    );
    
    set({ currentProduction: production });
  },

  fetchBiocharData: async () => {
    set({ isLoading: true });
    try {
      await new Promise((resolve) => setTimeout(resolve, 500));
      set({
        materials: biocharMaterials,
        facilities: mockBiocharFacilities,
      });
    } catch (error) {
      console.error('Failed to fetch biochar data:', error);
    } finally {
      set({ isLoading: false });
    }
  },
}));


