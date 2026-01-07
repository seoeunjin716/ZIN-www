'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Sprout, Target, Lightbulb, Users, Code, Database, Cloud } from 'lucide-react';

const techStack = [
  { category: 'Frontend', items: ['Next.js 14', 'React', 'TypeScript', 'Tailwind CSS', 'Zustand', 'Recharts'] },
  { category: 'Backend', items: ['Node.js', 'Python', 'FastAPI', 'PostgreSQL'] },
  { category: 'AI/ML', items: ['TensorFlow', 'PyTorch', 'LSTM', 'Transformer', 'RL'] },
  { category: 'Data', items: ['NASA MODIS', 'JAXA ALOS-2', 'Sentinel-1', 'GPM', '기상청 API'] },
];

const problems = [
  {
    title: '재생에너지 과잉 생산',
    description: '제주도는 풍력·태양광 발전이 수요를 초과하여 연간 수백억원 규모의 출력제한 발생',
    icon: '⚡',
  },
  {
    title: '계통 불안정',
    description: '섬 지역 특성상 재생에너지 변동성으로 인한 전력망 안정성 문제',
    icon: '🔌',
  },
  {
    title: '바이오매스 폐기물',
    description: '음식물·가축분뇨·산림부산물 등 대량 바이오매스 미활용',
    icon: '🌾',
  },
  {
    title: '침수 위험 증가',
    description: '기후변화로 인한 집중호우 빈발, 재생에너지 시설 보호 필요',
    icon: '🌊',
  },
];

const solutions = [
  {
    title: 'RE100 재생에너지 최적화',
    description: '실시간 모니터링 & AI 발전량 예측으로 출력제한 최소화',
    color: 'from-blue-500 to-cyan-500',
  },
  {
    title: 'Biochar CCUS',
    description: '바이오매스 → 바이오차 전환으로 탄소 영구 저장',
    color: 'from-green-500 to-emerald-500',
  },
  {
    title: 'Green H₂ 생산',
    description: '잉여전력 → 그린수소 전환으로 에너지 저장',
    color: 'from-hydrogen-500 to-blue-400',
  },
  {
    title: 'AI 듀얼 최적화',
    description: '재생에너지 + 바이오차 통합 최적화로 탄소감축 극대화',
    color: 'from-purple-500 to-pink-500',
  },
];

const features = [
  {
    icon: <Target className="h-8 w-8 text-seed-500" />,
    title: 'Dual Carbon Reduction',
    description: '재생에너지 탄소감축 + 바이오차 탄소저장 이중 효과',
  },
  {
    icon: <Lightbulb className="h-8 w-8 text-yellow-500" />,
    title: 'AI 최적화 엔진',
    description: '머신러닝 기반 실시간 스케줄링 & LCA 분석',
  },
  {
    icon: <Database className="h-8 w-8 text-blue-500" />,
    title: '지구관측 데이터',
    description: 'NASA/JAXA 위성 데이터 기반 침수위험 예측',
  },
  {
    icon: <Cloud className="h-8 w-8 text-purple-500" />,
    title: '실시간 대시보드',
    description: '모든 시스템 통합 모니터링 & 알림',
  },
];

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-seed-50 via-white to-hydrogen-50">
      <div className="container mx-auto px-4 py-8">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <div className="flex justify-center mb-6">
            <Sprout className="h-20 w-20 text-seed-500 animate-leaf-sway" />
          </div>
          <h1 className="text-5xl font-bold mb-4">
            <span className="bg-gradient-to-r from-seed-600 to-hydrogen-500 bg-clip-text text-transparent">
              RE:SEED
            </span>
          </h1>
          <p className="text-2xl text-gray-700 font-semibold mb-4">
            제주 듀얼 탄소감축 플랫폼
          </p>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            재생에너지 잉여전력과 바이오차를 결합한 차세대 탄소중립 통합 솔루션<br />
            RE100 + Biochar CCUS + Green H₂ + AI Optimization
          </p>
        </div>

        {/* Problem Section */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">
            제주도가 직면한 문제
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {problems.map((problem, idx) => (
              <Card key={idx} className="hover:shadow-lg transition-shadow">
                <CardContent className="p-6">
                  <div className="text-4xl mb-4">{problem.icon}</div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">{problem.title}</h3>
                  <p className="text-gray-600">{problem.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>

        {/* Solution Section */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">
            RE:SEED 통합 솔루션
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {solutions.map((solution, idx) => (
              <Card key={idx} className="hover:shadow-xl transition-all duration-300 overflow-hidden">
                <div className={`h-2 bg-gradient-to-r ${solution.color}`}></div>
                <CardContent className="p-6">
                  <h3 className="text-lg font-bold text-gray-900 mb-3">{solution.title}</h3>
                  <p className="text-sm text-gray-600">{solution.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>

        {/* Features Section */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">
            핵심 기능
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {features.map((feature, idx) => (
              <Card key={idx} className="hover:shadow-lg transition-shadow">
                <CardContent className="p-6 flex items-start space-x-4">
                  <div className="flex-shrink-0">{feature.icon}</div>
                  <div>
                    <h3 className="text-lg font-bold text-gray-900 mb-2">{feature.title}</h3>
                    <p className="text-gray-600">{feature.description}</p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>

        {/* System Architecture */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">
            시스템 구조
          </h2>
          <Card>
            <CardContent className="p-8">
              <div className="flex flex-col items-center space-y-6">
                {/* Layer 1: Data Sources */}
                <div className="w-full">
                  <h3 className="text-center font-bold text-gray-700 mb-4">데이터 수집</h3>
                  <div className="flex justify-center space-x-4">
                    <div className="px-4 py-2 bg-blue-100 rounded-lg text-sm font-medium">기상청 API</div>
                    <div className="px-4 py-2 bg-blue-100 rounded-lg text-sm font-medium">NASA 위성</div>
                    <div className="px-4 py-2 bg-blue-100 rounded-lg text-sm font-medium">JAXA EO</div>
                    <div className="px-4 py-2 bg-blue-100 rounded-lg text-sm font-medium">에너지공단</div>
                  </div>
                </div>

                <div className="text-gray-400">↓</div>

                {/* Layer 2: AI Processing */}
                <div className="w-full">
                  <h3 className="text-center font-bold text-gray-700 mb-4">AI 처리</h3>
                  <div className="flex justify-center space-x-4">
                    <div className="px-4 py-2 bg-purple-100 rounded-lg text-sm font-medium">발전량 예측</div>
                    <div className="px-4 py-2 bg-purple-100 rounded-lg text-sm font-medium">최적화 알고리즘</div>
                    <div className="px-4 py-2 bg-purple-100 rounded-lg text-sm font-medium">LCA 분석</div>
                  </div>
                </div>

                <div className="text-gray-400">↓</div>

                {/* Layer 3: Applications */}
                <div className="w-full">
                  <h3 className="text-center font-bold text-gray-700 mb-4">통합 플랫폼</h3>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="p-4 bg-gradient-to-br from-hydrogen-100 to-blue-100 rounded-lg text-center">
                      <div className="font-bold text-sm mb-1">RE100</div>
                      <div className="text-xs text-gray-600">재생에너지</div>
                    </div>
                    <div className="p-4 bg-gradient-to-br from-seed-100 to-green-100 rounded-lg text-center">
                      <div className="font-bold text-sm mb-1">Biochar</div>
                      <div className="text-xs text-gray-600">탄소저장</div>
                    </div>
                    <div className="p-4 bg-gradient-to-br from-blue-100 to-cyan-100 rounded-lg text-center">
                      <div className="font-bold text-sm mb-1">Green H₂</div>
                      <div className="text-xs text-gray-600">수소생산</div>
                    </div>
                    <div className="p-4 bg-gradient-to-br from-orange-100 to-red-100 rounded-lg text-center">
                      <div className="font-bold text-sm mb-1">Flood Risk</div>
                      <div className="text-xs text-gray-600">위험분석</div>
                    </div>
                  </div>
                </div>

                <div className="text-gray-400">↓</div>

                {/* Layer 4: Outcome */}
                <div className="px-8 py-4 bg-gradient-to-r from-seed-500 to-hydrogen-500 rounded-lg text-white text-center">
                  <div className="font-bold text-lg">듀얼 탄소감축 달성</div>
                  <div className="text-sm mt-1">제주 탄소중립 2030</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </section>

        {/* Tech Stack */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">
            기술 스택
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {techStack.map((stack, idx) => (
              <Card key={idx}>
                <CardHeader>
                  <CardTitle className="text-base flex items-center">
                    <Code className="h-4 w-4 mr-2" />
                    {stack.category}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {stack.items.map((item, i) => (
                      <li key={i} className="text-sm text-gray-700 flex items-center">
                        <span className="w-2 h-2 bg-seed-500 rounded-full mr-2"></span>
                        {item}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>

        {/* Team */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">
            팀 소개
          </h2>
          <Card className="max-w-md mx-auto">
            <CardContent className="p-8 text-center">
              <div className="flex justify-center mb-4">
                <Users className="h-16 w-16 text-seed-500" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">ESGseed</h3>
              <p className="text-gray-600 mb-4">탄소중립 솔루션 전문팀</p>
              <div className="inline-block px-4 py-2 bg-seed-100 text-seed-700 rounded-full text-sm font-medium">
                2024 해커톤 참가
              </div>
            </CardContent>
          </Card>
        </section>

        {/* Impact Stats */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">
            예상 효과 (제주 전체 적용시)
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card className="bg-gradient-to-br from-green-50 to-seed-50">
              <CardContent className="p-8 text-center">
                <div className="text-4xl font-bold text-seed-600 mb-2">-35%</div>
                <div className="text-gray-700 font-medium">출력제한 감소</div>
                <div className="text-sm text-gray-600 mt-2">연간 수백억원 손실 방지</div>
              </CardContent>
            </Card>
            <Card className="bg-gradient-to-br from-blue-50 to-hydrogen-50">
              <CardContent className="p-8 text-center">
                <div className="text-4xl font-bold text-hydrogen-600 mb-2">+120톤</div>
                <div className="text-gray-700 font-medium">일일 CO₂ 감축</div>
                <div className="text-sm text-gray-600 mt-2">연간 43,800톤</div>
              </CardContent>
            </Card>
            <Card className="bg-gradient-to-br from-purple-50 to-pink-50">
              <CardContent className="p-8 text-center">
                <div className="text-4xl font-bold text-purple-600 mb-2">100%</div>
                <div className="text-gray-700 font-medium">바이오매스 활용</div>
                <div className="text-sm text-gray-600 mt-2">폐기물 → 자원화</div>
              </CardContent>
            </Card>
          </div>
        </section>

        {/* Contact */}
        <section className="text-center">
          <Card className="bg-gradient-to-r from-seed-500 to-hydrogen-500 text-white">
            <CardContent className="p-8">
              <h2 className="text-2xl font-bold mb-4">함께 만드는 탄소중립 제주</h2>
              <p className="mb-6">RE:SEED 플랫폼으로 지속가능한 미래를 실현합니다</p>
              <div className="flex justify-center space-x-4">
                <div className="px-6 py-3 bg-white text-seed-600 rounded-lg font-medium">
                  프로젝트 문의
                </div>
                <div className="px-6 py-3 bg-white/20 backdrop-blur rounded-lg font-medium">
                  데모 요청
                </div>
              </div>
            </CardContent>
          </Card>
        </section>
      </div>
    </div>
  );
}


