'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { MapPin, AlertTriangle, Satellite, CloudRain } from 'lucide-react';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';

const mockRiskAreas = [
  { id: 1, name: '제주시 도심', riskLevel: 'high', rainfall: 350, slope: 5, population: 45000 },
  { id: 2, name: '서귀포 해안', riskLevel: 'medium', rainfall: 280, slope: 15, population: 28000 },
  { id: 3, name: '한경면 농경지', riskLevel: 'low', rainfall: 200, slope: 8, population: 5000 },
  { id: 4, name: '성산 일출봉', riskLevel: 'high', rainfall: 380, slope: 3, population: 12000 },
  { id: 5, name: '중문 관광단지', riskLevel: 'medium', rainfall: 260, slope: 12, population: 18000 },
];

const rainfallForecast = [
  { day: '오늘', rainfall: 35, risk: 45 },
  { day: '+1일', rainfall: 85, risk: 72 },
  { day: '+2일', rainfall: 120, risk: 85 },
  { day: '+3일', rainfall: 65, risk: 58 },
  { day: '+4일', rainfall: 30, risk: 38 },
  { day: '+5일', rainfall: 20, risk: 28 },
  { day: '+6일', rainfall: 15, risk: 22 },
];

const facilityRisks = [
  { facility: '풍력 A', type: 'wind', risk: 25, lat: 33.23, lng: 126.31 },
  { facility: '태양광 B', type: 'solar', risk: 78, lat: 33.51, lng: 126.49 },
  { facility: '바이오차 C', type: 'biochar', risk: 42, lat: 33.49, lng: 126.49 },
  { facility: 'RE100 D', type: 're100', risk: 68, lat: 33.50, lng: 126.53 },
  { facility: '수소 E', type: 'hydrogen', risk: 35, lat: 33.41, lng: 126.29 },
];

const eoDataSources = [
  { name: 'NASA MODIS', type: '지표면 온도', coverage: '제주 전역', update: '매일' },
  { name: 'JAXA ALOS-2', type: '지형 변화', coverage: '제주 전역', update: '주간' },
  { name: 'Sentinel-1', type: 'SAR 침수 감지', coverage: '해안선', update: '실시간' },
  { name: 'GPM', type: '강수량 측정', coverage: '동아시아', update: '매시간' },
];

export default function FloodRiskPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">Flood Risk Analysis</h1>
          <p className="text-gray-600">지구관측 데이터 기반 침수위험 분석 및 시설 보호</p>
        </div>

        {/* Alert Banner */}
        <Card className="mb-8 border-l-4 border-l-orange-500 bg-orange-50">
          <CardContent className="py-4">
            <div className="flex items-start">
              <AlertTriangle className="h-6 w-6 text-orange-500 mr-3 mt-1" />
              <div>
                <h3 className="font-bold text-orange-800 mb-1">중급 침수 경보</h3>
                <p className="text-sm text-orange-700">
                  내일(+2일) 120mm 집중호우 예상 • 제주시 도심 및 성산 지역 주의 • 
                  태양광 B 시설 및 RE100 D 데이터센터 긴급 점검 필요
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Risk Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="border-l-4 border-l-red-500">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">
                고위험 지역
              </CardTitle>
              <AlertTriangle className="h-5 w-5 text-red-500" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-red-600">
                2
                <span className="text-lg text-gray-600 ml-1">개소</span>
              </div>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-yellow-500">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">
                중위험 지역
              </CardTitle>
              <MapPin className="h-5 w-5 text-yellow-500" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-yellow-600">
                2
                <span className="text-lg text-gray-600 ml-1">개소</span>
              </div>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-blue-500">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">
                예상 강수량
              </CardTitle>
              <CloudRain className="h-5 w-5 text-blue-500" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-blue-600">
                120
                <span className="text-lg text-gray-600 ml-1">mm</span>
              </div>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-purple-500">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">
                위성 데이터
              </CardTitle>
              <Satellite className="h-5 w-5 text-purple-500" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-purple-600">
                4
                <span className="text-lg text-gray-600 ml-1">소스</span>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Map Placeholder */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center">
              <MapPin className="h-5 w-5 mr-2" />
              제주도 침수위험 지도
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="relative bg-gradient-to-br from-blue-100 via-green-100 to-yellow-100 rounded-lg h-96 flex items-center justify-center">
              <div className="absolute inset-0 opacity-20">
                <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
                  <defs>
                    <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
                      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="gray" strokeWidth="0.5"/>
                    </pattern>
                  </defs>
                  <rect width="100%" height="100%" fill="url(#grid)" />
                </svg>
              </div>
              <div className="text-center z-10">
                <MapPin className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600 font-medium mb-2">인터랙티브 침수위험 지도</p>
                <div className="flex items-center justify-center gap-4 text-sm">
                  <div className="flex items-center">
                    <div className="w-4 h-4 bg-red-500 rounded mr-2"></div>
                    <span>고위험</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-4 h-4 bg-yellow-500 rounded mr-2"></div>
                    <span>중위험</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-4 h-4 bg-green-500 rounded mr-2"></div>
                    <span>저위험</span>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {/* Rainfall Forecast */}
          <Card>
            <CardHeader>
              <CardTitle>7일 강수량 예측 & 위험도</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={250}>
                <LineChart data={rainfallForecast}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="day" />
                  <YAxis yAxisId="left" label={{ value: '강수량 (mm)', angle: -90, position: 'insideLeft' }} />
                  <YAxis yAxisId="right" orientation="right" label={{ value: '위험도', angle: 90, position: 'insideRight' }} />
                  <Tooltip />
                  <Legend />
                  <Line yAxisId="left" type="monotone" dataKey="rainfall" stroke="#3b82f6" strokeWidth={2} name="강수량" />
                  <Line yAxisId="right" type="monotone" dataKey="risk" stroke="#ef4444" strokeWidth={2} name="위험도" />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Facility Risk Scatter */}
          <Card>
            <CardHeader>
              <CardTitle>시설별 침수 위험도</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={facilityRisks}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="facility" />
                  <YAxis label={{ value: '위험도 점수', angle: -90, position: 'insideLeft' }} />
                  <Tooltip />
                  <Bar dataKey="risk">
                    {facilityRisks.map((entry, index) => (
                      <Cell
                        key={`cell-${index}`}
                        fill={entry.risk > 60 ? '#ef4444' : entry.risk > 40 ? '#f59e0b' : '#22c55e'}
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>

        {/* Risk Areas Table */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>침수위험 지역 상세</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-3 px-4 font-medium text-gray-600">지역</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">위험도</th>
                    <th className="text-right py-3 px-4 font-medium text-gray-600">예상 강수량</th>
                    <th className="text-right py-3 px-4 font-medium text-gray-600">경사도</th>
                    <th className="text-right py-3 px-4 font-medium text-gray-600">인구</th>
                    <th className="text-center py-3 px-4 font-medium text-gray-600">조치</th>
                  </tr>
                </thead>
                <tbody>
                  {mockRiskAreas.map((area) => (
                    <tr key={area.id} className="border-b hover:bg-gray-50">
                      <td className="py-3 px-4">{area.name}</td>
                      <td className="py-3 px-4">
                        <span
                          className={`px-3 py-1 rounded-full text-xs font-medium ${
                            area.riskLevel === 'high'
                              ? 'bg-red-100 text-red-700'
                              : area.riskLevel === 'medium'
                              ? 'bg-yellow-100 text-yellow-700'
                              : 'bg-green-100 text-green-700'
                          }`}
                        >
                          {area.riskLevel === 'high' ? '높음' : area.riskLevel === 'medium' ? '중간' : '낮음'}
                        </span>
                      </td>
                      <td className="text-right py-3 px-4">{area.rainfall}mm</td>
                      <td className="text-right py-3 px-4">{area.slope}°</td>
                      <td className="text-right py-3 px-4">{area.population.toLocaleString()}명</td>
                      <td className="text-center py-3 px-4">
                        {area.riskLevel === 'high' && (
                          <span className="text-xs text-red-600 font-medium">긴급 점검</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>

        {/* EO Data Sources */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Satellite className="h-5 w-5 mr-2" />
              지구관측 (EO) 데이터 소스
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {eoDataSources.map((source, idx) => (
                <div
                  key={idx}
                  className="p-4 rounded-lg border border-blue-200 bg-blue-50 hover:border-blue-400 transition-colors"
                >
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-bold text-gray-900">{source.name}</h3>
                    <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full font-medium">
                      {source.update}
                    </span>
                  </div>
                  <div className="space-y-1 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600">유형</span>
                      <span className="font-medium">{source.type}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">범위</span>
                      <span className="font-medium">{source.coverage}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}


