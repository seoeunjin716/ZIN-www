'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useEnergyStore } from '@/store/energyStore';
import { Wind, Sun, AlertTriangle, Battery, Zap } from 'lucide-react';
import { AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { mockWeeklyGeneration } from '@/lib/mockData/energy';

export default function RenewableEnergyPage() {
  const { currentGeneration, forecast, curtailment, fetchEnergyData } = useEnergyStore();
  const [demand] = useState(650); // Mock 수요 (MW)

  useEffect(() => {
    fetchEnergyData();
  }, [fetchEnergyData]);

  const surplusEnergy = Math.max(0, currentGeneration.total - demand);

  return (
    <div className="min-h-screen bg-gradient-to-br from-hydrogen-50 via-white to-blue-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">RE100 & 재생에너지</h1>
          <p className="text-gray-600">제주도 재생에너지 실시간 모니터링 및 최적화</p>
        </div>

        {/* Real-time Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="border-l-4 border-l-blue-500">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">
                풍력 발전
              </CardTitle>
              <Wind className="h-5 w-5 text-blue-500" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-gray-900">
                {currentGeneration.wind}
                <span className="text-lg text-gray-600 ml-1">MW</span>
              </div>
              <p className="text-xs text-gray-500 mt-2">실시간 출력</p>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-yellow-500">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">
                태양광 발전
              </CardTitle>
              <Sun className="h-5 w-5 text-yellow-500" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-gray-900">
                {currentGeneration.solar}
                <span className="text-lg text-gray-600 ml-1">MW</span>
              </div>
              <p className="text-xs text-gray-500 mt-2">실시간 출력</p>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-green-500">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">
                총 발전량
              </CardTitle>
              <Zap className="h-5 w-5 text-green-500" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-gray-900">
                {currentGeneration.total}
                <span className="text-lg text-gray-600 ml-1">MW</span>
              </div>
              <p className="text-xs text-gray-500 mt-2">풍력 + 태양광</p>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-orange-500">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">
                잉여 전력
              </CardTitle>
              <Battery className="h-5 w-5 text-orange-500" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-orange-600">
                {surplusEnergy.toFixed(1)}
                <span className="text-lg text-gray-600 ml-1">MW</span>
              </div>
              <p className="text-xs text-gray-500 mt-2">수소/바이오차 전환 가능</p>
            </CardContent>
          </Card>
        </div>

        {/* Curtailment Alert */}
        {curtailment.currentStatus !== 'normal' && (
          <Card className="mb-8 border-l-4 border-l-red-500 bg-red-50">
            <CardContent className="py-4">
              <div className="flex items-start">
                <AlertTriangle className="h-6 w-6 text-red-500 mr-3 mt-1" />
                <div>
                  <h3 className="font-bold text-red-800 mb-1">출력제한 경고</h3>
                  <p className="text-sm text-red-700">
                    오늘 {curtailment.todayEvents}건의 출력제한 발생 • 
                    총 {curtailment.totalLossMWh} MWh 손실 • 
                    현재 {curtailment.affectedCapacity}MW 제한 중
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* 24h Forecast Chart */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>24시간 발전량 예측 (AI)</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={forecast}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="hour" 
                  label={{ value: '시간', position: 'insideBottom', offset: -5 }}
                />
                <YAxis label={{ value: 'MW', angle: -90, position: 'insideLeft' }} />
                <Tooltip />
                <Legend />
                <Area 
                  type="monotone" 
                  dataKey="solar" 
                  stackId="1"
                  stroke="#eab308" 
                  fill="#fef08a" 
                  name="태양광"
                />
                <Area 
                  type="monotone" 
                  dataKey="wind" 
                  stackId="1"
                  stroke="#3b82f6" 
                  fill="#93c5fd" 
                  name="풍력"
                />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Weekly Generation */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>주간 발전량 vs 수요</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={mockWeeklyGeneration}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis label={{ value: 'MWh', angle: -90, position: 'insideLeft' }} />
                <Tooltip />
                <Legend />
                <Bar dataKey="solar" fill="#fbbf24" name="태양광" />
                <Bar dataKey="wind" fill="#3b82f6" name="풍력" />
                <Bar dataKey="demand" fill="#ef4444" name="수요" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* RE100 Sites */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">RE100 인증 사업장</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">제주 데이터센터 A</span>
                  <span className="px-2 py-1 bg-seed-100 text-seed-700 text-xs rounded-full font-medium">
                    인증완료
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">제주 산업단지 B</span>
                  <span className="px-2 py-1 bg-yellow-100 text-yellow-700 text-xs rounded-full font-medium">
                    진행중
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">제주 스마트팜</span>
                  <span className="px-2 py-1 bg-seed-100 text-seed-700 text-xs rounded-full font-medium">
                    인증완료
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">잉여전력 활용</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-600">수소 생산</span>
                    <span className="font-medium">50%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-hydrogen-500 h-2 rounded-full" style={{ width: '50%' }}></div>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-600">바이오차</span>
                    <span className="font-medium">30%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-seed-500 h-2 rounded-full" style={{ width: '30%' }}></div>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-600">배터리 저장</span>
                    <span className="font-medium">20%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-orange-500 h-2 rounded-full" style={{ width: '20%' }}></div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">계통 혼잡도</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-center h-full">
                <div className="text-center">
                  <div className="text-5xl font-bold text-green-600 mb-2">양호</div>
                  <p className="text-sm text-gray-600">현재 계통 상태</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}


