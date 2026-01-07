// 재생에너지 Mock 데이터
export interface EnergyGeneration {
  solar: number;
  wind: number;
  total: number;
  timestamp: Date;
}

export interface EnergyForecast {
  hour: number;
  solar: number;
  wind: number;
  temperature: number;
  cloudCover: number;
}

export interface CurtailmentData {
  todayEvents: number;
  totalLossMWh: number;
  currentStatus: 'normal' | 'warning' | 'curtailment';
  affectedCapacity: number;
}

// 실시간 발전량 (제주도 기준 예시)
export const mockRealtimeEnergy: EnergyGeneration = {
  solar: 450.5, // MW
  wind: 320.2,  // MW
  total: 770.7,
  timestamp: new Date(),
};

// 24시간 발전량 예측
export const mockEnergyForecast: EnergyForecast[] = [
  { hour: 0, solar: 0, wind: 280, temperature: 12, cloudCover: 30 },
  { hour: 1, solar: 0, wind: 265, temperature: 11, cloudCover: 35 },
  { hour: 2, solar: 0, wind: 290, temperature: 11, cloudCover: 40 },
  { hour: 3, solar: 0, wind: 310, temperature: 10, cloudCover: 45 },
  { hour: 4, solar: 0, wind: 295, temperature: 10, cloudCover: 50 },
  { hour: 5, solar: 0, wind: 280, temperature: 11, cloudCover: 45 },
  { hour: 6, solar: 50, wind: 270, temperature: 12, cloudCover: 40 },
  { hour: 7, solar: 150, wind: 260, temperature: 14, cloudCover: 35 },
  { hour: 8, solar: 280, wind: 250, temperature: 16, cloudCover: 30 },
  { hour: 9, solar: 380, wind: 240, temperature: 18, cloudCover: 25 },
  { hour: 10, solar: 450, wind: 230, temperature: 20, cloudCover: 20 },
  { hour: 11, solar: 490, wind: 225, temperature: 22, cloudCover: 15 },
  { hour: 12, solar: 520, wind: 220, temperature: 23, cloudCover: 10 },
  { hour: 13, solar: 510, wind: 225, temperature: 24, cloudCover: 10 },
  { hour: 14, solar: 480, wind: 235, temperature: 24, cloudCover: 15 },
  { hour: 15, solar: 420, wind: 250, temperature: 23, cloudCover: 20 },
  { hour: 16, solar: 330, wind: 270, temperature: 22, cloudCover: 25 },
  { hour: 17, solar: 200, wind: 290, temperature: 20, cloudCover: 30 },
  { hour: 18, solar: 80, wind: 310, temperature: 18, cloudCover: 35 },
  { hour: 19, solar: 10, wind: 330, temperature: 16, cloudCover: 40 },
  { hour: 20, solar: 0, wind: 340, temperature: 15, cloudCover: 40 },
  { hour: 21, solar: 0, wind: 325, temperature: 14, cloudCover: 35 },
  { hour: 22, solar: 0, wind: 310, temperature: 13, cloudCover: 30 },
  { hour: 23, solar: 0, wind: 295, temperature: 12, cloudCover: 30 },
];

// 출력 제한 (Curtailment) 데이터
export const mockCurtailmentData: CurtailmentData = {
  todayEvents: 3,
  totalLossMWh: 45.2,
  currentStatus: 'warning',
  affectedCapacity: 120, // MW
};

// 잉여 전력 계산 (간소화)
export const calculateSurplusEnergy = (
  generation: number,
  demand: number
): number => {
  return Math.max(0, generation - demand);
};

// 주간 발전량 히스토리
export const mockWeeklyGeneration = [
  { day: '월', solar: 4200, wind: 3800, demand: 6500 },
  { day: '화', solar: 3900, wind: 4100, demand: 6400 },
  { day: '수', solar: 4500, wind: 3600, demand: 6300 },
  { day: '목', solar: 4800, wind: 3200, demand: 6500 },
  { day: '금', solar: 4300, wind: 3900, demand: 6700 },
  { day: '토', solar: 4600, wind: 3500, demand: 6000 },
  { day: '일', solar: 4400, wind: 3700, demand: 5800 },
];

// RE100 적용 사업장 데이터
export const mockRE100Sites = [
  {
    id: 1,
    name: '제주 데이터센터 A',
    location: { lat: 33.4996, lng: 126.5312 },
    capacity: 50, // MW
    currentLoad: 42,
    re100Status: 'certified',
  },
  {
    id: 2,
    name: '제주 산업단지 B',
    location: { lat: 33.4890, lng: 126.4983 },
    capacity: 30,
    currentLoad: 28,
    re100Status: 'in-progress',
  },
  {
    id: 3,
    name: '제주 스마트팜',
    location: { lat: 33.5145, lng: 126.5203 },
    capacity: 15,
    currentLoad: 12,
    re100Status: 'certified',
  },
];


