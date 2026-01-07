'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Brain, TrendingUp, Calendar, Lightbulb, Leaf } from 'lucide-react';
import { AreaChart, Area, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';

const mockOptimizationSchedule = [
  { time: '00:00', biochar: 30, hydrogen: 50, battery: 20, score: 75 },
  { time: '03:00', biochar: 35, hydrogen: 45, battery: 20, score: 78 },
  { time: '06:00', biochar: 25, hydrogen: 55, battery: 20, score: 82 },
  { time: '09:00', biochar: 20, hydrogen: 60, battery: 20, score: 85 },
  { time: '12:00', biochar: 30, hydrogen: 50, battery: 20, score: 88 },
  { time: '15:00', biochar: 35, hydrogen: 45, battery: 20, score: 84 },
  { time: '18:00', biochar: 40, hydrogen: 40, battery: 20, score: 80 },
  { time: '21:00', biochar: 35, hydrogen: 45, battery: 20, score: 77 },
];

const lcaData = [
  { stage: '원료채취', renewable: 10, biochar: 15, hydrogen: 8 },
  { stage: '생산', renewable: 5, biochar: 25, hydrogen: 35 },
  { stage: '운송', renewable: 8, biochar: 12, hydrogen: 15 },
  { stage: '사용', renewable: -80, biochar: -90, hydrogen: -75 },
  { stage: '폐기', renewable: 3, biochar: 2, hydrogen: 5 },
];

const systemPerformance = [
  { subject: 'CO₂ 감축', A: 92, fullMark: 100 },
  { subject: '비용 효율', A: 78, fullMark: 100 },
  { subject: '안정성', A: 85, fullMark: 100 },
  { subject: '확장성', A: 88, fullMark: 100 },
  { subject: '환경 영향', A: 95, fullMark: 100 },
];

const recommendations = [
  {
    id: 1,
    title: '바이오차 생산 스케줄 조정',
    description: '오후 2-4시 태양광 피크 시간에 바이오차 열분해 프로세스 집중',
    impact: '탄소감축량 +15%',
    priority: 'high',
  },
  {
    id: 2,
    title: '수소 전해조 가동률 최적화',
    description: '야간 풍력 잉여전력 시간대에 수소 생산 증대',
    impact: '에너지 효율 +12%',
    priority: 'high',
  },
  {
    id: 3,
    title: 'RE100 부하 제어 개선',
    description: '데이터센터 유연 부하 활용으로 계통 안정성 향상',
    impact: '출력제한 -20%',
    priority: 'medium',
  },
  {
    id: 4,
    title: '바이오차-수소 하이브리드 운영',
    description: '바이오차 가스화와 수전해 결합으로 시너지 효과',
    impact: '총 생산성 +18%',
    priority: 'medium',
  },
];

export default function AIOptimizationPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">AI Optimization</h1>
          <p className="text-gray-600">듀얼 탄소감축 시스템 AI 최적화 엔진</p>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="border-l-4 border-l-purple-500">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">
                최적화 점수
              </CardTitle>
              <Brain className="h-5 w-5 text-purple-500" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-purple-600">
                87
                <span className="text-lg text-gray-600 ml-1">/100</span>
              </div>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-green-500">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">
                예측 정확도
              </CardTitle>
              <TrendingUp className="h-5 w-5 text-green-500" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-green-600">
                94.2
                <span className="text-lg text-gray-600 ml-1">%</span>
              </div>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-blue-500">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">
                CO₂ 최적화
              </CardTitle>
              <Leaf className="h-5 w-5 text-blue-500" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-blue-600">
                +18.5
                <span className="text-lg text-gray-600 ml-1">%</span>
              </div>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-orange-500">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">
                비용 절감
              </CardTitle>
              <TrendingUp className="h-5 w-5 text-orange-500" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-orange-600">
                ₩2.4M
                <span className="text-lg text-gray-600 ml-1">/월</span>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* AI Recommendations */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center">
              <Lightbulb className="h-5 w-5 mr-2 text-yellow-500" />
              AI 추천 최적화 전략
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recommendations.map((rec) => (
                <div
                  key={rec.id}
                  className={`p-4 rounded-lg border-l-4 ${
                    rec.priority === 'high'
                      ? 'border-l-red-500 bg-red-50'
                      : 'border-l-yellow-500 bg-yellow-50'
                  }`}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <h3 className="font-bold text-gray-900">{rec.title}</h3>
                        <span
                          className={`px-2 py-1 text-xs rounded-full font-medium ${
                            rec.priority === 'high'
                              ? 'bg-red-100 text-red-700'
                              : 'bg-yellow-100 text-yellow-700'
                          }`}
                        >
                          {rec.priority === 'high' ? '높음' : '중간'}
                        </span>
                      </div>
                      <p className="text-sm text-gray-600 mb-2">{rec.description}</p>
                      <div className="flex items-center gap-2">
                        <TrendingUp className="h-4 w-4 text-green-600" />
                        <span className="text-sm font-medium text-green-600">
                          예상 효과: {rec.impact}
                        </span>
                      </div>
                    </div>
                    <Button size="sm" className="bg-purple-500 hover:bg-purple-600">
                      적용
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Optimization Schedule */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center">
              <Calendar className="h-5 w-5 mr-2" />
              24시간 최적화 스케줄
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={mockOptimizationSchedule}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis yAxisId="left" label={{ value: '전력 배분 (%)', angle: -90, position: 'insideLeft' }} />
                <YAxis yAxisId="right" orientation="right" label={{ value: '최적화 점수', angle: 90, position: 'insideRight' }} />
                <Tooltip />
                <Legend />
                <Area yAxisId="left" type="monotone" dataKey="hydrogen" stackId="1" stroke="#0ea5e9" fill="#0ea5e9" name="수소 생산" />
                <Area yAxisId="left" type="monotone" dataKey="biochar" stackId="1" stroke="#22c55e" fill="#22c55e" name="바이오차" />
                <Area yAxisId="left" type="monotone" dataKey="battery" stackId="1" stroke="#fb923c" fill="#fb923c" name="배터리" />
                <Line yAxisId="right" type="monotone" dataKey="score" stroke="#8b5cf6" strokeWidth={2} name="최적화 점수" />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* LCA Analysis & System Performance */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {/* LCA */}
          <Card>
            <CardHeader>
              <CardTitle>전과정 평가 (LCA) 탄소배출량</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={lcaData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="stage" />
                  <YAxis label={{ value: 'kg CO₂eq', angle: -90, position: 'insideLeft' }} />
                  <Tooltip />
                  <Legend />
                  <Area type="monotone" dataKey="renewable" stroke="#0ea5e9" fill="#0ea5e9" name="재생에너지" />
                  <Area type="monotone" dataKey="biochar" stroke="#22c55e" fill="#22c55e" name="바이오차" />
                  <Area type="monotone" dataKey="hydrogen" stroke="#38bdf8" fill="#38bdf8" name="수소" />
                </AreaChart>
              </ResponsiveContainer>
              <div className="mt-4 p-3 bg-green-50 rounded-lg">
                <p className="text-sm font-medium text-green-800">
                  총 순 탄소감축량: <span className="text-lg font-bold">-242 kg CO₂eq</span>
                </p>
                <p className="text-xs text-green-600 mt-1">
                  * 마이너스 값은 탄소 순 제거를 의미
                </p>
              </div>
            </CardContent>
          </Card>

          {/* System Performance Radar */}
          <Card>
            <CardHeader>
              <CardTitle>시스템 성능 평가</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <RadarChart data={systemPerformance}>
                  <PolarGrid />
                  <PolarAngleAxis dataKey="subject" />
                  <PolarRadiusAxis angle={90} domain={[0, 100]} />
                  <Radar name="현재 성능" dataKey="A" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.6} />
                  <Tooltip />
                </RadarChart>
              </ResponsiveContainer>
              <div className="mt-4 grid grid-cols-2 gap-3">
                {systemPerformance.map((item) => (
                  <div key={item.subject} className="flex items-center justify-between text-sm">
                    <span className="text-gray-600">{item.subject}</span>
                    <span className="font-bold text-purple-600">{item.A}/100</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* AI Model Info */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="bg-gradient-to-br from-purple-50 to-blue-50">
            <CardHeader>
              <CardTitle className="text-base">위성 데이터 학습</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">데이터 소스</span>
                  <span className="font-medium">NASA/JAXA</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">학습 데이터</span>
                  <span className="font-medium">2년치</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">업데이트</span>
                  <span className="font-medium">실시간</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-green-50 to-blue-50">
            <CardHeader>
              <CardTitle className="text-base">기상 예측 모델</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">예측 범위</span>
                  <span className="font-medium">72시간</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">정확도</span>
                  <span className="font-medium">94.2%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">모델</span>
                  <span className="font-medium">LSTM + Transformer</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-yellow-50 to-orange-50">
            <CardHeader>
              <CardTitle className="text-base">최적화 알고리즘</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">알고리즘</span>
                  <span className="font-medium">RL + GA</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">처리 시간</span>
                  <span className="font-medium">&lt; 1초</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">개선율</span>
                  <span className="font-medium">+18.5%</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}


