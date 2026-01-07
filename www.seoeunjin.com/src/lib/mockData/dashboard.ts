// 대시보드 통합 Mock 데이터

export interface DashboardOverview {
  renewableEnergy: {
    todayGeneration: number; // MWh
    carbonReduction: number; // 톤 CO₂
    capacity: number; // MW
    utilizationRate: number; // %
  };
  biochar: {
    todayProduction: number; // 톤
    carbonStored: number; // 톤 CO₂eq
    facilitiesActive: number;
    totalFacilities: number;
  };
  greenHydrogen: {
    todayProduction: number; // kg
    surplusUsed: number; // MWh
    carbonReduction: number; // 톤 CO₂
  };
  dualCarbonScore: number; // 0-100
}

export const mockDashboardOverview: DashboardOverview = {
  renewableEnergy: {
    todayGeneration: 15420, // MWh
    carbonReduction: 7234, // 톤 CO₂
    capacity: 850, // MW
    utilizationRate: 76,
  },
  biochar: {
    todayProduction: 82, // 톤
    carbonStored: 125, // 톤 CO₂eq
    facilitiesActive: 3,
    totalFacilities: 4,
  },
  greenHydrogen: {
    todayProduction: 3280, // kg
    surplusUsed: 164, // MWh
    carbonReduction: 32.8, // 톤 CO₂
  },
  dualCarbonScore: 87,
};

// Dual Carbon Score 계산
export const calculateDualCarbonScore = (
  renewableCO2: number,
  biocharCO2: number,
  targetCO2: number = 10000 // 목표 탄소감축량 (톤/일)
): number => {
  const totalReduction = renewableCO2 + biocharCO2;
  const achievementRate = (totalReduction / targetCO2) * 100;
  
  // 가중치 적용 (재생에너지 60%, 바이오차 40%)
  const renewableWeight = (renewableCO2 / totalReduction) * 0.6;
  const biocharWeight = (biocharCO2 / totalReduction) * 0.4;
  
  const balanceBonus = Math.abs(renewableWeight - biocharWeight) < 0.1 ? 10 : 0;
  
  return Math.min(Math.round(achievementRate + balanceBonus), 100);
};

// 실시간 알림
export interface RealtimeAlert {
  id: string;
  type: 'info' | 'warning' | 'success' | 'error';
  title: string;
  message: string;
  timestamp: Date;
  actionRequired: boolean;
}

export const mockRealtimeAlerts: RealtimeAlert[] = [
  {
    id: '1',
    type: 'success',
    title: '재생에너지 과잉 발생',
    message: '현재 잉여전력 120MW - 바이오차 가스화 전환 추천',
    timestamp: new Date(Date.now() - 5 * 60000),
    actionRequired: true,
  },
  {
    id: '2',
    type: 'info',
    title: '수소 생산량 목표 달성',
    message: '오늘 수소 생산 3,280kg 달성 (목표 대비 109%)',
    timestamp: new Date(Date.now() - 15 * 60000),
    actionRequired: false,
  },
  {
    id: '3',
    type: 'warning',
    title: '풍력 발전 예측 변동',
    message: '오후 3시 풍속 감소 예상 - 발전량 20% 감소',
    timestamp: new Date(Date.now() - 30 * 60000),
    actionRequired: false,
  },
];

// 제주도 시설 위치 (통합)
export interface FacilityLocation {
  id: string;
  name: string;
  type: 'solar' | 'wind' | 'biochar' | 're100' | 'hydrogen';
  location: { lat: number; lng: number };
  status: 'active' | 'idle' | 'maintenance' | 'warning';
  capacity?: number;
  floodRisk?: 'low' | 'medium' | 'high';
}

export const mockFacilityLocations: FacilityLocation[] = [
  // 풍력
  {
    id: 'wind-1',
    name: '제주 해상풍력 A',
    type: 'wind',
    location: { lat: 33.2312, lng: 126.3124 },
    status: 'active',
    capacity: 100,
    floodRisk: 'low',
  },
  {
    id: 'wind-2',
    name: '한경 육상풍력',
    type: 'wind',
    location: { lat: 33.3421, lng: 126.1823 },
    status: 'active',
    capacity: 80,
    floodRisk: 'medium',
  },
  // 태양광
  {
    id: 'solar-1',
    name: '서귀포 태양광 단지',
    type: 'solar',
    location: { lat: 33.2456, lng: 126.5678 },
    status: 'active',
    capacity: 50,
    floodRisk: 'low',
  },
  {
    id: 'solar-2',
    name: '제주시 태양광 파크',
    type: 'solar',
    location: { lat: 33.5102, lng: 126.4914 },
    status: 'active',
    capacity: 40,
    floodRisk: 'high',
  },
  // 바이오차
  {
    id: 'biochar-1',
    name: '제주 바이오차 센터 A',
    type: 'biochar',
    location: { lat: 33.4890, lng: 126.4900 },
    status: 'active',
    capacity: 10,
    floodRisk: 'medium',
  },
  {
    id: 'biochar-2',
    name: '서귀포 가스화 플랜트',
    type: 'biochar',
    location: { lat: 33.2541, lng: 126.5601 },
    status: 'active',
    capacity: 15,
    floodRisk: 'low',
  },
  // RE100
  {
    id: 're100-1',
    name: '제주 데이터센터 A',
    type: 're100',
    location: { lat: 33.4996, lng: 126.5312 },
    status: 'active',
    floodRisk: 'low',
  },
  // 수소
  {
    id: 'hydrogen-1',
    name: '제주 그린수소 생산기지',
    type: 'hydrogen',
    location: { lat: 33.4123, lng: 126.2900 },
    status: 'active',
    capacity: 5,
    floodRisk: 'medium',
  },
];

// 월별 통합 실적
export const mockMonthlyPerformance = [
  { month: '1월', renewable: 380000, biochar: 2100, hydrogen: 85000, score: 82 },
  { month: '2월', renewable: 360000, biochar: 1950, hydrogen: 78000, score: 79 },
  { month: '3월', renewable: 410000, biochar: 2250, hydrogen: 92000, score: 85 },
  { month: '4월', renewable: 450000, biochar: 2400, hydrogen: 98000, score: 88 },
  { month: '5월', renewable: 480000, biochar: 2600, hydrogen: 105000, score: 91 },
  { month: '6월', renewable: 465000, biochar: 2480, hydrogen: 101000, score: 89 },
  { month: '7월', renewable: 420000, biochar: 2300, hydrogen: 94000, score: 86 },
  { month: '8월', renewable: 440000, biochar: 2380, hydrogen: 97000, score: 87 },
  { month: '9월', renewable: 455000, biochar: 2450, hydrogen: 99500, score: 88 },
  { month: '10월', renewable: 470000, biochar: 2550, hydrogen: 103000, score: 90 },
  { month: '11월', renewable: 430000, biochar: 2350, hydrogen: 95000, score: 87 },
  { month: '12월', renewable: 400000, biochar: 2200, hydrogen: 88000, score: 84 },
];

// 시간대별 에너지 플로우
export interface EnergyFlow {
  hour: number;
  generation: number; // MW
  demand: number; // MW
  surplus: number; // MW
  toBiochar: number; // MW
  toHydrogen: number; // MW
  toBattery: number; // MW
}

export const mockEnergyFlow: EnergyFlow[] = Array.from({ length: 24 }, (_, hour) => {
  const baseGeneration = 600 + Math.sin((hour - 12) * Math.PI / 12) * 200;
  const baseDemand = 500 + Math.sin((hour - 14) * Math.PI / 12) * 100;
  const generation = Math.max(baseGeneration, 0);
  const demand = Math.max(baseDemand, 0);
  const surplus = Math.max(generation - demand, 0);
  
  return {
    hour,
    generation: Math.round(generation),
    demand: Math.round(demand),
    surplus: Math.round(surplus),
    toBiochar: Math.round(surplus * 0.3),
    toHydrogen: Math.round(surplus * 0.5),
    toBattery: Math.round(surplus * 0.2),
  };
});


