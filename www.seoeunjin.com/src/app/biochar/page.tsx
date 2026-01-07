'use client';

import { useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';
import { useBiocharStore } from '@/store/biocharStore';
import { Leaf, Factory, TrendingUp, Sprout } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { mockWeeklyBiocharProduction } from '@/lib/mockData/biochar';

const COLORS = ['#22c55e', '#86efac', '#4ade80', '#16a34a', '#15803d'];

export default function BiocharPage() {
  const {
    materials,
    facilities,
    currentProduction,
    selectedMaterial,
    inputAmount,
    temperature,
    setSelectedMaterial,
    setInputAmount,
    setTemperature,
    calculateProduction,
    fetchBiocharData,
  } = useBiocharStore();

  useEffect(() => {
    fetchBiocharData();
  }, [fetchBiocharData]);

  const handleCalculate = () => {
    calculateProduction();
  };

  const activeFacilities = facilities.filter(f => f.status === 'active');
  const totalCapacity = facilities.reduce((sum, f) => sum + f.capacity, 0);
  const totalProduction = facilities.reduce((sum, f) => sum + f.currentProduction, 0);

  const materialDistribution = materials.slice(0, 5).map((m, idx) => ({
    name: m.name,
    value: (5 - idx) * 15 + 10, // Mock distribution
  }));

  return (
    <div className="min-h-screen bg-gradient-to-br from-seed-50 via-white to-green-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">Biochar & CCUS</h1>
          <p className="text-gray-600">바이오차 생산 및 탄소 포집·저장·활용</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="border-l-4 border-l-seed-500">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">
                총 생산량
              </CardTitle>
              <Leaf className="h-5 w-5 text-seed-500" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-gray-900">
                {totalProduction.toFixed(1)}
                <span className="text-lg text-gray-600 ml-1">톤/일</span>
              </div>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-green-500">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">
                가동 시설
              </CardTitle>
              <Factory className="h-5 w-5 text-green-500" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-gray-900">
                {activeFacilities.length}
                <span className="text-lg text-gray-600 ml-1">/ {facilities.length}</span>
              </div>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-blue-500">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">
                총 용량
              </CardTitle>
              <TrendingUp className="h-5 w-5 text-blue-500" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-gray-900">
                {totalCapacity}
                <span className="text-lg text-gray-600 ml-1">톤/일</span>
              </div>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-purple-500">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">
                가동률
              </CardTitle>
              <Sprout className="h-5 w-5 text-purple-500" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-purple-600">
                {((totalProduction / totalCapacity) * 100).toFixed(1)}
                <span className="text-lg text-gray-600 ml-1">%</span>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Calculator Section */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>바이오차 생산량 계산기</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Input Form */}
              <div className="space-y-4">
                <div>
                  <Label>원료 종류</Label>
                  <Select
                    value={selectedMaterial?.id || ''}
                    onValueChange={(value) => {
                      const material = materials.find(m => m.id === value);
                      setSelectedMaterial(material || null);
                    }}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="원료를 선택하세요" />
                    </SelectTrigger>
                    <SelectContent>
                      {materials.map((material) => (
                        <SelectItem key={material.id} value={material.id}>
                          {material.name} ({material.nameEn})
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label>투입량 (톤)</Label>
                  <Input
                    type="number"
                    value={inputAmount}
                    onChange={(e) => setInputAmount(Number(e.target.value))}
                    placeholder="투입량을 입력하세요"
                    min={0}
                  />
                </div>

                <div>
                  <Label>열분해 온도: {temperature}°C</Label>
                  <Slider
                    value={[temperature]}
                    onValueChange={(value) => setTemperature(value[0])}
                    min={350}
                    max={700}
                    step={50}
                    className="mt-2"
                  />
                  <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>350°C</span>
                    <span className="text-seed-600 font-medium">최적: 400-600°C</span>
                    <span>700°C</span>
                  </div>
                </div>

                <Button
                  onClick={handleCalculate}
                  className="w-full bg-seed-500 hover:bg-seed-600"
                  disabled={!selectedMaterial || inputAmount <= 0}
                >
                  <Leaf className="h-4 w-4 mr-2" />
                  생산량 계산
                </Button>
              </div>

              {/* Material Info */}
              {selectedMaterial && (
                <Card className="bg-seed-50 border-seed-200">
                  <CardHeader>
                    <CardTitle className="text-base">원료 특성</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">탄소 함량</span>
                      <span className="font-medium">{selectedMaterial.carbonContent}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">수율</span>
                      <span className="font-medium">{selectedMaterial.yield}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">단가</span>
                      <span className="font-medium">
                        {selectedMaterial.costPerTon.toLocaleString()}원/톤
                      </span>
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Results */}
              {currentProduction && (
                <Card className="bg-gradient-to-br from-seed-100 to-green-100 border-seed-300">
                  <CardHeader>
                    <CardTitle className="text-base">생산 결과</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div>
                      <div className="text-sm text-gray-600 mb-1">바이오차 생산량</div>
                      <div className="text-3xl font-bold text-seed-700">
                        {currentProduction.outputAmount.toFixed(2)}
                        <span className="text-lg ml-1">톤</span>
                      </div>
                    </div>
                    <div className="pt-3 border-t border-seed-300">
                      <div className="text-sm text-gray-600 mb-1">탄소 저장량</div>
                      <div className="text-2xl font-bold text-green-700">
                        {currentProduction.carbonStored.toFixed(2)}
                        <span className="text-base ml-1">톤 CO₂eq</span>
                      </div>
                    </div>
                    <div className="pt-3 border-t border-seed-300">
                      <div className="text-sm text-gray-600 mb-1">예상 소요 시간</div>
                      <div className="text-xl font-medium text-gray-700">
                        {currentProduction.duration} 시간
                      </div>
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
              <CardTitle>주간 생산량 추이</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={mockWeeklyBiocharProduction}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="day" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="production" fill="#22c55e" name="생산량 (톤)" />
                  <Bar dataKey="carbonStored" fill="#86efac" name="탄소저장 (톤)" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Material Distribution */}
          <Card>
            <CardHeader>
              <CardTitle>원료 비율</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie
                    data={materialDistribution}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {materialDistribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>

        {/* Facilities List */}
        <Card>
          <CardHeader>
            <CardTitle>제주 바이오차 생산 시설</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {facilities.map((facility) => (
                <div
                  key={facility.id}
                  className={`p-4 rounded-lg border-2 ${
                    facility.status === 'active' 
                      ? 'border-seed-300 bg-seed-50' 
                      : 'border-gray-200 bg-gray-50'
                  }`}
                >
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <h3 className="font-semibold text-gray-900">{facility.name}</h3>
                      <p className="text-sm text-gray-600">{facility.type.toUpperCase()}</p>
                    </div>
                    <span
                      className={`px-2 py-1 text-xs rounded-full font-medium ${
                        facility.status === 'active'
                          ? 'bg-seed-500 text-white'
                          : facility.status === 'maintenance'
                          ? 'bg-yellow-100 text-yellow-700'
                          : 'bg-gray-200 text-gray-700'
                      }`}
                    >
                      {facility.status === 'active' ? '가동중' : 
                       facility.status === 'maintenance' ? '정비중' : '대기'}
                    </span>
                  </div>
                  <div className="space-y-1">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">용량</span>
                      <span className="font-medium">{facility.capacity} 톤/일</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">현재 생산</span>
                      <span className="font-medium">{facility.currentProduction} 톤/일</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                      <div 
                        className={`h-2 rounded-full ${
                          facility.status === 'active' ? 'bg-seed-500' : 'bg-gray-400'
                        }`}
                        style={{ width: `${(facility.currentProduction / facility.capacity) * 100}%` }}
                      ></div>
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


