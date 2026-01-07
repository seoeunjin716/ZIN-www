// 그린수소 Mock 데이터

export interface ElectrolyzerType {
  id: string;
  name: string;
  nameKo: string;
  efficiency: number; // %
  powerConsumption: number; // kWh/kg H₂
  capex: number; // 억원/MW
  opex: number; // 억원/년
  lifespan: number; // 년
}

export interface HydrogenProduction {
  electrolyzerType: string;
  inputPowerMW: number;
  outputKg: number;
  productionCost: number; // 원/kg
  carbonReduction: number; // kg CO₂
}

export interface HydrogenStorage {
  type: 'compressed' | 'liquid' | 'lohc' | 'ammonia';
  capacity: number; // kg
  cost: number; // 원/kg
  efficiency: number; // %
}

// 수전해 방식
export const electrolyzerTypes: ElectrolyzerType[] = [
  {
    id: 'pem',
    name: 'PEM',
    nameKo: '고분자전해질막',
    efficiency: 70,
    powerConsumption: 50, // kWh/kg
    capex: 15,
    opex: 0.5,
    lifespan: 20,
  },
  {
    id: 'alkaline',
    name: 'Alkaline',
    nameKo: '알칼라인',
    efficiency: 65,
    powerConsumption: 54,
    capex: 8,
    opex: 0.3,
    lifespan: 25,
  },
  {
    id: 'aem',
    name: 'AEM',
    nameKo: '음이온교환막',
    efficiency: 68,
    powerConsumption: 52,
    capex: 12,
    opex: 0.4,
    lifespan: 15,
  },
  {
    id: 'soec',
    name: 'SOEC',
    nameKo: '고온수증기전기분해',
    efficiency: 85,
    powerConsumption: 40,
    capex: 20,
    opex: 0.8,
    lifespan: 10,
  },
];

// 그린수소 생산 계산
export const calculateHydrogenProduction = (
  electrolyzerTypeId: string,
  surplusPowerMW: number,
  electricityPrice: number = 80 // 원/kWh (SMP 평균)
): HydrogenProduction => {
  const electrolyzer = electrolyzerTypes.find(e => e.id === electrolyzerTypeId);
  if (!electrolyzer) {
    throw new Error('Invalid electrolyzer type');
  }

  // 수소 생산량 계산
  const powerKWh = surplusPowerMW * 1000; // MW → kWh
  const outputKg = (powerKWh / electrolyzer.powerConsumption) * (electrolyzer.efficiency / 100);

  // 생산 비용 계산
  const electricityCost = powerKWh * electricityPrice;
  const maintenanceCost = (electrolyzer.opex * 100000000) / (365 * 24); // 시간당
  const productionCost = (electricityCost + maintenanceCost) / outputKg;

  // 탄소 감축량 (그레이수소 대비)
  // 그레이수소: 약 10 kg CO₂/kg H₂
  const carbonReduction = outputKg * 10;

  return {
    electrolyzerType: electrolyzer.nameKo,
    inputPowerMW: surplusPowerMW,
    outputKg: Math.round(outputKg * 100) / 100,
    productionCost: Math.round(productionCost),
    carbonReduction: Math.round(carbonReduction),
  };
};

// 저장 방식
export const hydrogenStorageTypes: HydrogenStorage[] = [
  {
    type: 'compressed',
    capacity: 1000,
    cost: 3000,
    efficiency: 95,
  },
  {
    type: 'liquid',
    capacity: 5000,
    cost: 5000,
    efficiency: 85,
  },
  {
    type: 'lohc',
    capacity: 3000,
    cost: 4000,
    efficiency: 90,
  },
  {
    type: 'ammonia',
    capacity: 10000,
    cost: 3500,
    efficiency: 88,
  },
];

// 바이오차 기반 수소 생산 (가스화)
export interface BiocharGasification {
  biocharInputKg: number;
  synGasOutput: number; // Nm³
  hydrogenPurity: number; // %
  hydrogenOutputKg: number;
  byproductBiocharKg: number;
  carbonCaptured: number; // kg CO₂
}

export const calculateBiocharGasification = (
  biocharInputKg: number
): BiocharGasification => {
  // 바이오차 가스화 → 합성가스 → 수소
  const synGasOutput = biocharInputKg * 2.5; // Nm³
  const hydrogenPurity = 55; // %
  const hydrogenOutputKg = (synGasOutput * hydrogenPurity / 100) * 0.09; // H₂ 밀도 0.09 kg/Nm³
  
  // 부산물 바이오차 (일부 남음)
  const byproductBiocharKg = biocharInputKg * 0.3;
  
  // 탄소 포집 (CCUS)
  const carbonCaptured = biocharInputKg * 0.5 * 3.67; // CO₂eq

  return {
    biocharInputKg,
    synGasOutput: Math.round(synGasOutput * 100) / 100,
    hydrogenPurity,
    hydrogenOutputKg: Math.round(hydrogenOutputKg * 100) / 100,
    byproductBiocharKg: Math.round(byproductBiocharKg * 100) / 100,
    carbonCaptured: Math.round(carbonCaptured * 100) / 100,
  };
};

// 경제성 분석
export interface EconomicAnalysis {
  lcoe: number; // 균등화발전비용 (원/kWh)
  lch: number; // 균등화수소비용 (원/kg)
  paybackPeriod: number; // 년
  npv: number; // 순현재가치 (억원)
  irr: number; // 내부수익률 (%)
}

export const calculateEconomics = (
  capacity: number, // MW
  electrolyzerType: string,
  electricityPrice: number,
  sellingPrice: number = 7000 // 원/kg (수소 판매가)
): EconomicAnalysis => {
  const electrolyzer = electrolyzerTypes.find(e => e.id === electrolyzerType);
  if (!electrolyzer) {
    throw new Error('Invalid electrolyzer type');
  }

  const annualProduction = (capacity * 1000 * 8760) / electrolyzer.powerConsumption; // kg/년
  const annualRevenue = annualProduction * sellingPrice;
  const annualCost = (capacity * 1000 * 8760 * electricityPrice) + (electrolyzer.opex * 100000000);
  
  const initialInvestment = electrolyzer.capex * capacity * 100000000;
  const annualCashFlow = annualRevenue - annualCost;
  
  // 단순 회수기간
  const paybackPeriod = initialInvestment / annualCashFlow;
  
  // NPV (할인율 5%)
  const discountRate = 0.05;
  let npv = -initialInvestment;
  for (let year = 1; year <= electrolyzer.lifespan; year++) {
    npv += annualCashFlow / Math.pow(1 + discountRate, year);
  }
  
  // LCOE & LCH
  const lcoe = electricityPrice * 1.2; // 간소화
  const lch = (initialInvestment / annualProduction / electrolyzer.lifespan) + 
               (annualCost / annualProduction);

  return {
    lcoe: Math.round(lcoe),
    lch: Math.round(lch),
    paybackPeriod: Math.round(paybackPeriod * 10) / 10,
    npv: Math.round(npv / 100000000),
    irr: 12.5, // 간소화
  };
};

// 주간 수소 생산량
export const mockWeeklyHydrogenProduction = [
  { day: '월', production: 420, surplus: 85 },
  { day: '화', production: 380, surplus: 72 },
  { day: '수', production: 450, surplus: 95 },
  { day: '목', production: 490, surplus: 102 },
  { day: '금', production: 410, surplus: 88 },
  { day: '토', production: 520, surplus: 115 },
  { day: '일', production: 480, surplus: 98 },
];

// 수소 활용 시나리오
export const hydrogenUseCases = [
  {
    id: 'fuel-cell',
    name: '연료전지 발전',
    nameEn: 'Fuel Cell Power',
    efficiency: 60,
    outputKWh: 33.3, // per kg H₂
  },
  {
    id: 'mobility',
    name: '수소차 충전',
    nameEn: 'Hydrogen Vehicle',
    efficiency: 50,
    range: 100, // km per kg H₂
  },
  {
    id: 'industry',
    name: '산업용 원료',
    nameEn: 'Industrial Feedstock',
    efficiency: 95,
    application: '철강, 화학',
  },
  {
    id: 'energy-storage',
    name: '에너지 저장',
    nameEn: 'Energy Storage',
    efficiency: 40,
    duration: 'long-term',
  },
];


