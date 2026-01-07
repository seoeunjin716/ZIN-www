'use client';

import { useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useHydrogenStore } from '@/store/hydrogenStore';
import { Droplet, Zap, DollarSign, TrendingDown } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { mockWeeklyHydrogenProduction, hydrogenUseCases } from '@/lib/mockData/hydrogen';

export default function GreenHydrogenPage() {
  const {
    electrolyzerTypes,
    selectedElectrolyzer,
    surplusPower,
    electricityPrice,
    currentProduction,
    setSelectedElectrolyzer,
    setSurplusPower,
    setElectricityPrice,
    calculateProduction,
    fetchHydrogenData,
  } = useHydrogenStore();

  useEffect(() => {
    fetchHydrogenData();
  }, [fetchHydrogenData]);

  const handleCalculate = () => {
    calculateProduction();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-hydrogen-50 via-white to-blue-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">Green Hydrogen</h1>
          <p className="text-gray-600">재생에너지 기반 그린수소 생산 시뮬레이터</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="border-l-4 border-l-hydrogen-500">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">
                오늘 생산량
              </CardTitle>
              <Droplet className="h-5 w-5 text-hydrogen-500" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-gray-900">
                3,280
                <span className="text-lg text-gray-600 ml-1">kg</span>
              </div>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-green-500">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">
                잉여전력 활용
              </CardTitle>
              <Zap className="h-5 w-5 text-green-500" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-gray-900">
                164
                <span className="text-lg text-gray-600 ml-1">MWh</span>
              </div>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-blue-500">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">
                생산 단가
              </CardTitle>
              <DollarSign className="h-5 w-5 text-blue-500" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-gray-900">
                4,850
                <span className="text-lg text-gray-600 ml-1">원/kg</span>
              </div>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-purple-500">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">
                탄소 감축
              </CardTitle>
              <TrendingDown className="h-5 w-5 text-purple-500" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-purple-600">
                32.8
                <span className="text-lg text-gray-600 ml-1">톤 CO₂</span>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Production Simulator */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>그린수소 생산 시뮬레이터</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Input Form */}
              <div className="space-y-4">
                <div>
                  <Label>수전해 방식</Label>
                  <Select
                    value={selectedElectrolyzer?.id || ''}
                    onValueChange={(value) => {
                      const electrolyzer = electrolyzerTypes.find(e => e.id === value);
                      setSelectedElectrolyzer(electrolyzer || null);
                    }}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="수전해 방식 선택" />
                    </SelectTrigger>
                    <SelectContent>
                      {electrolyzerTypes.map((type) => (
                        <SelectItem key={type.id} value={type.id}>
                          {type.name} ({type.nameKo})
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label>잉여전력 (MW)</Label>
                  <Input
                    type="number"
                    value={surplusPower}
                    onChange={(e) => setSurplusPower(Number(e.target.value))}
                    placeholder="잉여전력을 입력하세요"
                    min={0}
                  />
                </div>

                <div>
                  <Label>전기 단가 (원/kWh)</Label>
                  <Input
                    type="number"
                    value={electricityPrice}
                    onChange={(e) => setElectricityPrice(Number(e.target.value))}
                    placeholder="전기 단가"
                    min={0}
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    * SMP 평균: 약 80원/kWh
                  </p>
                </div>

                <Button
                  onClick={handleCalculate}
                  className="w-full bg-hydrogen-500 hover:bg-hydrogen-600"
                  disabled={!selectedElectrolyzer || surplusPower <= 0}
                >
                  <Droplet className="h-4 w-4 mr-2" />
                  수소 생산량 계산
                </Button>
              </div>

              {/* Electrolyzer Info */}
              {selectedElectrolyzer && (
                <Card className="bg-blue-50 border-blue-200">
                  <CardHeader>
                    <CardTitle className="text-base">
                      {selectedElectrolyzer.name} 특성
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">효율</span>
                      <span className="font-medium">{selectedElectrolyzer.efficiency}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">전력 소비</span>
                      <span className="font-medium">
                        {selectedElectrolyzer.powerConsumption} kWh/kg H₂
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">설비비 (CAPEX)</span>
                      <span className="font-medium">{selectedElectrolyzer.capex}억원/MW</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">수명</span>
                      <span className="font-medium">{selectedElectrolyzer.lifespan}년</span>
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Results */}
              {currentProduction && (
                <Card className="bg-gradient-to-br from-hydrogen-100 to-blue-100 border-hydrogen-300">
                  <CardHeader>
                    <CardTitle className="text-base">생산 결과</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div>
                      <div className="text-sm text-gray-600 mb-1">수소 생산량</div>
                      <div className="text-3xl font-bold text-hydrogen-700">
                        {currentProduction.outputKg}
                        <span className="text-lg ml-1">kg</span>
                      </div>
                    </div>
                    <div className="pt-3 border-t border-hydrogen-300">
                      <div className="text-sm text-gray-600 mb-1">생산 비용</div>
                      <div className="text-2xl font-bold text-blue-700">
                        {currentProduction.productionCost.toLocaleString()}
                        <span className="text-base ml-1">원/kg</span>
                      </div>
                    </div>
                    <div className="pt-3 border-t border-hydrogen-300">
                      <div className="text-sm text-gray-600 mb-1">탄소 감축량</div>
                      <div className="text-xl font-medium text-green-700">
                        {currentProduction.carbonReduction} kg CO₂
                      </div>
                      <p className="text-xs text-gray-600 mt-1">
                        (그레이수소 대비)
                      </p>
                    </div>
                  </CardContent>
                </Card>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {/* Weekly Production */}
          <Card>
            <CardHeader>
              <CardTitle>주간 수소 생산량 추이</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={mockWeeklyHydrogenProduction}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="day" />
                  <YAxis yAxisId="left" label={{ value: '생산량 (kg)', angle: -90, position: 'insideLeft' }} />
                  <YAxis yAxisId="right" orientation="right" label={{ value: '잉여전력 (MW)', angle: 90, position: 'insideRight' }} />
                  <Tooltip />
                  <Legend />
                  <Bar yAxisId="left" dataKey="production" fill="#0ea5e9" name="수소 생산량" />
                  <Bar yAxisId="right" dataKey="surplus" fill="#86efac" name="잉여전력" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Electrolyzer Comparison */}
          <Card>
            <CardHeader>
              <CardTitle>수전해 방식 비교</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={electrolyzerTypes}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="efficiency" fill="#0ea5e9" name="효율 (%)" />
                  <Bar dataKey="capex" fill="#fb923c" name="설비비 (억원/MW)" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>

        {/* Use Cases */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>그린수소 활용 시나리오</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              {hydrogenUseCases.map((useCase) => (
                <div
                  key={useCase.id}
                  className="p-4 rounded-lg border-2 border-hydrogen-200 bg-hydrogen-50 hover:border-hydrogen-400 transition-colors"
                >
                  <h3 className="font-semibold text-gray-900 mb-2">{useCase.name}</h3>
                  <p className="text-xs text-gray-600 mb-3">{useCase.nameEn}</p>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">효율</span>
                      <span className="font-medium">{useCase.efficiency}%</span>
                    </div>
                    {useCase.outputKWh && (
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-600">출력</span>
                        <span className="font-medium">{useCase.outputKWh} kWh/kg</span>
                      </div>
                    )}
                    {useCase.range && (
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-600">주행거리</span>
                        <span className="font-medium">{useCase.range} km/kg</span>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Economic Analysis */}
        <Card>
          <CardHeader>
            <CardTitle>경제성 분석</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="p-4 bg-blue-50 rounded-lg">
                <div className="text-sm text-gray-600 mb-1">균등화 수소비용 (LCH)</div>
                <div className="text-2xl font-bold text-blue-700">
                  5,200 <span className="text-base">원/kg</span>
                </div>
              </div>
              <div className="p-4 bg-green-50 rounded-lg">
                <div className="text-sm text-gray-600 mb-1">회수기간</div>
                <div className="text-2xl font-bold text-green-700">
                  8.5 <span className="text-base">년</span>
                </div>
              </div>
              <div className="p-4 bg-purple-50 rounded-lg">
                <div className="text-sm text-gray-600 mb-1">내부수익률 (IRR)</div>
                <div className="text-2xl font-bold text-purple-700">
                  12.5 <span className="text-base">%</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}


