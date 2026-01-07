'use client';

import { Button } from '@/components/ui/button';
import { 
  LayoutDashboard, 
  Wind, 
  Leaf, 
  Droplet, 
  Brain, 
  MapPin, 
  Info,
  Sprout,
  User,
  LogOut 
} from 'lucide-react';
import { useRouter, usePathname } from 'next/navigation';
import { useUserStore } from '@/store/userStore';
import { useAuthStore } from '@/store/auth.store';

export function Navigation() {
  const router = useRouter();
  const pathname = usePathname();
  const { user, logout } = useUserStore();
  const accessToken = useAuthStore((s) => s.accessToken);
  const clearAccessToken = useAuthStore((s) => s.clearAccessToken);

  const handleLogout = () => {
    logout();
    sessionStorage.removeItem('user');
    localStorage.removeItem('user');
    clearAccessToken();
    router.push('/');
  };

  const tabs = [
    { id: 'dashboard', label: '대시보드', path: '/dashboard', icon: LayoutDashboard },
    { id: 'renewable', label: 'RE100', path: '/renewable-energy', icon: Wind },
    { id: 'biochar', label: 'Biochar', path: '/biochar', icon: Leaf },
    { id: 'hydrogen', label: 'Green H₂', path: '/green-hydrogen', icon: Droplet },
    { id: 'ai', label: 'AI 최적화', path: '/ai-optimization', icon: Brain },
    { id: 'flood', label: '위험분석', path: '/flood-risk', icon: MapPin },
    { id: 'about', label: 'About', path: '/about', icon: Info },
  ];

  return (
    <nav className="bg-white border-b border-border shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div
            className="flex items-center space-x-3 cursor-pointer"
            onClick={() => router.push('/')}
          >
            <div className="relative">
              <Sprout className="h-8 w-8 text-seed-500 leaf-sway" />
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-hydrogen-400 rounded-full animate-pulse"></div>
            </div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-seed-600 to-hydrogen-500 bg-clip-text text-transparent">
              RE:SEED
            </h1>
          </div>

          {/* Navigation Tabs */}
          <div className="flex items-center space-x-1">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              const isActive = pathname === tab.path || pathname.startsWith(tab.path + '/');

              return (
                <Button
                  key={tab.id}
                  variant={isActive ? "default" : "ghost"}
                  onClick={() => router.push(tab.path)}
                  className={`
                    flex items-center space-x-2 px-4 py-2 rounded-lg transition-all duration-300
                    ${isActive
                      ? 'bg-seed-500 text-white shadow-lg hover:bg-seed-600'
                      : 'text-muted-foreground hover:text-seed-600 hover:bg-seed-50'
                    }
                  `}
                >
                  <Icon className={`h-4 w-4 ${isActive ? 'seed-grow' : ''}`} />
                  <span className="font-medium text-sm">{tab.label}</span>
                </Button>
              );
            })}

            {/* 로그인된 경우 사용자 정보 + 로그아웃 버튼 표시 */}
            {user && (
              <>
                <div className="flex items-center space-x-2 px-4 py-2 text-muted-foreground border-l border-border ml-2">
                  <User className="h-4 w-4" />
                  <span className="font-medium text-sm">{user.name || user.email}</span>
                </div>
                <Button
                  variant="ghost"
                  onClick={handleLogout}
                  className="flex items-center space-x-2 px-4 py-2 rounded-lg text-muted-foreground hover:text-red-600 hover:bg-red-50"
                >
                  <LogOut className="h-4 w-4" />
                  <span className="font-medium text-sm">로그아웃</span>
                </Button>
              </>
            )}
            {/* accessToken만 있고 user 정보 없으면 "로그인" 버튼 표시 */}
            {!user && accessToken && (
              <Button
                variant="ghost"
                onClick={() => router.push('/login')}
                className="flex items-center space-x-2 px-4 py-2 rounded-lg text-muted-foreground hover:text-seed-600 hover:bg-seed-50"
              >
                <User className="h-4 w-4" />
                <span className="font-medium text-sm">로그인</span>
              </Button>
            )}

            {/* 미로그인 상태에서는 로그인 버튼 노출 */}
            {!user && !accessToken && (
              <Button
                variant="default"
                onClick={() => router.push('/login')}
                className="ml-2 bg-gray-900 hover:bg-gray-800 text-white"
              >
                로그인
              </Button>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
