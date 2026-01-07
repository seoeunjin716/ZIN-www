'use client';

import { useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useDashboardStore } from '@/store/dashboardStore';
import { Wind, Leaf, Droplet, TrendingUp, AlertCircle, MapPin } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';

export default function DashboardPage() {
  const { overview, alerts, fetchDashboardData } = useDashboardStore();

  useEffect(() => {
    fetchDashboardData();
  }, [fetchDashboardData]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-seed-50 via-white to-hydrogen-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">종합 대시보드</h1>
          <p className="text-gray-600">제주 듀얼 탄소감축 플랫폼 실시간 현황</p>
        </div>

        {/* Main Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* 재생에너지 */}
          <Card className="border-l-4 border-l-hydrogen-500 hover:shadow-lg transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">
                재생에너지 발전
              </CardTitle>
              <Wind className="h-5 w-5 text-hydrogen-500" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-gray-900">
                {overview.renewableEnergy.todayGeneration.toLocaleString()}
                <span className="text-lg text-gray-600 ml-1">MWh</span>
              </div>
              <div className="flex items-center mt-2">
                <TrendingUp className="h-4 w-4 text-green-500 mr-1" />
                <p className="text-sm text-gray-600">
                  탄소감축: {overview.renewableEnergy.carbonReduction.toLocaleString()} 톤 CO₂
                </p>
              </div>
              <div className="mt-2">
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-hydrogen-500 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${overview.renewableEnergy.utilizationRate}%` }}
                  ></div>
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  가동률: {overview.renewableEnergy.utilizationRate}%
                </p>
              </div>
            </CardContent>
          </Card>

          {/* 바이오차 */}
          <Card className="border-l-4 border-l-seed-500 hover:shadow-lg transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">
                바이오차 생산
              </CardTitle>
              <Leaf className="h-5 w-5 text-seed-500" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-gray-900">
                {overview.biochar.todayProduction}
                <span className="text-lg text-gray-600 ml-1">톤</span>
              </div>
              <div className="flex items-center mt-2">
                <TrendingUp className="h-4 w-4 text-green-500 mr-1" />
                <p className="text-sm text-gray-600">
                  탄소저장: {overview.biochar.carbonStored} 톤 CO₂eq
                </p>
              </div>
              <div className="mt-2 flex items-center justify-between">
                <span className="text-xs text-gray-500">
                  가동 시설: {overview.biochar.facilitiesActive}/{overview.biochar.totalFacilities}
                </span>
                <div className="flex space-x-1">
                  {Array.from({ length: overview.biochar.totalFacilities }).map((_, i) => (
                    <div
                      key={i}
                      className={`w-2 h-2 rounded-full ${
                        i < overview.biochar.facilitiesActive ? 'bg-seed-500' : 'bg-gray-300'
                      }`}
                    />
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* 그린수소 */}
          <Card className="border-l-4 border-l-hydrogen-400 hover:shadow-lg transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">
                그린수소 생산
              </CardTitle>
              <Droplet className="h-5 w-5 text-hydrogen-400" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-gray-900">
                {overview.greenHydrogen.todayProduction.toLocaleString()}
                <span className="text-lg text-gray-600 ml-1">kg</span>
              </div>
              <div className="flex items-center mt-2">
                <TrendingUp className="h-4 w-4 text-green-500 mr-1" />
                <p className="text-sm text-gray-600">
                  잉여전력 활용: {overview.greenHydrogen.surplusUsed} MWh
                </p>
              </div>
              <p className="text-xs text-gray-500 mt-2">
                탄소감축: {overview.greenHydrogen.carbonReduction} 톤 CO₂
              </p>
            </CardContent>
          </Card>

          {/* Dual Carbon Score */}
          <Card className="border-l-4 border-l-purple-500 hover:shadow-lg transition-shadow bg-gradient-to-br from-purple-50 to-white">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">
                Dual Carbon Score
              </CardTitle>
              <TrendingUp className="h-5 w-5 text-purple-500" />
            </CardHeader>
            <CardContent>
              <div className="text-5xl font-bold text-purple-600">
                {overview.dualCarbonScore}
                <span className="text-2xl text-gray-600 ml-1">/100</span>
              </div>
              <p className="text-sm text-gray-600 mt-2">
                통합 탄소감축 지표
              </p>
              <div className="mt-3 w-full bg-gray-200 rounded-full h-3">
                <div 
                  className="bg-gradient-to-r from-purple-500 to-seed-500 h-3 rounded-full transition-all duration-500"
                  style={{ width: `${overview.dualCarbonScore}%` }}
                ></div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Alerts Section */}
        {alerts.length > 0 && (
          <div className="mb-8">
            <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
              <AlertCircle className="h-5 w-5 mr-2" />
              실시간 알림
            </h2>
            <div className="space-y-3">
              {alerts.slice(0, 3).map((alert) => (
                <Alert 
                  key={alert.id}
                  className={`
                    ${alert.type === 'success' ? 'border-seed-500 bg-seed-50' : ''}
                    ${alert.type === 'warning' ? 'border-alert-400 bg-orange-50' : ''}
                    ${alert.type === 'info' ? 'border-hydrogen-500 bg-blue-50' : ''}
                  `}
                >
                  <AlertDescription>
                    <div className="flex items-start justify-between">
                      <div>
                        <p className="font-semibold text-gray-900">{alert.title}</p>
                        <p className="text-sm text-gray-600 mt-1">{alert.message}</p>
                        <p className="text-xs text-gray-500 mt-1">
                          {new Date(alert.timestamp).toLocaleTimeString('ko-KR')}
                        </p>
                      </div>
                      {alert.actionRequired && (
                        <span className="px-3 py-1 bg-white rounded-full text-xs font-medium border border-gray-200">
                          조치 필요
                        </span>
                      )}
                    </div>
                  </AlertDescription>
                </Alert>
              ))}
            </div>
          </div>
        )}

        {/* Interactive Map Placeholder */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center">
              <MapPin className="h-5 w-5 mr-2" />
              제주도 통합 시설 지도
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="bg-gradient-to-br from-seed-100 to-hydrogen-100 rounded-lg h-96 flex items-center justify-center">
              <div className="text-center">
                <MapPin className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600 font-medium">인터랙티브 지도</p>
                <p className="text-sm text-gray-500 mt-2">
                  재생에너지 발전소 • 바이오차 시설 • 침수위험 지역
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">오늘의 총 탄소감축량</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-seed-600">
                {(
                  overview.renewableEnergy.carbonReduction +
                  overview.biochar.carbonStored +
                  overview.greenHydrogen.carbonReduction
                ).toLocaleString()}
                <span className="text-lg text-gray-600 ml-1">톤 CO₂</span>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">재생에너지 용량</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-hydrogen-600">
                {overview.renewableEnergy.capacity}
                <span className="text-lg text-gray-600 ml-1">MW</span>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">주간 성과 추이</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center">
                <TrendingUp className="h-8 w-8 text-green-500 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-green-600">+12.5%</div>
                  <p className="text-sm text-gray-600">전주 대비</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}


