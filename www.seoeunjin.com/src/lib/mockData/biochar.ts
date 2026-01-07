// 바이오차 Mock 데이터

export interface BiocharMaterial {
  id: string;
  name: string;
  nameEn: string;
  carbonContent: number; // %
  yield: number; // %
  costPerTon: number; // 원/톤
}

export interface BiocharProduction {
  material: string;
  inputAmount: number; // 톤
  outputAmount: number; // 톤
  carbonStored: number; // 톤 CO₂eq
  temperature: number; // °C
  duration: number; // 시간
}

export interface BiocharFacility {
  id: number;
  name: string;
  location: { lat: number; lng: number };
  type: 'pyrolysis' | 'gasification' | 'hybrid';
  capacity: number; // 톤/일
  currentProduction: number;
  status: 'active' | 'idle' | 'maintenance';
}

// 원료 종류별 특성
export const biocharMaterials: BiocharMaterial[] = [
  {
    id: 'food-waste',
    name: '음식물 쓰레기',
    nameEn: 'Food Waste',
    carbonContent: 45,
    yield: 35,
    costPerTon: 50000,
  },
  {
    id: 'livestock',
    name: '가축분뇨',
    nameEn: 'Livestock Manure',
    carbonContent: 38,
    yield: 30,
    costPerTon: 30000,
  },
  {
    id: 'forestry',
    name: '산림 부산물',
    nameEn: 'Forestry Residue',
    carbonContent: 52,
    yield: 40,
    costPerTon: 80000,
  },
  {
    id: 'agricultural',
    name: '농업 부산물',
    nameEn: 'Agricultural Residue',
    carbonContent: 42,
    yield: 32,
    costPerTon: 40000,
  },
  {
    id: 'seaweed',
    name: '해조류',
    nameEn: 'Seaweed',
    carbonContent: 35,
    yield: 28,
    costPerTon: 60000,
  },
];

// 바이오차 생산 시설 (제주도)
export const mockBiocharFacilities: BiocharFacility[] = [
  {
    id: 1,
    name: '제주 바이오차 생산센터 A',
    location: { lat: 33.4890, lng: 126.4900 },
    type: 'pyrolysis',
    capacity: 10,
    currentProduction: 8.5,
    status: 'active',
  },
  {
    id: 2,
    name: '서귀포 가스화 플랜트',
    location: { lat: 33.2541, lng: 126.5601 },
    type: 'gasification',
    capacity: 15,
    currentProduction: 12.3,
    status: 'active',
  },
  {
    id: 3,
    name: '제주 동부 바이오차 공장',
    location: { lat: 33.5088, lng: 126.6594 },
    type: 'hybrid',
    capacity: 12,
    currentProduction: 0,
    status: 'maintenance',
  },
  {
    id: 4,
    name: '한림 순환자원 센터',
    location: { lat: 33.4120, lng: 126.2694 },
    type: 'pyrolysis',
    capacity: 8,
    currentProduction: 7.2,
    status: 'active',
  },
];

// 바이오차 생산량 계산 함수
export const calculateBiocharProduction = (
  materialId: string,
  inputAmount: number,
  temperature: number = 500
): BiocharProduction => {
  const material = biocharMaterials.find(m => m.id === materialId);
  if (!material) {
    throw new Error('Invalid material');
  }

  // 온도에 따른 수율 조정 (400-600°C 최적)
  const tempFactor = temperature >= 400 && temperature <= 600 ? 1.0 : 0.85;
  const outputAmount = (inputAmount * material.yield * tempFactor) / 100;

  // 탄소 저장량 계산 (CO₂eq)
  // 바이오차 탄소 함량 * 탄소의 CO₂ 전환 계수 (3.67)
  const carbonStored = (outputAmount * material.carbonContent * 3.67) / 100;

  return {
    material: material.name,
    inputAmount,
    outputAmount,
    carbonStored,
    temperature,
    duration: 4, // 평균 4시간
  };
};

// 토양 개량 효과
export interface SoilImprovementEffect {
  waterRetention: number; // % 증가
  nutrientRetention: number; // % 증가
  phAdjustment: number;
  microbialActivity: number; // % 증가
}

export const calculateSoilImprovement = (
  biocharAmount: number // kg/m²
): SoilImprovementEffect => {
  return {
    waterRetention: Math.min(biocharAmount * 15, 60),
    nutrientRetention: Math.min(biocharAmount * 12, 50),
    phAdjustment: biocharAmount * 0.3,
    microbialActivity: Math.min(biocharAmount * 20, 80),
  };
};

// CCUS 성능 점수 (0-100)
export const calculateCCUSScore = (
  carbonStored: number,
  productionEfficiency: number,
  costEffectiveness: number
): number => {
  const storageScore = Math.min((carbonStored / 100) * 40, 40);
  const efficiencyScore = Math.min(productionEfficiency * 0.4, 30);
  const costScore = Math.min((1 / costEffectiveness) * 30, 30);
  
  return Math.round(storageScore + efficiencyScore + costScore);
};

// 주간 바이오차 생산량
export const mockWeeklyBiocharProduction = [
  { day: '월', production: 85, carbonStored: 32 },
  { day: '화', production: 92, carbonStored: 35 },
  { day: '수', production: 78, carbonStored: 30 },
  { day: '목', production: 88, carbonStored: 34 },
  { day: '금', production: 95, carbonStored: 36 },
  { day: '토', production: 72, carbonStored: 28 },
  { day: '일', production: 68, carbonStored: 26 },
];

// 탄소 제거 비용 계산 ($/tCO₂)
export const calculateCarbonRemovalCost = (
  materialCost: number,
  operatingCost: number,
  carbonStored: number
): number => {
  const totalCost = materialCost + operatingCost;
  const usdExchangeRate = 1300; // 원/달러
  return (totalCost / usdExchangeRate) / carbonStored;
};


