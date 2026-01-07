'use client';

import { Suspense, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { handleGoogleLogin, handleKakaoLogin, handleNaverLogin, saveAccessToken } from '@/service/mainservice';
import { useAuthStore } from '@/store/auth.store';

function LoginInner() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const accessToken = useAuthStore((state) => state.accessToken);

  useEffect(() => {
    const token = searchParams.get('token');
    const providerParam = searchParams.get('provider');
    const error = searchParams.get('error');
    const errorDescription = searchParams.get('error_description');
    const errorMessage = searchParams.get('message');

    if (token) {
      saveAccessToken(token);
      router.push(`/dashboard/${providerParam || 'google'}`);
      return;
    }

    if (error) {
      const errorMsg = errorMessage
        ? decodeURIComponent(errorMessage)
        : errorDescription
          ? decodeURIComponent(errorDescription)
          : error;

      console.error('OAuth 로그인 에러:', error, errorMsg);
      alert(`로그인 실패: ${errorMsg}`);
      return;
    }

    // 이미 로그인된 사용자는 대시보드로 이동(사용자 저장 값 기반)
    if (accessToken) {
      const storedUser = localStorage.getItem('user');
      if (storedUser) {
        try {
          const user = JSON.parse(storedUser) as { provider?: string };
          router.push(`/dashboard/${user.provider || 'google'}`);
          return;
        } catch {
          // ignore
        }
      }
    }
  }, [searchParams, router, accessToken]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-white font-sans">
      <main className="flex w-full max-w-md flex-col items-center gap-8 px-8 py-16">
        <h1 className="text-3xl font-bold text-gray-900">로그인</h1>
        <div className="flex w-full flex-col gap-4">
          <button
            onClick={handleGoogleLogin}
            className="flex h-14 w-full items-center justify-center gap-3 rounded-lg border border-gray-300 bg-white px-6 text-base font-medium text-gray-700 transition-colors hover:bg-gray-50"
          >
            구글 로그인
          </button>
          <button
            onClick={handleKakaoLogin}
            className="flex h-14 w-full items-center justify-center gap-3 rounded-lg bg-[#FEE500] px-6 text-base font-medium text-gray-900 transition-colors hover:bg-[#FDD835]"
          >
            카카오 로그인
          </button>
          <button
            onClick={handleNaverLogin}
            className="flex h-14 w-full items-center justify-center gap-3 rounded-lg bg-[#03C75A] px-6 text-base font-medium text-white transition-colors hover:bg-[#02B350]"
          >
            네이버 로그인
          </button>
        </div>
      </main>
    </div>
  );
}

export default function LoginPage() {
  return (
    <Suspense
      fallback={
        <div className="flex min-h-screen items-center justify-center bg-white font-sans">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-gray-300 border-t-transparent"></div>
        </div>
      }
    >
      <LoginInner />
    </Suspense>
  );
}


