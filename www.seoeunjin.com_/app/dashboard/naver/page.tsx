'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/auth.store';

interface User {
    id: number;
    email: string;
    name: string;
    nickname?: string;
    profile_image?: string;
    provider: string;
}

export default function Dashboard() {
    const router = useRouter();
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);
    const accessToken = useAuthStore((state) => state.accessToken);
    const clearAccessToken = useAuthStore((state) => state.clearAccessToken);

    useEffect(() => {
        // 저장된 사용자 정보 불러오기
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
            try {
                setUser(JSON.parse(storedUser));
            } catch (err) {
                console.error('사용자 정보 파싱 실패:', err);
            }
        } else {
            // 토큰이 있으면 사용자 정보 조회
            if (accessToken) {
                fetchUserInfo(accessToken);
            } else {
                // 토큰이 없으면 로그인 페이지로 리다이렉트
                router.push('/');
            }
        }
        setLoading(false);
    }, [router, accessToken]);

    const fetchUserInfo = async (accessToken: string) => {
        try {
            const response = await fetch('http://localhost:8080/naver/user', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                },
            });

            const data = await response.json();

            if (data.success && data.user) {
                setUser(data.user);
                localStorage.setItem('user', JSON.stringify(data.user));
            } else {
                throw new Error(data.message || '사용자 정보 조회 실패');
            }
        } catch (err) {
            console.error('사용자 정보 조회 실패:', err);
            // 토큰이 유효하지 않으면 로그인 페이지로 리다이렉트
            router.push('/');
        }
    };

    const handleLogout = async () => {
        // 토큰 및 사용자 정보 삭제
        clearAccessToken();
        localStorage.removeItem('user');
        
        // 쿠키 삭제를 위한 백엔드 호출 (선택적)
        try {
            await fetch('http://localhost:8080/naver/logout', {
                method: 'POST',
                credentials: 'include',
            });
        } catch (err) {
            console.error('로그아웃 API 호출 실패:', err);
        }
        
        // 로그인 페이지로 리다이렉트 (로그아웃 플래그 포함)
        router.push('/?logout=true');
    };

    if (loading) {
        return (
            <div className="flex min-h-screen items-center justify-center bg-white font-sans">
                <div className="h-8 w-8 animate-spin rounded-full border-4 border-[#03C75A] border-t-transparent"></div>
            </div>
        );
    }

    if (!user) {
        return (
            <div className="flex min-h-screen items-center justify-center bg-white font-sans">
                <main className="flex w-full max-w-md flex-col items-center gap-8 px-8 py-16">
                    <p className="text-lg text-gray-600">사용자 정보를 불러올 수 없습니다.</p>
                    <button
                        onClick={handleLogout}
                        className="flex h-14 w-full items-center justify-center gap-3 rounded-lg bg-[#03C75A] px-6 text-base font-medium text-white transition-colors hover:bg-[#02B350]"
                    >
                        로그인 페이지로 돌아가기
                    </button>
                </main>
            </div>
        );
    }

    return (
        <div className="flex min-h-screen items-center justify-center bg-white font-sans">
            <main className="flex w-full max-w-md flex-col items-center gap-8 px-8 py-16">
                <h1 className="text-3xl font-bold text-gray-900">네이버 로그인 성공</h1>
                <div className="flex w-full flex-col gap-4 rounded-lg border border-gray-200 bg-gray-50 p-6">
                    <div className="flex items-center gap-4">
                        {user.profile_image && (
                            <img
                                src={user.profile_image}
                                alt={user.name}
                                className="h-16 w-16 rounded-full"
                            />
                        )}
                        <div className="flex flex-col">
                            <p className="text-lg font-semibold text-gray-900">{user.name}</p>
                            {user.nickname && user.nickname !== user.name && (
                                <p className="text-sm text-gray-600">@{user.nickname}</p>
                            )}
                            <p className="text-sm text-gray-500">{user.email}</p>
                        </div>
                    </div>
                    <div className="mt-4 flex flex-col gap-2">
                        <p className="text-sm text-gray-600">
                            <span className="font-medium">사용자 ID:</span> {user.id}
                        </p>
                        <p className="text-sm text-gray-600">
                            <span className="font-medium">제공자:</span> {user.provider}
                        </p>
                    </div>
                </div>
                <button
                    onClick={handleLogout}
                    className="flex h-14 w-full items-center justify-center gap-3 rounded-lg bg-[#03C75A] px-6 text-base font-medium text-white transition-colors hover:bg-[#02B350]"
                >
                    로그아웃
                </button>
            </main>
        </div>
    );
}
